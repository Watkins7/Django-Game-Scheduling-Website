from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#Creates a field type the forces the characters to be lowercase. This helps
#preserve uniqueness
class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower() 

# Create your models here.
class User(AbstractUser):
    teamName = models.TextField(20)

    def authenticate(username, password):
        for user in User.objects.all():
            if (user.username == username and user.password == password):
                return user
        return None

class Games(models.Model):
    game = NameField(max_length = 30, unique=True)
    gameType = models.TextField(20)


class PickupTeam(models.Model):

    teamname = models.CharField(max_length=50,default='')
    email = models.EmailField(max_length=100, default='')
    password = models.CharField(max_length=50,default='')
    checkpassword = models.CharField(max_length=50, default='')
    longitude = models.FloatField(default=76.7100)
    latitude = models.FloatField(default=39.2543)

    teamaccount = models.OneToOneField(User, null=True, on_delete=models.CASCADE)