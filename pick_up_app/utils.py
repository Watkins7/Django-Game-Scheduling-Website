# cal/utils.py

from calendar import HTMLCalendar
from .models import TimeSlot, User
from django.urls import reverse
from django.utils import timezone


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
            # Only show future timeslots on the calendar
            if s.slot_start > timezone.now():
                formatted_day += f'<li> {get_slot_url(s, viewing_team, cur_team)} </li>'
            # For now, expired timeslots are just not shown, if need be in the future they can be deleted here

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

    #############################################################################################
    # Team owns the time slot
    #############################################################################################

    # If a team is viewing their own calendar the
    # And timeslot still has NULL opponent team
    # url links to the edit timeslot page
    if (cur_team == viewing_team.username) and not slot.opponent_team_id:
        url = reverse('timeslot_edit', args=(cur_team, slot.id,))

    # If a team is viewing their own calendar the
    # opponent slot is NOT null
    # viewing team needs to submit GAME RESULTS
    elif (cur_team == viewing_team.username) and slot.opponent_team_id:
        url = reverse('submit_results', args=(cur_team, slot.id,))

    #############################################################################################
    # Viewing another team's calendar
    #############################################################################################

    # if opponent_id slot is null
    # opponent can book game
    elif not slot.opponent_team_id:
        url = reverse('booking', args=(cur_team, slot.id,))

    # if opponent_id slot is NOT null
    # viewing_team id == opponent_id in slot
    # opponent is trying to submit results
    elif User.objects.get(id=slot.opponent_team_id).username == cur_team:
        url = reverse('submit_results', args=(cur_team, slot.id,))

    # the url links to the challenge page
    else:
        return f'<a class="listed_timeslot" href="#" style="text-decoration: none"> {slot.game} </a>'
    return f'<a class="listed_timeslot" href="{url}" style="text-decoration: none"> {slot.game} </a>'
