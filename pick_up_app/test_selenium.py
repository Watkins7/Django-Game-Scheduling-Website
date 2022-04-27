from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
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
            username = driver.find_element_by_id("id_username")
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

        # Known Teamname exists
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

        print("######################################################################")
        print("#                     Home Page Selenium Test                        #")
        print("######################################################################")

        # Makes handler to FireFox
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        #Create Test User
        new_user = User(username="lime", password="lemon",
                        latitude=-76.71, longitude=39.2543)
        new_user.save()

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
            user_id.send_keys("lime")
            pass_id = driver.find_element_by_class_name("pass")
            pass_id.send_keys("lemon")
            time.sleep(3)

        except Exception:
            print("FAILED, could not find USER or PASSWORD element on login screen")

        try:
            driver.find_element_by_class_name("login").submit()
            time.sleep(3)
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

        print("######################################################################")
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

# Tests mainpage
class HomePageHTMLTests(StaticLiveServerTestCase):
    def test_main_page_rendering(self):

        print("######################################################################")
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
            print(E)
            return -1

        # Find the the main box
        try:
            driver.find_element_by_class_name("main")
        except Exception as E:
            print(E)
            return -1

        # find the about us box
        try:
            driver.find_element_by_class_name("box")
        except Exception as E:
            print(E)
            return -1

        # find all the images
        try:
            images = driver.find_elements_by_tag_name('img')
        except Exception as E:
            print(E)
            return -1

        # count to make sure that the number of images is 5
        count = 0
        for image in images:
            print("Image", count, ":", image.get_attribute('src'))
            count+=1

        if count != 5:
            print("FAILED, Number of images on the page is not correct")
            return -1

        driver.quit()



class SecondHomePageHTMLTests(StaticLiveServerTestCase):
    def second_test_home_page_rendering(self):

        print("######################################################################")
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

        print("######################################################################")
        print("#                     Redirect Login to Home Selenium Test            #")
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

        print("######################################################################")
        print("#                     Home to Login Redirection  Selenium Test       #")
        print("######################################################################")

        # Add a new tes user
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

        driver.implicitly_wait(0.5)  # Wait before finding the title

        curr_title = driver.title  # Gets the title of the current page
        actual_title = "Sign in"  # The actual title of the login page

        self.assertEqual(actual_title, curr_title)  # Title of redirected page should match

        # Close browser
        driver.quit()


