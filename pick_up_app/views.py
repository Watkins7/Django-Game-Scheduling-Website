# HTTP libraries
# from curses.ascii import HT
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse
import datetime
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
import calendar

# Forms
from .forms import NewUserForm, TimeSlotForm

# Models
from .models import User, TimeSlot
from django.conf import settings

##########################################
# Create your views here.
##########################################

def team_search(request):
    if(request.method == "POST"):
        team_search = request.POST['team_search']
        teams = User.objects.all()
        return render(request, 'pick_up_app/team_search.html', {"team_search": team_search, "teams": teams})
    else:
        return render(request, 'pick_up_app/team_search.html')

def main_page(request):
    # This is just a message for the app's index view page, can be changed later.
    return render(request, 'pick_up_app/mainpage.html')


def home_page(request, username):

    #Is the user logged in
    if(request.user.is_authenticated):

        #Is the user at THEIR home page
        if(request.user.username != username):

            return HttpResponse("You are trying to view a page that is not yours!")

        else:
            # List of the top 5 teams in User model database to be displayed on the
            # team homepage.Note: Uses a placeholder mmr_score in the User model,
            # will need to be properly implemented and tested later.
            # Top Teams to be displayed
            top_teams_list = User.objects.order_by('-mmr_score')[:5]

            # All the teams to add markers
            all_teams = User.objects.order_by('username')

            # Centered team "username"
            try:
                centered_team = User.objects.get(username=username)
            except Exception:
                return HttpResponse("ERROR, Team does not exist")

            teams =  User.objects.all()
            teamNames = []
            for i in range(len(teams)):
                teamNames.append(teams[i].username)

            key = str(settings.GOOGLE_MAPS_API_KEY)

            context = {'top_teams_list': top_teams_list,
                       'all_teams': all_teams,
                       'centered_team': centered_team,
                       'api_key': key,
                       "teams": teamNames,
                       }

            return render(request, 'pick_up_app/home_page.html', context)

    else:
         return HttpResponse("You are not logged in!")

def team_page(request, username):
     #Is the user logged in
    if(request.user.is_authenticated):

        #Is the user at THEIR home page
        if(request.user.username != username):

            return HttpResponse("You are trying to view a page that is not yours!")

        else:
            return render(request, 'pick_up_app/team.html')

def index(request):
    allUsers = User.objects.all()
    context = {'userList': allUsers}
    return render(request, 'pick_up_app/login.html', context)


def save(request):
    #newUser = User(username=request.POST['username'], password=request.POST['password'], teamName=request.POST['teamName'])
    newUser = User(username=request.POST['username'], password=request.POST['password'])
    print(newUser)
    newUser.save()
    return HttpResponse("New User Saved")


def check(request):
    currUser = User.authenticate(request.POST['username'], request.POST['password'])
    if(currUser):
        login(request, currUser)
        return HttpResponseRedirect(reverse('home_page', args=(currUser.username,)))
    else:
        return HttpResponse("not a user oop")


##########################################
# register
##########################################
def register(request):
    # User Request POST HTTP on '/register'
    if request.method == 'POST':

        # Post Registration Form in browser
        f = NewUserForm(request.POST)

        # Form RETURNED is valid
        if f.is_valid():

            #########################################
            # form creates NEW 'PickupTeam'
            #########################################
            try:
                f.save()

            except BaseException as E:
                return HttpResponse('Error in f.save()...', E)

            ##############################################################
            # Creates NEW 'User', ties User to ForeignKey in PickupTeam
            ##############################################################

            # Send back success message
            messages.success(request, 'Registration submitted successfully! Welcome to PickupTeam')

    # GET request
    else:
        f = NewUserForm()

    # if form invalid or form valid, redisplay orginal form with errors/messages
    return render(request, 'pick_up_app/register.html', {'form': f})


# Class View for a Team's calendar
class TeamCalendarView(generic.ListView):
    model = TimeSlot
    template_name = 'pick_up_app/calendar.html'

    # Ensures only logged-in users can view calendars
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(TeamCalendarView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Only logged in users may view another team's calendar")

    # Custom implementation of get_context_data
    # to provide additional information to the template
    def get_context_data(self, **kwargs):
        # Gets the initial base context data
        context = super().get_context_data(**kwargs)

        # Get a current date either from the request string or generate one
        current_month = get_request_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        new_calendar = Calendar(current_month.year, current_month.month)

        # Gets the team currently making the request and the team of the calendar being viewed
        viewing_team = User.objects.get(username=self.kwargs['username'])
        cur_team = self.request.user.username

        # Call the formatmonth method, which returns our calendar as a table
        formatted_calendar = new_calendar.formatmonth(viewing_team, cur_team)
        context['viewing_team'] = viewing_team.username
        context['current_team'] = cur_team
        context['calendar'] = mark_safe(formatted_calendar)
        context['next_month'] = get_next_month(current_month)
        context['last_month'] = get_last_month(current_month)
        return context


# Checks the request for a valid date and returns the formatted date
def get_request_date(cur_month):

    # Checks if there is a date in the request, if so re-format it to be used by date()
    if cur_month:
        year, month = (int(date_pair) for date_pair in cur_month.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()


# Gets the next month using the current date
def get_next_month(cur_month):
    num_days = calendar.monthrange(cur_month.year, cur_month.month)[1]
    next_month = cur_month.replace(day=num_days) + datetime.timedelta(days=1)
    return 'month=' + str(next_month.year) + '-' + str(next_month.month)


# Gets the last month using the current date
def get_last_month(cur_month):
    previous_month = cur_month.replace(day=1) - datetime.timedelta(days=1)
    return 'month=' + str(previous_month.year) + '-' + str(previous_month.month)


# View to add/update a team's timeslot information
def timeslot(request, username, timeslot_id=None):
    # Ensures only authenticated team can edit timeslot data
    if request.user.is_authenticated:
        if request.user.username != username:
            return HttpResponse("You are trying to view a page that is not yours!")
        else:
            cur_team = User.objects.get(username=username)

            # If a timeslot ID is in the URL, get that timeslot object to be edited
            if timeslot_id:
                instance = get_object_or_404(TimeSlot, pk=timeslot_id)
            else:
                instance = TimeSlot(team=cur_team)

            timeslot_form = TimeSlotForm(request.POST or None, instance=instance)

            # If the request is a post and the form has been cleaned either save the form or delete the timeslot
            if request.POST:
                if request.POST.get('delete'):
                    instance.delete()
                    return HttpResponseRedirect(reverse('calendar', args=(username,)))
                else:
                    if timeslot_form.is_valid():
                        timeslot_form.save()
                        return HttpResponseRedirect(reverse('calendar', args=(username,)))

            context = {'timeslot_form': timeslot_form,
                       'current_team': cur_team.username,
                       'timeslot_id': timeslot_id}
            return render(request, 'pick_up_app/timeslot.html', context)
    else:
        return HttpResponse("You are not logged in!")
