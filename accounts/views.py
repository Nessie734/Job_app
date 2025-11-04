from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('home')  # later we'll define this route
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')
# def home_page(request):
    # return render(request, 'accounts/home_page.html')
# core/views.py (or accounts/views.py)

from django.shortcuts import render
from django.db.models import Q
from jobs.models import Job

def home_page(request):
    """
    Homepage view:
    - optional search via GET param 'q'
    - returns 'featured_jobs' (first 4 active results) and echoes 'q'
    """
    q = request.GET.get('q', '').strip()

    # Base queryset: only active jobs
    qs = Job.objects.filter(is_active=True)

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(employer__username__icontains=q)
        )

    # Featured on homepage: latest 4 (you can change the selection logic)
    featured_jobs = qs.order_by('-created_at')[:4]

    context = {
        'featured_jobs': featured_jobs,
        'q': q,
    }
    return render(request, 'accounts/home_page.html', context)

# second login view
# # accounts/views.py
# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django import forms

# class LoginForm(forms.Form):
#     username = forms.CharField(label="Username or Email")
#     password = forms.CharField(widget=forms.PasswordInput)

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('home')

#     form = LoginForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']

#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             messages.success(request, f"Welcome back, {user.username}!")
#             return redirect('home')
#         else:
#             form.add_error(None, "Invalid username or password.")
#     return render(request, 'accounts/login.html', {'form': form})
def about_us(request):
    return render(request, "accounts/about.html")
    
    