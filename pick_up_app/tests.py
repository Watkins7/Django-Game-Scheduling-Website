from atexit import register
from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pick_up_app import models
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import os
import time

# Create your tests here.
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

################################################
# Registration Tests
################################################
from pick_up_app.models import PickupTeam
from pick_up_app.models import User
from pick_up_app.forms import NewPickupUserForm

"""
class loginSeleniumTests(StaticLiveServerTestCase):
    def test_LoginPage(self):
        ###This test just makes sure that it finds the username and password###
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        # Make address of HTML
        testingPath = self.live_server_url + "/pick_up_app/login"

        # Go to URL to test
        driver.get(testingPath)

        #test to find the username
        try:
            username = driver.find_element_by_id("id_teamname")
            username.send_keys("ThisIsTheUsername")
            print("SUCCESS, found html element ''username")
        except Exception:
            print("FAILED, could not get 'username' from HTML page")

        #test to find password
        try:
            password = driver.find_element_by_id("id_password")
            password.send_keys("ThisIsThePassword")
            print("SUCCESS, found html element ''password")
        except Exception:
            print("FAILED, could not get 'password' from HTML page")

        time.sleep(2)

    def test_RegisterRedirect(self):
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        testingPath = self.live_server_url + "/pick_up_app/login"

        registerButton = driver.find_element_by_class_name('newuser')
        registerButton.click()

        print("yay found redirect for register")

        driver.quit()

    def test_ForgotRedirect(self):
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        testingPath = self.live_server_url + "/pick_up_app/login"

        registerButton = driver.find_element_by_class_name('forgot')
        registerButton.click()

        print("Yay found the redirect for forgot pw")

        driver.quit()
"""

class registrationTests(TestCase):
    ###############################################################
    # Setup for registration
    ###############################################################
    def register_setup(self):
        t_password = "pass"
        t_check_pass = "pass"
        t_teamname = "test"
        t_email = "test@mail.com"
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


# Static Testing Server Test Class
class MySeleniumTests(StaticLiveServerTestCase):
    print("######################################################################")
    print("#                                                                    #")
    print("#                                                                    #")
    print("#                     Start of Selenium Tests                        #")
    print("#                                                                    #")
    print("#                                                                    #")
    print("######################################################################")


    #########################################################################
    # Test of home page map
    #########################################################################
    def test_HomePageMap(self):

        # Makes handler to FireFox
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        #Create Test User
        test_user = PickupTeam(teamname="ThisIsANewTeamName",
                               password="password",
                               email="testemail.email.com",
                               checkpassword="password",
                               longitude=22,
                               latitude=22)
        test_user.teamaccount = User.objects.create(username="ThisIsANewTeamName", password="password")

        test_user.save()

        # Make address of HTML
        try:
            driver.get(self.live_server_url + "/pick_up_app/login")
        except:
            print("FAILED, could not get '/pick_up_app/login'")

        time.sleep(2)

        # Path to test of where we should be naviagted to
        testingPath = self.live_server_url + "/pick_up_app/ThisIsANewTeamName/"

        # get login elements
        try:
            user_id = driver.find_element_by_class_name("user")
            user_id.send_keys("ThisIsANewTeamName")
            pass_id = driver.find_element_by_class_name("pass")
            pass_id.send_keys("password")
            time.sleep(2)

        except Exception:
            print("FAILED, could not find USER or PASSWORD element on login screen")

        try:
            driver.find_element_by_class_name("login").submit()
            time.sleep(2)
            print("SUCCESS, was able to navigate to a home page")

        except Exception:
            print("FAILED, could not navigate to home page")

        try:
            find_map = driver.find_element_by_id("googleMap")
            print("SUCCESS, found google map")
        except Exception:
            print("FAILED, could not find google map")

        driver.quit()

    #########################################################################
    # Test of "/register" page
    #########################################################################
    def test_RegisterPage(self):

        # Makes handler to FireFox
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        # Make address of HTML
        testingPath = self.live_server_url + "/pick_up_app/register"

        # Go to URL to test
        driver.get(testingPath)

        #########################################################################
        # Search for known form HTML 'id' attributes
        #########################################################################
        try:
            new_teamname = driver.find_element_by_id("id_teamname")
            new_teamname.send_keys("ThisIsANewTeamName")
            print("SUCCESS, found html element ''id_teamname")
        except Exception:
            print("FAILED, could not get 'id_teamname' from HTML page")

        try:
            new_email = driver.find_element_by_id("id_email")
            new_email.send_keys("ThisIsANewEmail@umbc.edu")
            print("SUCCESS, found html element ''id_email")
        except Exception:
            print("FAILED, could not get 'id_email' from HTML page")

        try:
            new_password = driver.find_element_by_id("id_password")
            new_password.send_keys("password")
            print("SUCCESS, found html element ''id_password")
        except Exception:
            print("FAILED, could not get 'id_password' from HTML page")

        try:
            new_checkpassword = driver.find_element_by_id("id_checkpassword")
            new_checkpassword.send_keys("password")
            print("SUCCESS, found html element ''id_checkpassword")
        except Exception:
            print("FAILED, could not get 'id_password' from HTML page")

        try:
            new_longitude = driver.find_element_by_id("id_longitude")
            print("SUCCESS, found html element ''id_longitude")

        except Exception:
            print("FAILED, could not get 'id_checkpassword' from HTML page")

        try:
            new_latitude = driver.find_element_by_id("id_latitude")
            print("SUCCESS, found html element ''id_latitude")
        except Exception:
            print("FAILED, could not get 'id_email' from HTML page")

        # Test for an ID that does not exists
        try:
            assert driver.find_element_by_id("id_lafftitude")
            print("FAILED, found invalid html element that should not exist on the page")
        except Exception:
            print("SUCCESS, failed to find invalid ID on '/pick_up_app/register' ")

        #########################################################################
        # End of HTML 'id' search tests
        #########################################################################

        #########################################################################
        # form submission
        #########################################################################
        time.sleep(2)
        try:
            button = driver.find_element_by_xpath("//button[text()='Register']")
            button.click()
            print("SUCCESS, submitted form")
        except Exception:
            print("FAILED, could not submit form")

        # Quick visual to see that form submitted
        time.sleep(2)


        #########################################################################
        # Redirect to '/login'
        # Redirect to 'main_site'
        #########################################################################

        # look for site links
        try:
            lnks = driver.find_elements_by_tag_name("a")
            print("SUCCESS, found following links on '/pick_up_app/register'")

            # for all links
            for lnk in lnks:
                print(lnk.get_attribute('href'))

        # failed to find site links
        except Exception:
            print("FAILED, could not find any 'href'")


        # tell handler to quit
        driver.quit()

        print("######################################################################")
        print("#                                                                    #")
        print("#                                                                    #")
        print("#                     End of Selenium Tests                          #")
        print("#                                                                    #")
        print("#                                                                    #")
        print("######################################################################")

