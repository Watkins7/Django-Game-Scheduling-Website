# Libraries and classes needed to make registration class
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import PickupTeam
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


# Registration Class
class NewPickupUserForm(ModelForm):

    class Meta:
        model = PickupTeam
        fields = '__all__'
    #PickupTeam.longitude = forms.FloatField(label='Longitude!:',max_value=100)
    #PickupTeam.latitude = forms.FloatField(label='Latitude!:', max_value=100)
    #PickupTeam.email = forms.CharField(label='Email!:')

