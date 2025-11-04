from django.contrib import admin
from .models import Job
# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'job_type', 'deadline', 'is_active')
    list_filter = ('job_type', 'is_active')
    search_fields = ('title', 'location', 'employer__username')
