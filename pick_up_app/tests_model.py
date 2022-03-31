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