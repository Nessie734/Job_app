from django.urls import path
from . import views
from applications.views import apply_for_job, applicant_applications, employer_applications, update_status

app_name = 'applications'

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('my-applications/', views.applicant_applications, name='applicant_applications'),
    path('received/', views.employer_applications, name='employer_applications'),
    path('update/<int:application_id>/', views.update_status, name='update_status'),
    path('application/<int:application_id>/update-status/', 
         update_status, name= 'update_application_status'),
]   
