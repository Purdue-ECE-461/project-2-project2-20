from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Package(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    version = models.CharField(max_length=200, blank=True, default='')
    url = models.CharField(max_length=200, blank=True, default='')
    content = models.FileField(upload_to='zip_files/')
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)
