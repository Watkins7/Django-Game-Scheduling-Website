# Libraries and classes needed to make registration class
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Child Registration Form Class
class NewPickupUser(UserCreationForm):
    email = forms.EmailField(required=True)

    class PickupUser:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewPickupUser, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user