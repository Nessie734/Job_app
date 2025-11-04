from django.urls import path
from . import views
from jobs.views import job_list
from applications.views import employer_applications, applicant_applications
app_name = 'accounts'

urlpatterns = [
    path('', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_page, name='home'),
    path('job_list/',job_list, name='job_list',),
    path('received/', employer_applications, name='employer_applications'),
    path('my-applications/', applicant_applications, name='applicant_applications'),
    path('about/', views.about_us, name="about"),
   
]