# Set of selenium tests for the Calendar Page
class CalendarHTMLTests(StaticLiveServerTestCase):

    # Tests that all elements on the calendar page are properly rendered when loaded
    def test_calendar_rendering(self):

        print("\n######################################################################")
        print("#                     Calendar Rendering Selenium Test                 #")
        print("########################################################################")

        # Creates two users & respective timeslots to be tested
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        test_team = "test"
        test_team2 = "test2"


        test_user = User(username="test", password="pass")
        test_user2 = User(username="test2", password="pass2")
        test_user.save()
        test_user2.save()

        test_game = Games(game="newgame", gameType="testing")
        test_game.save()

        test_timeslot = TimeSlot(team=test_user,
                                 game=test_game,
                                 slot_start=timezone.now() + datetime.timedelta(minutes=1),
                                 slot_end=timezone.now() + datetime.timedelta(minutes=30))
        test_timeslot2 = TimeSlot(team=test_user2,
                                  game=test_game,
                                  slot_start=timezone.now() + datetime.timedelta(minutes=1),
                                  slot_end=timezone.now() + datetime.timedelta(minutes=30))
        test_timeslot.save()
        test_timeslot2.save()

        # Performs Log-in for the first test user
        driver.get(self.live_server_url + "/pick_up_app/login/")
        driver.find_element(by=By.XPATH, value='//input[@class="user"][@type="username"]').send_keys("test")
        driver.find_element(by=By.XPATH, value='//input[@class="pass"][@type="password"]').send_keys("pass")
        login_button = driver.find_element(by=By.CLASS_NAME, value="login")
        login_button.click()
        driver.implicitly_wait(0.5)
        driver.get(self.live_server_url + "/pick_up_app/calendar/" + test_team)

        # Try to find all the button elements which should be on the first test user's calendar
        try:
            driver.find_element(by=By.CLASS_NAME, value="previous_month_btn")
            driver.find_element(by=By.CLASS_NAME, value="new_timeslot_btn")
            driver.find_element(by=By.CLASS_NAME, value="next_month_btn")
            driver.find_element(by=By.CLASS_NAME, value="home_btn")
            print("SUCCESS, found logged-in user's redirection buttons")
        except Exception:
            print("FAILED, did not find logged-in user's redirection buttons")

        # Try to find the first test user's calendar element
        try:
            driver.find_element(by=By.CLASS_NAME, value="calendar")
            print("SUCCESS, found logged-in user's calendar")
        except Exception:
            print("FAILED, did not find logged-in user's calendar")

        # Try to find a listed timeslot on the first test user's calendar
        try:
            driver.find_element(by=By.CLASS_NAME, value="listed_timeslot")
            print("SUCCESS, found logged-in user's timeslot")
        except Exception:
            print("FAILED, did not find logged-in user's timeslot")

        # Redirect to the other team's calendar while logged in as the first test user
        driver.get(self.live_server_url + "/pick_up_app/calendar/" + test_team2)

        # Try to find new timeslot button while viewing another team's calendar
        try:
            driver.find_element(by=By.CLASS_NAME, value="new_timeslot_btn")
            print("FAILED, found new timeslot button while viewing another team's calendar")
        except Exception:
            print("SUCCESS, did not find new timeslot button while viewing another team's calendar")

        # Try to find a listed timeslot while viewing the second test user's calendar
        try:
            driver.find_element(by=By.CLASS_NAME, value="listed_timeslot")
            print("SUCCESS, found timeslot while viewing another team's calendar")
        except Exception:
            print("FAILED, did not find timeslot while viewing another team's calendar")

        driver.quit()

    # Tests the redirect links on the calendar work as intended
    def test_calendar_redirection(self):

        print("\n######################################################################")
        print("#                     Calendar Redirection Selenium Test             #")
        print("######################################################################")

        # Performs user log-in to be used by other tests
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        test_team = "test"

        test_user = User(username="test", password="pass")
        test_user.save()

        test_game = Games(game="newgame", gameType="testing")
        test_game.save()

        test_timeslot = TimeSlot(team=test_user,
                                 game=test_game,
                                 slot_start=timezone.now() + datetime.timedelta(minutes=1),
                                 slot_end=timezone.now() + datetime.timedelta(minutes=30))
        test_timeslot.save()

        # Performs Log-in for the first test user
        driver.get(self.live_server_url + "/pick_up_app/login/")
        driver.find_element(by=By.XPATH, value='//input[@class="user"][@type="username"]').send_keys("test")
        driver.find_element(by=By.XPATH, value='//input[@class="pass"][@type="password"]').send_keys("pass")
        login_button = driver.find_element(by=By.CLASS_NAME, value="login")
        login_button.click()
        driver.implicitly_wait(0.5)
        driver.get(self.live_server_url + "/pick_up_app/calendar/" + test_team)

        # Tests redirection from the Calendar page to the Home Page using the home button
        driver.find_element(by=By.CLASS_NAME, value="home_btn").click()
        cur_title = driver.title
        actual_title = "Team Home Page"
        self.assertEqual(actual_title, cur_title)

        # Tests redirection from the Calendar page to the Timeslot page using the new timeslot button
        driver.get(self.live_server_url + "/pick_up_app/calendar/" + test_team)
        driver.find_element(by=By.CLASS_NAME, value="new_timeslot_btn").click()
        driver.implicitly_wait(0.5)
        cur_title = driver.title
        actual_title = "Timeslot Page"
        self.assertEqual(actual_title, cur_title)

        # Tests redirection from the Calendar page to a future month using the next month button
        driver.get(self.live_server_url + "/pick_up_app/calendar/" + test_team)
        driver.find_element(by=By.CLASS_NAME, value="next_month_btn").click()
        cur_url = driver.current_url
        actual_url = self.live_server_url+"/pick_up_app/calendar/"+test_team
        actual_url += "/?month="+str(timezone.now().year)+"-"+str(timezone.now().month + 1)
        self.assertEqual(cur_url, actual_url)

        # Tests redirection from the Calendar page to a previous month using the previous month button
        driver.find_element(by=By.CLASS_NAME, value="previous_month_btn").click()
        cur_url = driver.current_url
        actual_url = self.live_server_url + "/pick_up_app/calendar/" + test_team
        actual_url += "/?month=" + str(timezone.now().year) + "-" + str(timezone.now().month)
        self.assertEqual(cur_url, actual_url)

        driver.quit()


