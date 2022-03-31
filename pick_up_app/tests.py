from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.

################################################
# Registration Tests
################################################
from pick_up_app.models import PickupTeam
from pick_up_app.forms import NewPickupUserForm


class registrationTests(TestCase):


    ###############################################################
    # Setup for registration
    ###############################################################
    def register_setup(self):

        t_password = "pass"
        t_check_pass = "pass"
        t_teamname = "test"
        t_email = "test.mail"
        t_long = 7
        t_lat = 13

        test_user = PickupTeam(teamname=t_teamname,
                               password=t_password,
                               email=t_email,
                               checkpassword=t_check_pass,
                               longitude=t_long,
                               latitude=t_lat)

        test_user.save()


    ###############################################################
    # Model testing for PickUpTeam
    ###############################################################
    def test_model_PickupTeam(self):

        # Model Setup
        self.register_setup()

        # Known Teamname exists
        self.assertTrue(PickupTeam.objects.filter(teamname="test").exists())

        # Known Teamname does not exists
        self.assertFalse(PickupTeam.objects.filter(teamname="testbananasbananasasasfasfasf").exists())

        # Model Teardown
        self.register_teardown()


    ###############################################################
    # Registration Form Test
    ###############################################################
    def test_pickupform(self):

        self.register_setup()

        ###############################################################
        # Test Invalid Latitude
        ###############################################################
        form_1 = NewPickupUserForm(data=None)
        form_1.fields["latitude"] = 91
        self.assertFalse(form_1.is_valid())

        form_1.fields["latitude"] = -90

        ###############################################################
        # Test Invalid/Valid Longitude
        ###############################################################
        form_1.fields["longitude"] = -181
        self.assertFalse(form_1.is_valid())

        form_1.fields["longitude"] = 180

        ###############################################################
        # Test already taken team name
        ###############################################################
        form_1.fields["teamname"] = "test"
        self.assertFalse(form_1.is_valid())

        form_1.fields["teamname"] = "test_nottaken"

        ###############################################################
        # Test already registered email
        ###############################################################
        form_1.fields["email"] = "test.mail"
        self.assertFalse(form_1.is_valid())

        form_1.fields["email"] = "test.mail.nottaken"

        ###############################################################
        # Test mismatched passwords
        ###############################################################
        form_1.fields["password"] = "pass1"
        form_1.fields["checkpassword"] = "pass2"
        self.assertFalse(form_1.is_valid())

        ###############################################################
        # Test form is valid
        ###############################################################
        form_1.fields["checkpassword"] = "pass1"
        self.assertTrue(form_1.save)

        self.register_teardown()

    ###############################################################
    # Setup for registration
    ###############################################################
    def register_teardown(self):
        PickupTeam.objects.filter(teamname="test").delete()
