# Libraries and classes needed to make registration class
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import PickupTeam


# Registration Class
class NewPickupUserForm(forms.ModelForm):
    username = forms.CharField(label='Enter Pickup Game Username (4-150 characters):', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    long_coordinates = forms.FloatField(label='Enter Longitude Coordinates (-180 <= x <= 180):')
    lat_coordinates = forms.FloatField(label='Enter Latitude Coordinates (-90 <= x <= 90):')

    class Meta:
        model = PickupTeam
        fields = '__all__'

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def clean_long_coordinates(self):
        long = self.cleaned_data.get('long_coordinates')

        if long < -180 or long > 180:
            raise ValidationError("Longitude is invalid")

        return long

    def clean_lat_coordinates(self):
        lat = self.cleaned_data.get('lat_coordinates')

        if lat < -90 or lat > 90:
            raise ValidationError("Latitude is invalid")

        return lat


    def save(self, commit=True):

        self.clean_lat_coordinates()
        self.clean_long_coordinates()

        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )
        return user