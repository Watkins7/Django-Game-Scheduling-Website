from django.test import TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
import time
import datetime
from django.utils import timezone
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

################################################
# Registration Tests
################################################
from pick_up_app.models import User, TimeSlot, Games
from pick_up_app.forms import NewUserForm, NewGameForm

print("\n\n######################################################################")
print("#                                                                    #")
print("#                                                                    #")
print("#                     Start of Selenium Tests                        #")
print("#                                                                    #")
print("#                                                                    #")
print("######################################################################")



class registrationTests(TestCase):

    ###############################################################
    # Setup for registration
    ###############################################################
    def register_setup(self):
        t_password = "pass"
        t_check_pass = "pass"
        t_username = "test"
        t_email = "test@mail.com"
        t_long = 7
        t_lat = 13

        test_user = User(username=t_username,
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

        # Known username exists
        self.assertTrue(User.objects.filter(username="test").exists())

        # Known Teamname does not exists
        self.assertFalse(User.objects.filter(username="testbananasbananasasasfasfasf").exists())

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
        form_1.fields["username"] = "test"
        self.assertFalse(form_1.is_valid())

        form_1.fields["username"] = "test_nottaken"

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
        User.objects.filter(username="test").delete()


# Static Testing Server Test Class
class MySeleniumTests(StaticLiveServerTestCase):

    #########################################################################
    # Test of home page map
    #########################################################################
    def test_HomePageMap(self):

        print("\n######################################################################")
        print("#                     Home Page Selenium Test                        #")
        print("######################################################################")

        # Makes handler to FireFox
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        #Create Test User
        test_user = User(username="nuck", teamname="ThisIsANewTeamName",
                               password="password",
                               email="testemail.email.com",
                               checkpassword="password",
                               longitude=22,
                               latitude=22)
        test_user.save()

        # Make address of HTML
        try:
            driver.get(self.live_server_url + "/pick_up_app/login")
        except:
            print("FAILED, could not get '/pick_up_app/login'")

        time.sleep(3)

        # Path to test of where we should be naviagted to
        testingPath = self.live_server_url + "/pick_up_app/ThisIsANewTeamName/"

        # get login elements
        try:
            user_id = driver.find_element_by_class_name("user")
            user_id.send_keys("nuck")
            pass_id = driver.find_element_by_class_name("pass")
            pass_id.send_keys("password")
            time.sleep(3)

        except Exception:
            print("FAILED, could not find USER or PASSWORD element on login screen")

        try:
            login_button = driver.find_element_by_class_name("login")
            login_button.click()
            #driver.find_element_by_class_name("login").submit()
            time.sleep(3)
            print("SUCCESS, was able to navigate to a home page")

        except Exception:
            print("FAILED, could not navigate to home page")

        try:
            driver.implicitly_wait(2)
            find_map = driver.find_element_by_id("googleMap")
            print("SUCCESS, found google map")
        except Exception as e:
            print("FAILED, could not find google map")
            print(e)

        driver.quit()

    #########################################################################
    # Test of "/register" page
    #########################################################################
    def test_RegisterPage(self):

        print("\n######################################################################")
        print("#                     Register Page Selenium Test                    #")
        print("######################################################################")

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
            new_username = driver.find_element_by_id("id_username")
            new_username.send_keys("newUsername")
            print("SUCCESS, found html element ''id_teamname")
        except Exception:
            print("FAILED, could not get 'id_teamname' from HTML page")
        try:
            new_username = driver.find_element_by_id("id_username")
            new_username.send_keys("ThisIsANewTeamName")
            print("SUCCESS, found html element ''id_username")
        except Exception:
            print("FAILED, could not get 'id_username' from HTML page")

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

class loginSeleniumTests(StaticLiveServerTestCase):
    def test_LoginPage(self):
        ###This test just makes sure that it finds the username and password###
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        # Make address of HTML
        testingPath = self.live_server_url + "/pick_up_app/login"

        # Go to URL to test
        driver.get(testingPath)

        #make new user
        new_user = User(username="user", password="pw", teamname="team")
        new_user.save()

        driver.find_element_by_xpath('//input[@class="user"][@type="username"]').send_keys("user")
        driver.find_element_by_xpath('//input[@class="pass"][@type="password"]').send_keys("pw")

        try:
            driver.find_element_by_class_name("main")
            driver.find_element_by_class_name("user")
            driver.find_element_by_class_name("pass")
            driver.find_element_by_class_name("login")
            print("SUCCESS, found the classes")
        except Exception:
            print("FAILED, couldn't find the classes")

    def test_RegisterRedirect(self):
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        testingPath = self.live_server_url + "/pick_up_app/login"
        try:
            # Try to find the redirect buttons
            driver.find_element_by_class_name("newuser")
            print("SUCCESS, found new user redirect button")
        except Exception:
            print("FAILED, did not find user redirect button")

        driver.quit()

    def test_ForgotRedirect(self):
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        testingPath = self.live_server_url + "/pick_up_app/login"
        try:
            # Try to find the redirect buttons
            driver.find_element_by_class_name("forgot")
            print("SUCCESS, found forgot user redirect buttons")
        except Exception:
            print("FAILED, did not find forgot user redirect buttons")

        driver.quit()


class HomePageHTMLTests(StaticLiveServerTestCase):
    def test_main_page_rendering(self):

        print("\n######################################################################")
        print("#                     Main Page Rendering Selenium Test              #")
        print("######################################################################")

        # Makes handler to FireFox
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        # Make address of HTML
        testingPath = self.live_server_url

        driver.get(testingPath)
        time.sleep(1)

        # Find the heading
        try:
            driver.find_element_by_class_name("heading")
        except Exception as E:
            driver.quit()
            self.fail(E)

        # Find the the main box
        try:
            driver.find_element_by_class_name("main")
        except Exception as E:
            driver.quit()
            self.fail(E)

        # find the about us box
        try:
            driver.find_element_by_class_name("box")
        except Exception as E:
            driver.quit()
            self.fail(E)

        # find all the images
        try:
            images = driver.find_elements_by_tag_name('img')
        except Exception as E:
            driver.quit()
            self.fail(E)

        # count to make sure that the number of images is 5
        count = 0
        for image in images:
            print("Image", count, ":", image.get_attribute('src'))
            count+=1

        if count != 6:
            driver.quit()
            self.fail("FAILED, Number of images on the page is not correct")

        print("All tested in HOME page passed")
        driver.quit()



class SecondHomePageHTMLTests(StaticLiveServerTestCase):
    def second_test_home_page_rendering(self):
        """
        This function tests that all the necessary objects are added to
        the home page.

        :return: None
        """
        print("\n######################################################################")
        print("#                     Home Page Rendering Selenium Test              #")
        print("######################################################################")

        # Add a new user
        new_user = User(username="lime", password="lemon")
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

        print("\n######################################################################")
        print("#                     Redirect Login to Home Selenium Test           #")
        print("######################################################################")

        # Add a new test user
        new_user = User(username="lime", password="lemon")
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

        print("\n######################################################################")
        print("#                     Home to Login Redirection  Selenium Test       #")
        print("######################################################################")

        # Add a new test user
        new_user = User(username="lime", password="lemon")
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

        driver.implicitly_wait(2)  # Wait before finding the title

        curr_title = driver.title  # Gets the title of the current page
        actual_title = "Sign in"  # The actual title of the login page

        self.assertEqual(actual_title, curr_title)  # Title of redirected page should match

        # Close browser
        driver.quit()


    def test_redirect_home_to_team_page(self):
        """
        This function tests the team page button on the home page. It will
        redirect the user to their team page by checking that the button
        sends users to the page titled "Team Page"
        :return: None
        """

        # Add a new test user
        new_user = User(username="lime", password="lemon")
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

        # Find and click the team page button
        driver.find_element_by_class_name("team_button").click()

        driver.implicitly_wait(2)  # Wait before finding the title

        curr_title = driver.title  # Gets the title of the current page
        actual_title = "Team Page"  # The actual title of the login page

        self.assertEqual(actual_title, curr_title)  # Title of redirected page should match

        # Close browser
        driver.quit()


    def test_redirect_team_to_home_page(self):
        """
        This function tests the team page button on the home page. It will
        redirect the user to their home page by checking that the button
        sends users to the page titled "Team Home Page"
        :return: None
        """

        # Add a new test user
        new_user = User(username="lime", password="lemon")
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

        # Redirect to the team page
        driver.get(self.live_server_url + reverse('team_page', kwargs={'username': 'lime'}))

        # Find and click the home page link
        driver.find_element_by_class_name("home_page").click()

        driver.implicitly_wait(2)  # Wait before finding the title

        curr_title = driver.title  # Gets the title of the current page
        actual_title = "Team Home Page"  # The actual title of the login page

        self.assertEqual(actual_title, curr_title)  # Title of redirected page should match

        # Close browser
        driver.quit()


    def test_redirect_team_to_edit_team_page(self):
        """
        This function tests the edit team page button on the team page. It will
        redirect the user to their edit team page by checking that the link
        sends users to the page titled "Edit Team Info"
        :return: None
        """

        # Add a new test user
        new_user = User(username="lime", password="lemon")
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

        # Go to the team_page then find and click the edit_team link
        driver.get(self.live_server_url + reverse('team_page', kwargs={'username': 'lime'}))
        driver.find_element_by_class_name("edit_team_page").click()

        driver.implicitly_wait(2)  # Wait before finding the title

        curr_title = driver.title  # Gets the title of the current page
        actual_title = "Edit Team Info"  # The actual title of the login page

        self.assertEqual(actual_title, curr_title)  # Title of redirected page should match

        # Close browser
        driver.quit()


    def test_redirect_edit_team_to_team_page(self):
        """
        This function tests the "Back to Team Page" button on the edit team
        page. It will redirect the user to their team page by checking that
        the button sends users to the page titled "Team Page"
        :return: None
        """

        # Add a new test user
        new_user = User(username="lime", password="lemon")
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

        # Redirect to the edit_team page
        driver.get(self.live_server_url + reverse('edit_team', kwargs={'username': 'lime'}))

        # Find and click the redirect to team page button
        driver.find_element_by_class_name("redirect_btn").click()

        driver.implicitly_wait(2)  # Wait before finding the title

        curr_title = driver.title  # Gets the title of the current page
        actual_title = "Team Page"  # The actual title of the login page

        self.assertEqual(actual_title, curr_title)  # Title of redirected page should match

        # Close browser
        driver.quit()


    def test_duplicate_info_given_handled_correctly(self):
        """
        This function tests that changes to team info made with separate forms
         via the edit team page are added are made successfully.
        :return: None
        """

        # Add a new test user
        new_user = User(username="tim", teamname="timtom", password="tommy", checkpassword="tommy",
                        email="tim@gmail.com", longitude=-76.71, latitude=39.2543)
        new_user.save()

        # Expected messages for submitting duplicate data
        expected_message = ["ERROR: The username given is already this team's username.",
                            "ERROR: The team name given is already this team's team name.",
                            "ERROR: The password given is already this team's password.",
                            "ERROR: The email given is already this team's email.",
                            "ERROR: The longitude given is already this team's longitude coordinate.",
                            "ERROR: The latitude given is already this team's latitude coordinate.",
                            ]

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
        self.assertTrue(message_text == expected_message[0])

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
        self.assertTrue(message_text == expected_message[1])

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
        self.assertTrue(message_text == expected_message[2])

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
        self.assertTrue(message_text == expected_message[3])

        # Enter same longitude
        driver.find_element_by_xpath('//input[@type="text"][@name="new_longitude"]').send_keys("-76.71")
        driver.find_element_by_class_name("my_save_button").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Get error message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="error"]')
        message_text = ""  # Reset message text to empty
        for message in messages_found:
            message_text = message.text
        # Compare error message (if any) to the expected message string
        self.assertTrue(message_text == expected_message[4])

        # Enter same latitude
        driver.find_element_by_xpath('//input[@type="text"][@name="new_latitude"]').send_keys("39.2543")
        driver.find_element_by_class_name("my_save_button").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Get error message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="error"]')
        message_text = ""  # Reset message text to empty
        for message in messages_found:
            message_text = message.text
        # Compare error message (if any) to the expected message string
        self.assertTrue(message_text == expected_message[5])

        # Close browser
        driver.quit()


    def test_check_latitude_and_longitude_range(self):
        """
        This function tests that attempts to change latitude and longitude that are
        outside the desired range are not changed.
        :return: None
        """

        # Add a new test user
        new_user = User(username="tim", teamname="timtom", password="tommy", checkpassword="tommy",
                        email="tim@gmail.com", longitude=-76.71, latitude=39.2543)
        new_user.save()

        # Expected messages for submitting duplicate data
        expected_message = ["ERROR: Longitude must be within -180 to 180",
                            "ERROR: Latitude must be within -90 to 90",
                            ]

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

        # Enter longitude < -180
        driver.find_element_by_xpath('//input[@type="text"][@name="new_longitude"]').send_keys("-200")
        driver.find_element_by_class_name("my_save_button").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Get error message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="error"]')
        message_text = ""  # Reset message text to empty
        for message in messages_found:
            message_text = message.text
        # Compare error message (if any) to the expected message string
        self.assertTrue(message_text == expected_message[0])

        # Enter longitude > 180
        driver.find_element_by_xpath('//input[@type="text"][@name="new_longitude"]').send_keys("200")
        driver.find_element_by_class_name("my_save_button").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Get error message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="error"]')
        message_text = ""  # Reset message text to empty
        for message in messages_found:
            message_text = message.text
        # Compare error message (if any) to the expected message string
        self.assertTrue(message_text == expected_message[0])

        # Enter latitude < -90
        driver.find_element_by_xpath('//input[@type="text"][@name="new_latitude"]').send_keys("-100")
        driver.find_element_by_class_name("my_save_button").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Get error message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="error"]')
        message_text = ""  # Reset message text to empty
        for message in messages_found:
            message_text = message.text
        # Compare error message (if any) to the expected message string
        self.assertTrue(message_text == expected_message[1])

        # Enter latitude > 90
        driver.find_element_by_xpath('//input[@type="text"][@name="new_latitude"]').send_keys("100")
        driver.find_element_by_class_name("my_save_button").click()

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Get error message from messages
        messages_found = driver.find_elements_by_xpath('//p[@class="error"]')
        message_text = ""  # Reset message text to empty
        for message in messages_found:
            message_text = message.text
        # Compare error message (if any) to the expected message string
        self.assertTrue(message_text == expected_message[1])

        driver.implicitly_wait(0.5)  # Wait before proceeding

        # Close browser
        driver.quit()
