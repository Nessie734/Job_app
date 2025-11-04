from django.urls import path
from . import views
from applications.views import apply_for_job

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('create/', views.create_job, name='create_job'),
    path('<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('<int:job_id>/delete/', views.delete_job, name='delete_job'),
     path('apply/<int:job_id>/', apply_for_job, name='apply_for_job')
]
