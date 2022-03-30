from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    teamName = models.TextField(20)
    # Added mmr_score for home_page template, can be changed later
    mmr_score = models.IntegerField(default=0)

    def authenticate(username, password):
        for user in User.objects.all():
            if (user.username == username and user.password == password):
                return user
        return None
