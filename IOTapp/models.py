from django.db import models

# Create your models here.


class Device(models.Model):
    SN = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    temp_array = models.TextField
    time_array = models.TextField
    threshold = models.IntegerField
