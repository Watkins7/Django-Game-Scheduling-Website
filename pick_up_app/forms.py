from django.forms import ModelForm

# Team Table
from .models import PickupTeam


# Registration Form
class NewPickupUserForm(ModelForm):
    class Meta:
        model = PickupTeam

        # These are the attributes to be stored
        fields = (
            'teamname',
            'email',
            'password',
            'checkpassword'
            'longitude',
            'latitude')

        # This is what the form displays them as
        labels = {
            'teamname': "New Team Name:",
            'email': "Registration Email:",
            'password': "Password:",
            'checkpassword': "Password Conformation:",
            'longitude': "Longitude:",
            'latitude': "Latitude:"
        }
