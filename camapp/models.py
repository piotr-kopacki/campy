import uuid
from datetime import date
from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.UUIDField(default=uuid.uuid4, unique=True)

class Camera(models.Model):
    alias = models.CharField(max_length=100, null=True, blank=True, default="My Camera")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rtsp = models.CharField(max_length=500)
    live = models.BooleanField(default=True)

    class Meta:
        ordering = ['live']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('camera-detail', args=[str(self.id)])
