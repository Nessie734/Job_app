from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job
from .forms import JobForm
# Create your views here.
@login_required
def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_details.html', {'job': job})

@login_required
def create_job(request):
    if request.user.role != 'employer':
        messages.error(request, "Only employers can post jobs.")
        return redirect('jobs:job_list')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('jobs:job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect('jobs:job_detail', job_id=job.id)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect('jobs:job_list')

#adding the notification module
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import ApplicationStatusForm
from .models import Application

def update_application_status(request,application_id):
    application = get_object_or_404(Application, pk=application_id)
    
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            app = form.save()

            # Send notification email
            subject = f"Application Update for {app.job.title}"
            message = f"Hello {app.applicant_name},\n\nYour application status is now: {app.get_status_display()}."
            send_mail(subject, message, 'agggiego20@gmail.com', [app.email])
            
            app.notification_sent = True
            app.save()

            messages.success(request, f"Notification sent to {app.applicant_name}")
            return redirect('job_detail')  # Replace with your employer's application list view
    else:
        form = ApplicationStatusForm(instance=application)

    return render(request, 'jobs/update_status.html', {'form': form, 'application': application})
