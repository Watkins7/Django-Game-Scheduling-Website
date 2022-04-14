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
        newUser = User(username = "nuck", password="milk", teamName="usm")
        newUser.save()
        testUser = User.objects.filter(id=newUser.id)
        self.assertNotEqual(testUser, None)

    #Ensures the authentication method works
    def test_authenticate(self):
        newUser = User(username = "nuck2", password="milk2", teamName="usm")
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
        temp_team = PickupTeam.objects.create(teamname='test_team')
        temp_email = Emails(team=temp_team, email='test@t.co', is_captain=False)
        temp_email.save()
        test_email = Emails.objects.filter(id=temp_email.id)
        self.assertNotEqual(test_email, None)

    # Tests an exception is raised if a null email is entered
    def test_null_email(self):
        temp_team = PickupTeam.objects.create(teamname='test_team')
        temp_email = Emails(team=temp_team, email=None, is_captain=True)

        with self.assertRaises(Exception):
            temp_email.save()

    # Tests an exception is raised if a team has more than one associated team captain email
    def test_two_captain_emails_entered(self):
        temp_team = PickupTeam.objects.create(teamname='test_team')
        self.captain_email1 = Emails.objects.create(team=temp_team, is_captain=True)
        captain_email2 = Emails(team=temp_team, is_captain=True)

        with self.assertRaises(Exception):
            captain_email2.save()


class MMRModelTests(TestCase):

    # Tests an MMR object can be created and retrieved
    def test_create_MMR(self):
        temp_team = PickupTeam.objects.create(teamname='test_team')
        temp_mmr = MMR(team=temp_team)
        temp_mmr.save()
        test_mmr = MMR.objects.filter(id=temp_mmr.id)
        self.assertNotEqual(test_mmr, None)

    # Tests an exception is raised if a null MMR is entered
    def test_null_MMR(self):
        temp_team = PickupTeam.objects.create(teamname='test_team')
        temp_email = MMR(team=temp_team, MMR_rating=None)

        with self.assertRaises(Exception):
            temp_email.save()

    # Tests an exception is raised if a team has a negative MMR
    def test_negative_MMR(self):
        temp_team = PickupTeam.objects.create(teamname='test_team')
        negative_mmr = MMR(team=temp_team, MMR_rating=-1)

        with self.assertRaises(Exception) as raised:
            negative_mmr.save()
        self.assertEqual(IntegrityError, type(raised.exception))


# Creates a temporary timeslot with an input time for testing
def create_timeslot(start_time, end_time):
    temp_team = PickupTeam.objects.create(teamname='test_team')
    temp_game = Games.objects.create(game='test_game', gameType='Test')
    return TimeSlot(team=temp_team, game=temp_game, slot_start=start_time, slot_end=end_time)


class TimeSlotModelTests(TestCase):

    # Tests a timeslot object can be created and retrieved
    def test_create_timeslot(self):
        start_time = timezone.now() - datetime.timedelta(minutes=1)
        end_time = start_time + datetime.timedelta(hours=1)
        temp_timeslot = create_timeslot(start_time, end_time)
        temp_timeslot.save()
        test_timeslot = TimeSlot.objects.filter(id=temp_timeslot.id)
        self.assertNotEqual(test_timeslot, None)

    # Tests an exception is raised if an old timeslot is entered
    def test_old_timeslot(self):
        start_time = timezone.now() - datetime.timedelta(minutes=1)
        end_time = start_time + datetime.timedelta(hours=1)
        temp_timeslot = create_timeslot(start_time, end_time)
        self.assertIs(temp_timeslot.is_advanced_date(), False)

    # Tests an advanced timeslot can be entered
    def test_future_timeslot(self):
        start_time = timezone.now() + datetime.timedelta(minutes=1)
        end_time = start_time + datetime.timedelta(hours=1)
        temp_timeslot = create_timeslot(start_time, end_time)
        self.assertIs(temp_timeslot.is_advanced_date(), True)

    # Tests an exception is raised if the end of a slot is before the start
    def test_invalid_timeslot(self):
        start_time = timezone.now() + datetime.timedelta(minutes=1)
        end_time = start_time - datetime.timedelta(hours=1)
        temp_timeslot = create_timeslot(start_time, end_time)
        with self.assertRaises(Exception):
            temp_timeslot.save()

    # Tests an exception is raised if the start and end of a slot are not on the same day
    def test_invalid_timeslot2(self):
        start_time = timezone.now() + datetime.timedelta(minutes=1)
        end_time = start_time + datetime.timedelta(days=1)
        temp_timeslot = create_timeslot(start_time, end_time)
        self.assertIs(temp_timeslot.is_slot_same_day(), False)

    # Tests an exception is raised if a duplicate timeslot is entered
    def test_duplicate_timeslot(self):
        start_time = timezone.now() + datetime.timedelta(minutes=1)
        end_time = start_time + datetime.timedelta(hours=1)
        temp_timeslot1 = create_timeslot(start_time, end_time)
        temp_timeslot1.save()
        temp_game = Games.objects.create(game='test_game2', gameType='Test')
        temp_timeslot2 = TimeSlot(team=temp_timeslot1.team, game=temp_game,
                                  slot_start=start_time, slot_end=end_time)
        with self.assertRaises(Exception):
            temp_timeslot2.save()
