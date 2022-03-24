from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PickupTeam(models.Model):

    teamname = models.CharField(max_length=50,default='')
    email = models.EmailField(max_length=100, default='')
    password = models.CharField(max_length=50,default='')
    checkpassword = models.CharField(max_length=50, default='')
    longitude = models.FloatField(default=76.7100)
    latitude = models.FloatField(default=39.2543)

    teamaccount = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
