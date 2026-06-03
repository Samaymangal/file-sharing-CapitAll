from django.db import models
from django.contrib.auth.models import User
import os

def upload_to(instance, filename):
    return f'shared_files/{instance.uploaded_by.username}/{filename}'

class SharedFile(models.Model):
    title        = models.CharField(max_length=255)
    file         = models.FileField(upload_to=upload_to)
    uploaded_by  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    shared_with  = models.ManyToManyField(User, blank=True, related_name='received_files')
    uploaded_at  = models.DateTimeField(auto_now_add=True)
    description  = models.TextField(blank=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.title