from django import forms
from django.forms import ModelForm, DateInput
from django.utils import timezone
from .models import User, TimeSlot

# Error Handling
from django.core.exceptions import ValidationError


# Registration Form
class NewUserForm(ModelForm):
    class Meta:
        model = User

        # These are the attributes to be stored
        fields = (
            'username',
            'teamname',
            'email',
            'password',
            'checkpassword',
            'longitude',
            'latitude',)

        # This is what the form displays them as
        labels = {
            'username': "New username",
            'teamname': "New Team Name:",
            'email': "Registration Email:",
            'password': "Password:",
            'checkpassword': "Password Confirmation:",
            'longitude': "Longitude:",
            'latitude': "Latitude:",
        }

    ##########################################################
    # Handles cleaning data of form / checking accurate data
    ##########################################################
    def clean(self):

        # initial clean of form data
        f = self.cleaned_data

        # gets some of the form fields
        password1 = f.get("password")
        password2 = f.get("checkpassword")
        latitude = f.get("latitude")
        longitude = f.get("longitude")

        # validate passwords
        if password1 != password2:
            raise ValidationError("ERROR: Passwords are mismatched")

        # validate register email
        if User.objects.filter(email=f.get("email")):
            raise ValidationError("ERROR: A Team Captain has already registered this email address")

        # validate teamname
        if User.objects.filter(teamname=f.get("teamname")):
            raise ValidationError("ERROR: This team name has already been taken")

        # validate latitude
        if latitude < -90 or latitude > 90:
            raise ValidationError("ERROR: Latitude must be within -90 to 90")

        # validate longitude
        if longitude < -180 or longitude > 180:
            raise ValidationError("ERROR: Longitude must be within -180 to 180")


# Timeslot Form
class TimeSlotForm(ModelForm):
    class Meta:
        model = TimeSlot

        widgets = {
            'team': forms.HiddenInput(),
            'slot_start': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'slot_end': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    # Initializes the form, overriding the default input formats for dates
    def __init__(self, *args, **kwargs):
        super(TimeSlotForm, self).__init__(*args, **kwargs)
        self.fields['slot_start'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['slot_end'].input_formats = ('%Y-%m-%dT%H:%M',)

    # Validates form input
    def clean(self):
        f = self.cleaned_data
        team = f.get('team')
        slot_start = f.get('slot_start')
        slot_end = f.get('slot_end')

        # Checks the end of a slot is before the beginning
        if slot_start > slot_end:
            raise ValidationError("ERROR: Start of timeslot must be before end")

        # Checks the start and end of a slot are on the same day
        if slot_start.day != slot_end.day:
            raise ValidationError("ERROR: Start and end of timeslot must be on the same day")

        # Checks only future timeslots are being scheduled
        if slot_start < timezone.now():
            raise ValidationError("ERROR: Only future timeslots may be scheduled")

        # Checks timeslots do not overlap one another when a NEW timeslot is added
        # Cannot check when editing timeslots or small modifications could not be made
        if self.instance.pk is None:
            daily_timeslots = TimeSlot.objects.filter(slot_start__day=slot_start.day,
                                                      slot_end__day=slot_end.day,
                                                      team_id=team.id)
            for i in daily_timeslots:
                check1 = slot_start.time() <= timezone.localtime(i.slot_end).time()
                check2 = slot_end.time() >= timezone.localtime(i.slot_start).time()
                if check1 and check2:
                    raise ValidationError("ERROR: New timeslot overlaps existing timeslot")

        # Checks the limit on the number of timeslots for a particular day has not been reached
        num_timeslots = TimeSlot.objects.filter(slot_start__day=slot_start.day,
                                                slot_end__day=slot_end.day,
                                                team_id=team.id).count()
        if num_timeslots >= 8:
            raise ValidationError("ERROR: Maximum number of timeslots allowed on this day has been reached")
