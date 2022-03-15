from django.test import TestCase
from pick_up_app.models import User


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