from distutils.log import error
from re import L
from django.db import IntegrityError
from django.test import TestCase
from pick_up_app.models import *
import datetime


#Tests reading and writing from User model and the authentication method
class UserModelTests(TestCase):

    #Ensures the model can be written to and read from
    def test_save(self):
        newUser = User(username = "nuck", password="milk")
        newUser.save()
        testUser = User.objects.filter(id=newUser.id)
        self.assertNotEqual(testUser, None)

    #Ensures the authentication method works
    def test_authenticate(self):
        newUser = User(username = "nuck2", password="milk2")
        newUser.save()
        currentUser = User.authenticate(newUser.username, newUser.password)
        self.assertNotEqual(currentUser, None)

    #Ensures the unique constraint works
    def test_games_is_unique(self):
        newGame = Games(game='milk', gameType='drink')
        newGame.save()
        failGame = Games(game='milk', gameType='drink')
        with self.assertRaises(IntegrityError):
            failGame.save()

    #Ensures that letter casing does not matter, the same word will still throw an integrity error
    def test_games_lowercase(self):
        newGame = Games(game='red', gameType='color')
        newGame.save()
        failGame = Games(game='RED', gameType='color')
        with self.assertRaises(IntegrityError):
            failGame.save()


class EmailsModelTests(TestCase):

    # Tests an email object can be created and retrieved
    def test_create_email(self):
        temp_team = User.objects.create(username='test_team')
        temp_email = Emails(team=temp_team, email='test@t.co', is_captain=False)
        temp_email.save()
        test_email = Emails.objects.filter(id=temp_email.id)
        self.assertNotEqual(test_email, None)

    # Tests an exception is raised if a null email is entered
    def test_null_email(self):
        temp_team = User.objects.create(username='test_team')
        temp_email = Emails(team=temp_team, email=None, is_captain=True)

        with self.assertRaises(Exception):
            temp_email.save()

    # Tests an exception is raised if a team has more than one associated team captain email
    def test_two_captain_emails_entered(self):
        temp_team = User.objects.create(username='test_team')
        self.captain_email1 = Emails.objects.create(team=temp_team, is_captain=True)
        captain_email2 = Emails(team=temp_team, is_captain=True)

        with self.assertRaises(Exception):
            captain_email2.save()


# Creates a temporary timeslot with an input time for testing
def create_timeslot(start_time, end_time):
    temp_team = User.objects.create(username='test_team')
    temp_game = Games.objects.create(game='test_game', gameType='Test')
    return TimeSlot(host_team=temp_team, game=temp_game, slot_start=start_time, slot_end=end_time)


class TimeSlotModelTests(TestCase):

    # Tests a timeslot object can be created, has the correct null values, and is retrieved
    def test_create_timeslot(self):
        start_time = timezone.now() - datetime.timedelta(minutes=1)
        end_time = start_time + datetime.timedelta(hours=1)
        temp_timeslot = create_timeslot(start_time, end_time)
        temp_timeslot.save()
        test_timeslot = TimeSlot.objects.get(id=temp_timeslot.id)
        self.assertNotEqual(test_timeslot, None)
        self.assertEqual(test_timeslot.opponent_team, None)
        self.assertEqual(test_timeslot.host_won, None)
        self.assertEqual(test_timeslot.opponent_won, None)

    # Tests an exception is raised if the end of a slot is before the start
    def test_invalid_timeslot(self):
        start_time = timezone.now() + datetime.timedelta(minutes=1)
        end_time = start_time - datetime.timedelta(hours=1)
        temp_timeslot = create_timeslot(start_time, end_time)
        with self.assertRaises(Exception):
            temp_timeslot.save()

    # Tests an exception is raised if a duplicate timeslot is entered
    def test_duplicate_timeslot(self):
        start_time = timezone.now() + datetime.timedelta(minutes=1)
        end_time = start_time + datetime.timedelta(hours=1)
        temp_timeslot1 = create_timeslot(start_time, end_time)
        temp_timeslot1.save()
        temp_game = Games.objects.create(game='test_game2', gameType='Test')
        temp_timeslot2 = TimeSlot(host_team=temp_timeslot1.host_team, game=temp_game,
                                  slot_start=start_time, slot_end=end_time)
        with self.assertRaises(Exception):
            temp_timeslot2.save()
