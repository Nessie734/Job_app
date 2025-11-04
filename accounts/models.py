from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        APPLICANT = 'applicant', 'Applicant'
        EMPLOYER = 'employer', 'Employer'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.APPLICANT
    )

    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
