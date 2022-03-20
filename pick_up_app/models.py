from django.db import models

# Create your models here.

"""
class Emails(models.Model):
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.email
"""
class PickupTeam(models.Model):

    team_name = models.CharField(max_length=50)
    team_email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    team_coordinate_long = models.FloatField()
    team_coordinates_lat = models.FloatField()

    def __str__(self):
        return("Team Name:",self.team_name +
               "\nPassword:",self.password +
               "\nLat:",self.team_coordinates_lat +
               "\nLong:",self.team_coordinate_long)

