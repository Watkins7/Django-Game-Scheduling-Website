from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class PickupTeam(models.Model):
    username = models.CharField(max_length=50,default='')
    email = models.CharField(max_length=200,default='')
    password = models.CharField(max_length=50,default='')
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
