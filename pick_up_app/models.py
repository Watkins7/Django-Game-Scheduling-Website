from django.db import models
from django.contrib.auth.models import AbstractUser

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