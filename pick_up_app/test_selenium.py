from atexit import register

from django.contrib.messages import get_messages
from django.test import TestCase
from django.test import LiveServerTestCase
from django.urls import reverse
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
from pick_up_app.models import User, Games
from pick_up_app.forms import NewUserForm

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

        test_user = User(teamname=t_teamname,
                               password=t_password,
                               email=t_email,
                               checkpassword=t_check_pass,
                               longitude=t_long,
                               latitude=t_lat)

        test_user.save()


    ###############################################################
    # Model testing for User
    ###############################################################
    def test_model_User(self):
        # Model Setup
        self.register_setup()

        # Known Teamname exists
        self.assertTrue(User.objects.filter(teamname="test").exists())

        # Known Teamname does not exists
        self.assertFalse(User.objects.filter(teamname="testbananasbananasasasfasfasf").exists())

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
        form_1 = NewUserForm(data=None)
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
        User.objects.filter(teamname="test").delete()


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
        test_user = User(teamname="ThisIsANewTeamName",
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

        time.sleep(1)

        # Path to test of where we should be naviagted to
        testingPath = self.live_server_url + "/pick_up_app/ThisIsANewTeamName/"

        # get login elements
        try:
            user_id = driver.find_element_by_class_name("user")
            user_id.send_keys("ThisIsANewTeamName")
            pass_id = driver.find_element_by_class_name("pass")
            pass_id.send_keys("password")
            time.sleep(1)

        except Exception:
            print("FAILED, could not find USER or PASSWORD element on login screen")

        try:
            driver.find_element_by_class_name("login").submit()
            time.sleep(1)
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
        time.sleep(1)
        try:
            button = driver.find_element_by_xpath("//button[text()='Register']")
            button.click()
            print("SUCCESS, submitted form")
        except Exception:
            print("FAILED, could not submit form")

        # Quick visual to see that form submitted
        time.sleep(1)


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


class HomePageHTMLTests(StaticLiveServerTestCase):
    def test_home_page_rendering(self):
        """
        This function tests that all the necessary objects are added to
        the home page.

        :return: None
        """

        # Add a new user
        new_user = User(username="lime", password="lemon", teamname="citrus")
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

        login_button = driver.find_element_by_class_name("login")
        login_button.click()

        driver.implicitly_wait(0.5)  # Wait to find the title

        # Try to find all the template items on the home page
        try:
            # Try to find all the elements of the Top 5 Teams box
            driver.find_element_by_class_name("top_teams")
            driver.find_element_by_class_name("teams_label")
            driver.find_element_by_xpath('//table')

            print("SUCCESS, found top 5 teams template items")
        except Exception:
            print("FAILED, did not find top 5 teams template items")

        try:
            # Try to find the map space
            driver.find_element_by_class_name("map_space")
            print("SUCCESS, found map space")
        except Exception:
            print("FAILED, did not find map space")

        try:
            # Try to find the redirect buttons
            driver.find_element_by_class_name("login_button")
            driver.find_element_by_class_name("team_button")

            print("SUCCESS, found redirect buttons")
        except Exception:
            print("FAILED, did not find redirect buttons")

        # Check that home page title is correct
        home_title = "Team Home Page"  # The actual title of the home page
        self.assertEqual(home_title, driver.title)

        # Close browser
        driver.quit()


class RedirectLinkTests(StaticLiveServerTestCase):
    def test_redirect_login_to_home_page(self):
        """
        This function tests that a successful login will redirect the user to
        the home page by checking that the 'check' view sends users to the page
        titled "Team Home Page"
        :return: None
        """

        # Add a new test user
        new_user = User(username="lime", password="lemon", teamname="citrus")
        new_user.save()

        # Setup Firefox web driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.implicitly_wait(0.5)
        driver.maximize_window()

        # Open the login page URL
        driver.get(self.live_server_url + "/pick_up_app/login/")

        # Send the username and password to the login page
        driver.find_element_by_xpath('//input[@class="user"][@type="username"]').send_keys("lime")
        driver.find_element_by_xpath('//input[@class="pass"][@type="password"]').send_keys("lemon")

        # Hit the enter/submit button to login and redirect
        driver.find_element_by_xpath('//input[@class="login"][@type="submit"]').click()

        driver.implicitly_wait(0.5)  # Wait before finding title

        curr_title = driver.title  # Gets the title of the current page
        actual_title = "Team Home Page"  # What the actual title should be

        self.assertEqual(actual_title, curr_title)  # Title of redirected page should match

        # Close browser
        driver.quit()


    def test_redirect_home_to_login_page(self):
        """
        This function tests the login page button on the home page. It will
        redirect the user to the login page by checking that the check view
        sends users to the page titled "Sign in"
        :return: None
        """

        # Add a new test user
        new_user = User(username="lime", password="lemon", teamname="citrus")
        new_user.save()

        # Setup Firefox web driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.implicitly_wait(0.5)
        driver.maximize_window()

        # Open the login page URL
        driver.get(self.live_server_url + "/pick_up_app/login/")

        # Login user
        driver.find_element_by_xpath('//input[@class="user"][@type="username"]').send_keys("lime")
        driver.find_element_by_xpath('//input[@class="pass"][@type="password"]').send_keys("lemon")
        driver.find_element_by_class_name("login").click()

        # Find and click the login button
        driver.find_element_by_class_name("login_button").click()

        driver.implicitly_wait(0.5)  # Wait before finding the title

        curr_title = driver.title  # Gets the title of the current page
        actual_title = "Sign in"  # The actual title of the login page

        self.assertEqual(actual_title, curr_title)  # Title of redirected page should match

        # Close browser
        driver.quit()


class NewGamePageTests(StaticLiveServerTestCase):
    def test_new_game_adds_to_database_successfully(self):
        """
        This function tests that a game added via the new_game page actually
        adds it to the database
        :return: None
        """

        # Add a new test user
        new_user = User(username="lime", password="lemon", teamname="citrus")
        new_user.save()

        # Setup Firefox web driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.implicitly_wait(0.5)
        driver.maximize_window()

        # Open the login page URL
        driver.get(self.live_server_url + "/pick_up_app/login/")

        # Login user so we can access new_game page
        driver.find_element_by_xpath('//input[@class="user"][@type="username"]').send_keys("lime")
        driver.find_element_by_xpath('//input[@class="pass"][@type="password"]').send_keys("lemon")
        driver.find_element_by_class_name("login").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Find and click the new game link
        driver.find_element_by_class_name("new_game_link").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Enter new game info
        driver.find_element_by_xpath('//input[@type="text"][@name="game_name"]').send_keys("yahtzee")
        driver.find_element_by_xpath('//input[@type="text"][@name="game_type"]').send_keys("dice")

        # Find and click the game submit button
        driver.find_element_by_class_name("game_button").click()

        driver.implicitly_wait(0.5)  # Wait before checking if game was added

        self.assertTrue(Games.objects.filter(game='yahtzee', gameType='dice'))

        # Close browser
        driver.quit()


    def test_new_game_trying_to_add_duplicate_game(self):
        """
        This function tests that a game already in the database will not be
        added again.
        :return: None
        """

        # Add a new test user
        new_user = User(username="lime", password="lemon", teamname="citrus")
        new_user.save()

        # Add a test game to test adding an existing game
        new_game = Games(game="poker", gameType="cards")
        new_game.save()

        # Setup Firefox web driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.implicitly_wait(0.5)
        driver.maximize_window()

        # Open the login page URL
        driver.get(self.live_server_url + "/pick_up_app/login/")

        # Login user so we can access new_game page
        driver.find_element_by_xpath('//input[@class="user"][@type="username"]').send_keys("lime")
        driver.find_element_by_xpath('//input[@class="pass"][@type="password"]').send_keys("lemon")
        driver.find_element_by_class_name("login").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Find and click the new game link
        driver.find_element_by_class_name("new_game_link").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Enter new game info
        driver.find_element_by_xpath('//input[@type="text"][@name="game_name"]').send_keys("poker")
        driver.find_element_by_xpath('//input[@type="text"][@name="game_type"]').send_keys("cards")

        # Find and click the game submit button
        driver.find_element_by_class_name("game_button").click()
        time.sleep(2)

        driver.implicitly_wait(0.5)  # Wait before checking the game message

        # Get error message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="error"]')
        expected_message = "Game could not be added."
        message_text = ""  # Primes variable for the message (if one exists)
        for message in messages_found:
            message_text = message.text

        # Compare error message (if any) to the expected message string
        self.assertTrue(message_text == expected_message)

        # Close browser
        driver.quit()


class EditTeamPageTests(StaticLiveServerTestCase):
    def test_team_changes_made_successfully(self):
        """
        This function tests that changes to team info via the edit team page
        are added are made successfully.
        :return: None
        """

        # Add a new test user
        new_user = User(username="tim", teamname="timtom", password="tommy",
                        checkpassword="tommy", email="tim@gmail.com")
        new_user.save()

        # List of expected success messages
        expected_messages = ["Username changed successfully.",
                             "Team name changed successfully.",
                             "Password changed successfully.",
                             "Team email changed successfully."]


        # Setup Firefox web driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.implicitly_wait(0.5)
        driver.maximize_window()

        # Open the login page URL
        driver.get(self.live_server_url + "/pick_up_app/login/")

        # Login user so we can access new_game page
        driver.find_element_by_xpath('//input[@class="user"][@type="username"]').send_keys("tim")
        driver.find_element_by_xpath('//input[@class="pass"][@type="password"]').send_keys("tommy")
        driver.find_element_by_class_name("login").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Open the edit_team URL
        driver.get(self.live_server_url + reverse('edit_team', kwargs={'username': 'tim'}))

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Enter new user info to be changed
        driver.find_element_by_xpath('//input[@type="text"][@name="new_username"]').send_keys("lime")
        driver.find_element_by_xpath('//input[@type="text"][@name="new_team_name"]').send_keys("limeade")
        driver.find_element_by_xpath('//input[@type="text"][@name="new_password"]').send_keys("lemon")
        driver.find_element_by_xpath('//input[@type="text"][@name="confirm_password"]').send_keys("lemon")
        driver.find_element_by_xpath('//input[@type="text"][@name="new_email"]').send_keys("lime@gmail.com")

        # Find and click the save changes button
        driver.find_element_by_class_name("my_save_button").click()

        driver.implicitly_wait(0.5)  # Wait before checking that team info was updated
        # Get success messages and check with expected
        messages_found = driver.find_elements_by_xpath('//p[@class="success"]')
        message_text = ""  # Primes variable for the message (if one exists)
        for i in range(len(messages_found)):
            message_text = messages_found[i].text
            # Compare messages (if any) to the expected message string
            self.assertTrue(message_text == expected_messages[i])


        # Close browser
        driver.quit()

    def test_team_changes_made_individually_are_successful(self):
        """
        This function tests that changes to team info made separately via
        the edit team page are added are made successfully.
        :return: None
        """

        # Add a new test user
        new_user = User(username="tim", teamname="timtom", password="tommy",
                        checkpassword="tommy", email="tim@gmail.com")
        new_user.save()

        # List of expected success messages
        expected_messages = ["Username changed successfully.",
                             "Team name changed successfully.",
                             "Password changed successfully.",
                             "Team email changed successfully.", ]

        # Setup Firefox web driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.implicitly_wait(0.5)
        driver.maximize_window()

        # Open the login page URL
        driver.get(self.live_server_url + "/pick_up_app/login/")

        # Login user so we can access new_game page
        driver.find_element_by_xpath('//input[@class="user"][@type="username"]').send_keys("tim")
        driver.find_element_by_xpath('//input[@class="pass"][@type="password"]').send_keys("tommy")
        driver.find_element_by_class_name("login").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Open the login page URL
        driver.get(self.live_server_url + reverse('edit_team', kwargs={'username': 'tim'}))

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Enter new username info and save changes
        driver.find_element_by_xpath('//input[@type="text"][@name="new_username"]').send_keys("lime")
        driver.find_element_by_class_name("my_save_button").click()

        # Wait before confirming that username was changed
        driver.implicitly_wait(0.5)
        # Get success message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="success"]')
        message_text = ""  # Clears message_text for next message
        for message in messages_found:
            message_text = message.text
        # Compare message (if any) to the expected message string
        self.assertTrue(message_text == expected_messages[0])

        # Enter new team name info and save changes
        driver.find_element_by_xpath('//input[@type="text"][@name="new_team_name"]').send_keys("limeade")
        driver.find_element_by_class_name("my_save_button").click()

        # Wait before confirming that team name was changed
        driver.implicitly_wait(0.5)
        # Get success message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="success"]')
        message_text = ""  # Clears message_text for next message
        for message in messages_found:
            message_text = message.text
        # Compare message (if any) to the expected message string
        self.assertTrue(message_text == expected_messages[1])

        # Enter password and confirm password and save changes
        driver.find_element_by_xpath('//input[@type="text"][@name="new_password"]').send_keys("lemon")
        driver.find_element_by_xpath('//input[@type="text"][@name="confirm_password"]').send_keys("lemon")
        driver.find_element_by_class_name("my_save_button").click()

        # Wait before confirming that password(s) changed
        driver.implicitly_wait(0.5)
        # Get success message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="success"]')
        message_text = ""  # Clears message_text for next message
        for message in messages_found:
            message_text = message.text
        # Compare message (if any) to the expected message string
        self.assertTrue(message_text == expected_messages[2])
        #
        # # Wait before proceeding
        # driver.implicitly_wait(0.5)
        #
        # driver.find_element_by_xpath('//input[@type="text"][@name="new_email"]').send_keys("lime@gmail.com")
        # driver.find_element_by_class_name("my_save_button").click()
        #
        # time.sleep(2)
        # # Wait before confirming that email was changed
        # driver.implicitly_wait(0.5)
        # # Get success message from messages
        # messages_found = driver.find_elements_by_xpath('//p[@class="success"]')
        # message_text = ""  # Clears message_text for next message
        # for message in messages_found:
        #     message_text = message.text
        # # Compare message (if any) to the expected message string
        # print(message_text)
        # self.assertTrue(message_text == expected_messages[3])

        # Close browser
        driver.quit()


    def test_duplicate_info_given_handled_correctly(self):
        """
        This function tests that changes to team info made with separate forms
         via the edit team page are added are made successfully.
        :return: None
        """

        # Add a new test user
        new_user = User(username="tim", teamname="timtom", password="tommy",
                        checkpassword="tommy", email="tim@gmail.com")
        new_user.save()

        # Expected messages for submitting duplicate data
        expected_message_1 = "The username given is already this team's username."
        expected_message_2 = "The team name given is already this team's team name."
        expected_message_3 = "The password given is already this team's password."
        expected_message_4 = "The email given is already this team's email."

        # Setup Firefox web driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.implicitly_wait(0.5)
        driver.maximize_window()

        # Open the login page URL
        driver.get(self.live_server_url + "/pick_up_app/login/")

        # Login user so we can access new_game page
        driver.find_element_by_xpath('//input[@class="user"][@type="username"]').send_keys("tim")
        driver.find_element_by_xpath('//input[@class="pass"][@type="password"]').send_keys("tommy")
        driver.find_element_by_class_name("login").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Open the login page URL
        driver.get(self.live_server_url + reverse('edit_team', kwargs={'username': 'tim'}))

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Enter same username info and save changes
        driver.find_element_by_xpath('//input[@type="text"][@name="new_username"]').send_keys("tim")
        driver.find_element_by_class_name("my_save_button").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Get error message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="error"]')
        message_text = ""  # Primes variable for the message (if one exists)
        for message in messages_found:
            message_text = message.text
        # Compare error message (if any) to the expected message string
        self.assertTrue(message_text == expected_message_1)

        # Enter same team name info and save changes
        driver.find_element_by_xpath('//input[@type="text"][@name="new_team_name"]').send_keys("timtom")
        driver.find_element_by_class_name("my_save_button").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Get error message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="error"]')
        message_text = ""  # Reset message text to empty
        for message in messages_found:
            message_text = message.text
        # Compare error message (if any) to the expected message string
        self.assertTrue(message_text == expected_message_2)

        # Enter same password and confirm password and save changes
        driver.find_element_by_xpath('//input[@type="text"][@name="new_password"]').send_keys("tommy")
        driver.find_element_by_xpath('//input[@type="text"][@name="confirm_password"]').send_keys("tommy")
        driver.find_element_by_class_name("my_save_button").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Get error message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="error"]')
        message_text = ""  # Reset message text to empty
        for message in messages_found:
            message_text = message.text
        # Compare error message (if any) to the expected message string
        self.assertTrue(message_text == expected_message_3)

        # Enter same email address
        driver.find_element_by_xpath('//input[@type="text"][@name="new_email"]').send_keys("tim@gmail.com")
        driver.find_element_by_class_name("my_save_button").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Get error message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="error"]')
        message_text = ""  # Reset message text to empty
        for message in messages_found:
            message_text = message.text
        # Compare error message (if any) to the expected message string
        self.assertTrue(message_text == expected_message_4)

        # Close browser
        driver.quit()
