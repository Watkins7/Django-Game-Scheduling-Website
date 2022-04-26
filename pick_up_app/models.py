from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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
    mmr_score = models.IntegerField(default=0)
    teamname = models.CharField(max_length=50,default='')
    email = models.EmailField(max_length=100, default='')
    checkpassword = models.CharField(max_length=50, default='')
    longitude = models.FloatField(default=-76.7100)
    latitude = models.FloatField(default=39.2543)
    mmrScore = models.IntegerField(default=50)


    def authenticate(username, password):
        for user in User.objects.all():
            if (user.username == username and user.password == password):
                return user
        return None

class Games(models.Model):
    game = NameField(max_length = 30, unique=True)
    gameType = models.TextField(20)



class Emails(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    is_captain = models.BooleanField()

    # Constraint to check if each team only has one captain email address associated
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team'], condition=models.Q(is_captain=True), name='One_Captain_Per_Team')
        ]

class MMR(models.Model):
    team = models.OneToOneField(User, on_delete=models.CASCADE)
    MMR_rating = models.FloatField(default=0)

    # Constraint to check if a team's MMR is positive
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(MMR_rating__gte=0), name='Positive_MMR_Values')
        ]


class TimeSlot(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    slot_start = models.DateTimeField('Start date/time available')
    slot_end = models.DateTimeField('End date/time available')

    # Checks whether the slot date is in the future or not
    def is_advanced_date(self):
        return self.slot_start > timezone.now()

    # Checks the duration of a slot
    def slot_duration(self):
        return self.slot_end - self.slot_start

    # Checks if the start of a slot is on the same day as the end of a slot
    def is_slot_same_day(self):
        return self.slot_start.day == self.slot_end.day

    class Meta:
        constraints = [
            # Constraint to check that a team picks unique slot date-times
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_team_slot',
                fields=['team', 'slot_start', 'slot_end']),
            # Constraint to check that the start of a slot is before the end
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_slotstart_lte_slotend',
                check=models.Q(slot_start__lte=models.F('slot_end')))
        ]
        