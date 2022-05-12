from django.test import TestCase
from pick_up_app.models import *
from pick_up_app.forms import *
import datetime


# Tests for submitting a new timeslot using the timeslot form
class TimeSlotFormTests(TestCase):
    # Creates a user and game to be used in subsequent tests
    def create_user_and_game(self):
        test_user = User(username="test", password="pass")
        test_game = Games(game="newgame", gameType="testing")
        test_user.save()
        test_game.save()
        return test_user, test_game

    # Tests attempting to enter a timeslot where the end is on a different day than the start
    def test_invalid_timeslot_different_days(self):
        test_user, test_game = self.create_user_and_game()
        cur_time = datetime.datetime.now()
        test_form = TimeSlotForm(data={"host_team": test_user,
                                       "game": test_game,
                                       "slot_start": cur_time + datetime.timedelta(minutes=1),
                                       "slot_end": cur_time + datetime.timedelta(days=1)})
        self.assertFalse(test_form.is_valid())

    # Tests attempting to enter a timeslot where the end is before the start
    def test_invalid_timeslot_end_before_start(self):
        test_user, test_game = self.create_user_and_game()
        cur_time = datetime.datetime.now()
        test_form = TimeSlotForm(data={"host_team": test_user,
                                       "game": test_game,
                                       "slot_start": cur_time + datetime.timedelta(minutes=30),
                                       "slot_end": cur_time + datetime.timedelta(minutes=1)})
        self.assertFalse(test_form.is_valid())

    # Tests attempting to enter a timeslot where it is not advanced
    def test_invalid_timeslot_not_advanced(self):
        test_user, test_game = self.create_user_and_game()
        cur_time = datetime.datetime.now()
        test_form = TimeSlotForm(data={"host_team": test_user,
                                       "game": test_game,
                                       "slot_start": cur_time - datetime.timedelta(minutes=30),
                                       "slot_end": cur_time - datetime.timedelta(minutes=20)})
        self.assertFalse(test_form.is_valid())

    # Tests attempting to enter a timeslot where it overlaps another timeslot
    def test_invalid_timeslot_overlapping(self):
        test_user, test_game = self.create_user_and_game()
        cur_time = datetime.datetime.now()
        test_form1 = TimeSlotForm(data={"is_timeslot_form": True,
                                        "host_team": test_user,
                                        "game": test_game,
                                        "slot_start": cur_time + datetime.timedelta(minutes=5),
                                        "slot_end": cur_time + datetime.timedelta(minutes=10)})
        self.assertTrue(test_form1.is_valid())
        test_form1.save()

        test_form2 = TimeSlotForm(data={"is_timeslot_form": True,
                                        "host_team": test_user,
                                        "game": test_game,
                                        "slot_start": cur_time + datetime.timedelta(minutes=3),
                                        "slot_end": cur_time + datetime.timedelta(minutes=12)})
        self.assertFalse(test_form2.is_valid())

        test_form3 = TimeSlotForm(data={"is_timeslot_form": True,
                                        "host_team": test_user,
                                        "game": test_game,
                                        "slot_start": cur_time + datetime.timedelta(minutes=3),
                                        "slot_end": cur_time + datetime.timedelta(minutes=7)})
        self.assertFalse(test_form3.is_valid())

        test_form4 = TimeSlotForm(data={"is_timeslot_form": True,
                                        "host_team": test_user,
                                        "game": test_game,
                                        "slot_start": cur_time + datetime.timedelta(minutes=7),
                                        "slot_end": cur_time + datetime.timedelta(minutes=12)})
        self.assertFalse(test_form4.is_valid())

    # Tests attempting to enter too many timeslots on the same day
    def test_too_many_timeslots(self):
        test_user, test_game = self.create_user_and_game()
        cur_time = datetime.datetime.now()

        # Creates 8 timeslots on the same day
        for i in range(1, 9):
            test_form1 = TimeSlotForm(data={"is_timeslot_form": True,
                                            "host_team": test_user,
                                            "game": test_game,
                                            "slot_start": cur_time + datetime.timedelta(minutes=(i*2)),
                                            "slot_end": cur_time + datetime.timedelta(minutes=((i*2)+1))})
            test_form1.save()
        test_form2 = TimeSlotForm(data={"is_timeslot_form": True,
                                        "host_team": test_user,
                                        "game": test_game,
                                        "slot_start": cur_time + datetime.timedelta(minutes=(9 * 2)),
                                        "slot_end": cur_time + datetime.timedelta(minutes=((9 * 2) + 1))})
        self.assertFalse(test_form2.is_valid())
