from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    teamName = models.TextField(20)

    def authenticate(username, password):
        for user in User.objects.all():
            if (user.username == username and user.password == password):
                return user
        return None