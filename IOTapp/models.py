from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Device(models.Model):
    SN = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    last_updated = models.DateTimeField()
    temperature = models.IntegerField()
    threshold = models.IntegerField()
    user = models.ForeignKey(User)
