# cal/utils.py

from calendar import HTMLCalendar
from .models import TimeSlot
from django.urls import reverse
from django.utils import timezone
import datetime


# An extension of python's HTMLCalendar with overridden methods to implement time slots
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # Overrides format day to show the timeslots for the day
    def formatday(self, day, slots, viewing_team, cur_team):
        slots_per_day = slots.filter(slot_start__day=day)
        formatted_day = ''

        # For each Timeslot object of the day, list the game name
        for s in slots_per_day:
            # If the start of a timeslot is expired and no challenge has been made, delete it
            if (s.slot_start < timezone.now()) and (not s.opponent_team):
                s.delete()
            else:
                formatted_day += f'<li> {get_slot_url(s, viewing_team, cur_team)} </li>'

        # If the day is not a valid day in the month, return an empty cell
        if not day:
            return '<td></td>'
        return f"<td><span class='date'>{day}</span><ul> {formatted_day} </ul></td>"

    # Overrides format week
    def formatweek(self, week, slots, viewing_team, cur_team):
        formatted_week = ''

        # For each tuple day, format the day number
        for day in week:
            formatted_week += self.formatday(day[0], slots, viewing_team, cur_team)
        return f'<tr> {formatted_week} </tr>'

    # Overrides format month
    def formatmonth(self, viewing_team, cur_team):
        # Retrieves the all timeslots for the current month and year
        slots = TimeSlot.objects.filter(host_team_id=viewing_team.id,
                                        slot_start__year=self.year,
                                        slot_start__month=self.month)

        # Formats the month's header using methods from HTMLCalendar
        formatted_month = f'<table border="8" cellspacing="0" class="calendar">\n'
        formatted_month += f'{self.formatmonthname(self.year, self.month)}\n'
        formatted_month += f'{self.formatweekheader()}\n'

        # For each week in the list of weeks in the month, format the week
        for week in self.monthdays2calendar(self.year, self.month):
            formatted_month += f'{self.formatweek(week, slots, viewing_team, cur_team)}\n'
        formatted_month += f'</table>'
        return formatted_month


# Gets a specific url to be listed on the calendar
def get_slot_url(slot, viewing_team, cur_team):

    # Creates a URL to the past match results html page if the game is over
    if (slot.host_won is not None) and (slot.opponent_won is not None):
        url = reverse('past_game', args=(slot.id, slot.game_id))

    # Creates a URL to the "who won" html page if an opponent has made a challenge
    elif slot.opponent_team and (cur_team.id == slot.opponent_team_id or cur_team.id == slot.host_team_id):
        url = reverse('submit_results', args=(cur_team, slot.id))

    # Creates a URL to the edit timeslot html page if a team is viewing their own calendar
    elif cur_team.username == viewing_team.username:
        url = reverse('timeslot_edit', args=(cur_team, slot.id))

    # Creates a URL to the booking html page if a team is viewing another team's calendar
    elif cur_team.username != viewing_team.username:
        url = reverse('booking', args=(cur_team, slot.id))
    else:
        url = ""
    return f'<a class="listed_timeslot" href="{url}" style="text-decoration: none"> {slot.game} </a>'
