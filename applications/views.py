from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from .forms import ApplicationForm
from jobs.models import Job

# Create your views here.

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.user.role != 'applicant':
        messages.error(request, "Only applicants can apply for jobs.")
        return redirect('jobs:job_list')

    if Application.objects.filter(applicant=request.user, job=job).exists():
        messages.warning(request, "You’ve already applied for this job.")
        return redirect('jobs:job_detail', job_id=job.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.job = job
            application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('jobs:job_detail', job_id=job.id)
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply.html', {'form': form, 'job': job})


@login_required
def employer_applications(request):
    if request.user.role != 'employer':
        messages.error(request, "Only employers can view received applications.")
        return redirect('jobs:job_list')

    applications = Application.objects.filter(job__employer=request.user).select_related('job', 'applicant')
    return render(request, 'applications/employer_applications.html', {'applications': applications})


@login_required
def applicant_applications(request):
    if request.user.role != 'applicant':
        messages.error(request, "Only applicants can view their applications.")
        return redirect('jobs:job_list')

    applications = Application.objects.filter(applicant=request.user).select_related('job')
    return render(request, 'applications/applicant_applications.html', {'applications': applications})


@login_required
def update_status(request, application_id):
    app = get_object_or_404(Application, id=application_id, job__employer=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            app.status = new_status
            app.save()
            messages.success(request, f"Application status updated to '{new_status}'.")
    return redirect('applications:employer_applications')
