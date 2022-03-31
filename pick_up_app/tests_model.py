from distutils.log import error
from re import L
from django.db import IntegrityError
from django.test import TestCase
from pick_up_app.models import *


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