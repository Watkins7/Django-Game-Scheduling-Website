from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


#Creates a field type that forces the characters to be lowercase. This helps
#preserve uniqueness
class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower() 


# Create your models here.
class User(AbstractUser):
    mmrScore = models.IntegerField(default=50)
    teamname = models.CharField(max_length=50,default='')
    email = models.EmailField(max_length=100, default='')
    checkpassword = models.CharField(max_length=50, default='')
    longitude = models.FloatField(default=-76.7100)
    latitude = models.FloatField(default=39.2543)

    def authenticate(username, password):
        for user in User.objects.all():
            if (user.username == username and user.password == password):
                return user
        return None

    #Changes MMR based on bool parameter isWinner
    def changeMMR(self, isWinner = False):
        if(isWinner):
            self.mmrScore += 50
        else:
            self.mmrScore -= 50

        if(self.mmrScore < 0):
            self.mmrScore = 0

        return True

    def __str__(self):
        return self.username


class Games(models.Model):
    game = NameField(max_length=30, unique=True)
    gameType = models.CharField(max_length=30)

    def __str__(self):
        # This function controls how this model is displayed in query set
        return self.game


class Emails(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    is_captain = models.BooleanField()

    # Constraint to check if each team only has one captain email address associated
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team'], condition=models.Q(is_captain=True), name='One_Captain_Per_Team')
        ]


class TimeSlot(models.Model):
    host_team = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host_team', default='')
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    slot_start = models.DateTimeField('Start date/time available')
    slot_end = models.DateTimeField('End date/time available')
    opponent_team = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="opponent_team")
    host_won = models.BooleanField(null=True)
    opponent_won = models.BooleanField(null=True)

    # Checks the duration of a slot
    def slot_duration(self):
        return self.slot_end - self.slot_start

    class Meta:
        constraints = [
            # Constraint to check that a team picks unique slot date-times
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_team_slot',
                fields=['host_team', 'slot_start', 'slot_end']),
            # Constraint to check that the start of a slot is before the end
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_slotstart_lte_slotend',
                check=models.Q(slot_start__lte=models.F('slot_end')))
        ]
