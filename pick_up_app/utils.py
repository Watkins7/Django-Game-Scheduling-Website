# cal/utils.py

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import TimeSlot


# An extension of python's HTMLCalendar with overridden methods to implement time slots
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # Overrides format day to show the timeslots for the day
    def formatday(self, day, slots):
        slots_per_day = slots.filter(slot_start__day=day)
        formatted_day = ''

        # For each Timeslot object of the day, list the game name
        for s in slots_per_day:
            formatted_day += f'<li> {s.game.game} </li>'

        # If the day is not a valid day in the month, return an empty cell
        if not day:
            return '<td></td>'
        return f"<td><span class='date'>{day}</span><ul> {formatted_day} </ul></td>"

    # Overrides format week
    def formatweek(self, week, slots):
        formatted_week = ''

        # For each tuple day, format the day number
        for day in week:
            formatted_week += self.formatday(day[0], slots)
        return f'<tr> {formatted_week} </tr>'

    # Overrides format month
    def formatmonth(self):
        # Retrieves the all timeslots for the current month and year
        slots = TimeSlot.objects.filter(slot_start__year=self.year, slot_start__month=self.month)

        # Formats the month's header using methods from HTMLCalendar
        formatted_month = f'<table border="2" cellpadding="5" cellspacing="1" class="calendar">\n'
        formatted_month += f'{self.formatmonthname(self.year, self.month)}\n'
        formatted_month += f'{self.formatweekheader()}\n'

        # For each week in the list of weeks in the month, format the week
        for week in self.monthdays2calendar(self.year, self.month):
            formatted_month += f'{self.formatweek(week, slots)}\n'
        return formatted_month
