from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from webdriver_manager.firefox import GeckoDriverManager


# Create your tests here.

################################################
# Registration Tests
################################################
from pick_up_app.models import PickupTeam
from pick_up_app.forms import NewPickupUserForm
from pick_up_app.models import User


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


class HomePageHTMLTests(StaticLiveServerTestCase):
    def test_home_page_rendering(self):
        """
        This function tests that all the necessary objects are added to
        the home page.

        :return: None
        """

        # Setup Firefox web driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.implicitly_wait(0.5)
        driver.maximize_window()

        # Launch the team homepage URL
        driver.get(self.live_server_url + "/pick_up_app/home/")

        driver.implicitly_wait(0.5)  # Wait to find the title

        # Try to find all of the template items on the home page
        try:
            # Try to find all of the elements of the Top 5 Teams box
            driver.find_element_by_class_name("top_teams")
            driver.find_element_by_class_name("teams_label")
            driver.find_element_by_xpath('//table')

            # Try to find the map space
            driver.find_element_by_class_name("map_space")

            # Try to find the redirect buttons
            driver.find_element_by_class_name("redirect_button")
            driver.find_element_by_class_name("login_button")
            driver.find_element_by_class_name("team_button")
        # If any items not found, print fail message
        except Exception:
            print("FAILED, did not find all of the home page template items")

        # Check that home page title is correct
        home_title = "Team Home Page"  # The actual title of the home page
        self.assertEqual(home_title, driver.title)

        # Close browser
        driver.quit()


class RedirectLinkTests(StaticLiveServerTestCase):
    def test_redirect_home_to_login_page(self):
        """
        This function tests that a successful login will redirect the user to
        the home page by checking that the check view sends users to the page
        titled "Team Home Page"
        :return: None
        """

        # Add a new user
        new_user = User(username="lime", password="lemon", teamName="citrus")
        new_user.save()

        # Setup Firefox web driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.implicitly_wait(0.5)
        driver.maximize_window()

        # Open the login page URL
        driver.get(self.live_server_url + "/pick_up_app/login/")

        # Send the username and password to the login page and hit enter to redirect
        driver.find_element_by_xpath('//input[@class="user"][@type="username"]').send_keys("lime")
        driver.find_element_by_xpath('//input[@class="pass"][@type="password"]').send_keys("lemon")

        actual_title = "Team Home Page"  # What the actual title should be

        driver.find_element_by_xpath('//input[@class="login"][@type="submit"]').click()

        driver.implicitly_wait(0.5)  # Wait to find the link

        self.assertEqual(actual_title, driver.title)  # Title of redirected page should match

        # Close browser
        driver.quit()


    def test_redirect_login_to_home_page(self):
        """
        This function tests that the login page button on the home page. it
        will redirect the user to the login page by checking that the check
        view sends users to the page titled "Sign in"
        :return: None
        """

        # Setup Firefox web driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.implicitly_wait(0.5)
        driver.maximize_window()

        # Launch the team homepage URL
        driver.get(self.live_server_url + "/pick_up_app/home/")

        # Find the login page button and click it
        login_button = driver.find_element_by_xpath('//button[@type="button"][@class="login_button"]')
        login_button.click()

        actual_title = "Sign in"  # The actual title of the login page

        driver.implicitly_wait(0.5)  # Wait to find the title

        self.assertEqual(actual_title, driver.title)  # Title of redirected page should match

        # Close browser
        driver.quit()
