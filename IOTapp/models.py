import django.utils.timezone as timezone

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Device(models.Model):
    SN = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    last_updated = models.DateTimeField(default=timezone.now)
    temperature = models.IntegerField(default=0)
    threshold = models.IntegerField()
    user = models.ForeignKey(User)
    is_open = models.BooleanField()


class DeviceLog(models.Model):
    SN = models.CharField(max_length=10)
    time = models.DateTimeField(default=timezone.now)
    temperature = models.IntegerField(default=0)
    is_open = models.BooleanField(default=True)