# Set of Selenium tests for the Timeslot Page
class TimeslotHTMLTests(StaticLiveServerTestCase):
    # Tests a new timeslot can be added and removed from the calendar
    def test_timeslot_submission(self):

        print("######################################################################")
        print("#                     Timeslot Selenium Test                         #")
        print("######################################################################")

        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        cur_time = timezone.now().date() + datetime.timedelta(days=1)
        test_time = str(cur_time.month)+str(cur_time.day)+str(cur_time.year)
        test_team = "test"
        test_user = User(username="test", password="pass")
        test_game = Games(game="newgame", gameType="testing")
        test_game.save()
        test_user.save()

        # Performs Log-in for the first test user
        driver.get(self.live_server_url + "/pick_up_app/login/")
        driver.find_element(by=By.XPATH, value='//input[@class="user"][@type="username"]').send_keys("test")
        driver.find_element(by=By.XPATH, value='//input[@class="pass"][@type="password"]').send_keys("pass")
        login_button = driver.find_element(by=By.CLASS_NAME, value="login")
        login_button.click()
        driver.implicitly_wait(0.5)
        driver.get(self.live_server_url + "/pick_up_app/timeslot/new/" + test_team)

        # Try to find submission location for game choice
        try:
            select_element = driver.find_element(by=By.ID, value="id_game")
            select_object = Select(select_element)
            select_object.select_by_index(1)
            print("SUCCESS, found element id_game")
        except Exception:
            print("FAILED, could not find element id_game")

        # Try to find submission location for start of a timeslot
        try:
            driver.find_element(by=By.ID, value="id_slot_start").send_keys(test_time)
            driver.find_element(by=By.ID, value="id_slot_start").send_keys(Keys.TAB)
            driver.find_element(by=By.ID, value="id_slot_start").send_keys("0245PM")
            print("SUCCESS, found element id_slot_start")
        except Exception:
            print("FAILED, could not find element id_slot_start")

        # Try to find submission location for end of a timeslot
        try:
            driver.find_element(by=By.ID, value="id_slot_end").send_keys(test_time)
            driver.find_element(by=By.ID, value="id_slot_end").send_keys(Keys.TAB)
            driver.find_element(by=By.ID, value="id_slot_end").send_keys("0345PM")
            print("SUCCESS, found element id_slot_end")
        except Exception:
            print("FAILED, could not find element id_slot_end")

        # Try to submit the newly created timeslot
        try:
            driver.find_element(by=By.NAME, value="add").click()
            driver.implicitly_wait(0.5)
            print("SUCCESS, submitted timeslot form")
        except Exception:
            print("FAILED, could not submit timeslot form")

        # Tests the submission button redirects from the Timeslot Page to the Calendar Page
        cur_title = driver.title
        actual_title = test_team + " Team Calendar"
        self.assertEqual(actual_title, cur_title)

        # Try to delete the newly created timeslot
        driver.find_element(by=By.CLASS_NAME, value="listed_timeslot").click()
        try:
            driver.find_element(by=By.NAME, value="delete").click()
            print("SUCCESS, deleted timeslot")
        except Exception:
            print("FAILED, could not delete timeslot")

        driver.quit()

    def test_timeslot_redirection(self):

        print("######################################################################")
        print("#                     Time Slot Redirection Selenium Test            #")
        print("######################################################################")

        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        cur_time = timezone.now().date() + datetime.timedelta(days=1)
        test_time = str(cur_time.month) + str(cur_time.day) + str(cur_time.year)
        test_team = "test"
        test_user = User(username="test", password="pass")
        test_game = Games(game="newgame", gameType="testing")
        test_game.save()
        test_user.save()

        # Performs Log-in for the first test user
        driver.get(self.live_server_url + "/pick_up_app/login/")
        driver.find_element(by=By.XPATH, value='//input[@class="user"][@type="username"]').send_keys("test")
        driver.find_element(by=By.XPATH, value='//input[@class="pass"][@type="password"]').send_keys("pass")
        login_button = driver.find_element(by=By.CLASS_NAME, value="login")
        login_button.click()
        driver.implicitly_wait(0.5)
        driver.get(self.live_server_url + "/pick_up_app/timeslot/new/" + test_team)

        # Tests redirection from the Timeslot page to the Calendar using the calendar button
        driver.find_element(by=By.CLASS_NAME, value="calendar_btn").click()
        cur_title = driver.title
        actual_title = test_team + " Team Calendar"
        self.assertEqual(actual_title, cur_title)

        driver.quit()
        print("######################################################################")
        print("#                                                                    #")
        print("#                                                                    #")
        print("#                     End of Selenium Tests                          #")
        print("#                                                                    #")
        print("#                                                                    #")
        print("######################################################################")
