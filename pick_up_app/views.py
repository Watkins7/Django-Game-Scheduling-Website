# HTTP libraries
# from curses.ascii import HT
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse
import datetime
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
import calendar

import pick_up_app
# Forms
from .forms import NewPickupUserForm

# Models
from .models import User, PickupTeam, TimeSlot
from django.conf import settings

##########################################
# Create your views here.
##########################################

def team_search(request):
    if(request.method == "POST"):
        team_search = request.POST['team_search']
        teams = User.objects.filter(teamName__contains = team_search)
        return render(request, 'pick_up_app/team_search.html', {"team_search": team_search, "teams": teams})
    else:
        return render(request, 'pick_up_app/team_search.html')

def main_page(request):
    # This is just a message for the app's index view page, can be changed later.
    return HttpResponse("You're looking at the default main page.")


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
            top_teams_list = PickupTeam.objects.order_by('-mmr_score')[:5]

            # All the teams to add markers
            all_teams = PickupTeam.objects.order_by('teamname')

            # Centered team "username"
            #THIS MUST BE FIXED NEXT ITERATION. THIS IS NOT A GOOD SOLUTION
            centered_team = PickupTeam(teamname = request.user.username, password = request.user.password, email = request.user.email, longitude = -76.7100, latitude = 39.2543)

            teams =  User.objects.all()
            teamNames = []
            for i in range(len(teams)):
                teamNames.append(teams[i].teamName)

            context = {'top_teams_list': top_teams_list,
                       'all_teams': all_teams,
                       'centered_team': centered_team,
                       'api_key': settings.GOOGLE_MAPS_API_KEY,
                       "teams": teamNames,
                       }

            return render(request, 'pick_up_app/home_page.html', context)

    else:
         return HttpResponse("You are not logged in!")


def index(request):
    allUsers = User.objects.all()
    context = {'userList': allUsers}
    return render(request, 'pick_up_app/login.html', context)


def save(request):
    newUser = User(username=request.POST['username'], password=request.POST['password'], teamName=request.POST['teamName'])
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
        f = NewPickupUserForm(request.POST)

        # Form RETURNED is valid
        if f.is_valid():

            #########################################
            # form creates NEW 'PickupTeam'
            #########################################
            try:
                new_user = f.save()

            except BaseException as E:
                return HttpResponse('Error in f.save()...', E)

            ##############################################################
            # Creates NEW 'User', ties User to ForeignKey in PickupTeam
            ##############################################################
            try:
                new_user.teamaccount = User.objects.create(username=new_user.teamname,
                                             email=new_user.email,
                                             password=new_user.password)

            except BaseException as E:
                return HttpResponse('Error in User.create_user()...', E)

            try:
                new_user.save()
            except BaseException as E:
                return HttpResponse('Failed new_user.save()...', E)

            # Send back success message
            messages.success(request, 'Registration submitted successfully! Welcome to PickupTeam')

    # GET request
    else:
        f = NewPickupUserForm()

    # if form invalid or form valid, redisplay orginal form with errors/messages
    return render(request, 'pick_up_app/register.html', {'form': f})


# Class View for a Team's calendar
class TeamCalendarView(generic.ListView):
    model = TimeSlot
    template_name = 'pick_up_app/calendar.html'

    # Custom implementation of get_context_data
    # to provide additional information to the template
    def get_context_data(self, **kwargs):

        # Gets the initial base context data
        context = super().get_context_data(**kwargs)

        # Get a current date either from the request string or generate one
        current_month = get_request_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        new_calendar = Calendar(current_month.year, current_month.month)

        # Call the formatmonth method, which returns our calendar as a table
        formatted_calendar = new_calendar.formatmonth()
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
