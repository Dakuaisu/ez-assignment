from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES=(
        ('ops','Ops User'),
        ('client','Client User'),
    )
    role=models.CharField(max_length=10,choices=ROLE_CHOICES)
    is_email_verified=models.BooleanField(default=False)

class FileUpload(models.Model):
    file=models.FileField(upload_to='uploads/')
    uploaded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    uploaded_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name