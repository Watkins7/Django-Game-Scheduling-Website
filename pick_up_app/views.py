# HTTP libraries
# from curses.ascii import HT
from django.shortcuts import render, get_object_or_404, redirect
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
from .models import User, TimeSlot, Games
from django.conf import settings


##########################################
# Create your views here.
##########################################

def team_search(request):
    if (request.method == "POST"):
        team_search = request.POST['team_search']
        teams = User.objects.filter(teamname__contains=team_search)
        return render(request, 'pick_up_app/team_search.html', {"team_search": team_search, "teams": teams})
    else:
        return render(request, 'pick_up_app/team_search.html')


def main_page(request):
    # This is just a message for the app's index view page, can be changed later.
    return render(request, 'pick_up_app/mainpage.html')


def home_page(request, username):
    # Is the user logged in
    if (request.user.is_authenticated):

        # Is the user at THEIR home page
        if (request.user.username != username):

            return HttpResponse("You are trying to view a page that is not yours!")

        else:
            # List of the top 5 teams in User model database to be displayed on the
            # team homepage.Note: Uses a placeholder mmrScore in the User model,
            # will need to be properly implemented and tested later.
            # Top Teams to be displayed
            top_teams_list = User.objects.order_by('-mmrScore')[:5]

            # All the teams to add markers
            all_teams = User.objects.order_by('username')

            # Centered team "username"
            try:
                centered_team = User.objects.get(username=username)
            except Exception:
                return HttpResponse("ERROR, Team does not exist")

            teams = User.objects.all()
            teamNames = []
            for i in range(len(teams)):
                teamNames.append(teams[i].teamname)

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
    # Is the user logged in
    if (request.user.is_authenticated):
        # Is the user at THEIR home page
        if (request.user.username != username):
            return HttpResponse("You are trying to view a page that is not yours!")
        else:
            allUsers = User.objects.all()
            email_list = User.objects.order_by('email')
            emailList = []
            for i in range(len(email_list)):
                emailList.append(email_list[i].email) 
            context = {'userList': allUsers,
                        'email_list': email_list}
            return render(request, 'pick_up_app/team.html')


def index(request):
    allUsers = User.objects.all()
    context = {'userList': allUsers}
    return render(request, 'pick_up_app/login.html', context)


def save(request):
    # newUser = User(username=request.POST['username'], password=request.POST['password'], teamName=request.POST['teamName'])
    newUser = User(username=request.POST['username'], password=request.POST['password'])
    print(newUser)
    newUser.save()
    return HttpResponse("New User Saved")


def check(request):
    currUser = User.authenticate(request.POST['username'], request.POST['password'])
    if (currUser):
        login(request, currUser)
        return HttpResponseRedirect(reverse('home_page', args=(currUser.username,)))
    else:
        messages.add_message(request, messages.ERROR, 'Error, Invalid username or password')
        return render(request, 'pick_up_app/login.html')


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
            messages.add_message(request, messages.SUCCESS,
                                 'Registration submitted successfully! Welcome to PickupTeam')

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
            try:
                return super(TeamCalendarView, self).dispatch(request, *args, **kwargs)
            except User.DoesNotExist:
                return HttpResponse("The calendar you're looking for does not exist")
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
        context['viewing_teamname'] = viewing_team.teamname
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


# Will allow another team to be added to a timeslot
def booking(request, username, timeslot_id):
    # username should be OPPONENT
    # timeslot_id should be able to gather all others information

    # see if opponent team exists
    cur_team = User.objects.get(username=username)
    if not cur_team:
        return HttpResponse("Error, invalid 'username' passed")

    # see if timeslot exists
    instance = TimeSlot.objects.get(pk=timeslot_id)
    if not instance:
        return HttpResponse("Error, 'timeslot_id' does not exist")

    # check if booking_team != host_team
    if instance.host_team.username == username:
        host_calendar = "/pick_up_app/calendar/" + str(instance.host_team.username)
        messages.error(request, "You are trying to book your own game!")
        return HttpResponseRedirect(host_calendar)

    # if there is already opponent team on the timeslot
    # return response
    if instance.opponent_team:
        host_calendar = "/pick_up_app/calendar/" + str(instance.host_team.username)
        messages.error(request, "This game has already been booked!")
        return HttpResponseRedirect(host_calendar)

    # if POST request
    if request.method == 'POST':

        var = request.POST["submitbutton"]

        # update the timeslot with new oppenent_id
        if var == "Yes":
            userobject = User.objects.get(username=username)
            instance.opponent_team_id = userobject.id
            instance.save()
            messages.success(request, "You have successfully booked this game!")

        # go back to host team calendar
        host_calendar = "/pick_up_app/calendar/" + str(instance.host_team.username)
        return HttpResponseRedirect(host_calendar)

    # else this is a GET operation
    else:

        # variables to past to HTML
        context = {'host': instance.host_team.username,
                   'start': instance.slot_start,
                   'end': instance.slot_end,
                   'team': cur_team.username,
                   'gameName': Games.objects.get(id=instance.game_id).game,
                   'gameType': Games.objects.get(id=instance.game_id).gameType,
                   'opponent': username
                   }

        # Render the booking html
        return render(request, 'pick_up_app/booking.html', context)


# Will allow selected username to update timeslot GAME RESULTS
def submit_results(request, username, timeslot_id):
    # username should be OPPONENT or HOST
    # timeslot_id should be able to gather all other information

    # see if opponent team exists
    cur_team = User.objects.get(username=username)
    if not cur_team:
        return HttpResponse("Error, invalid 'username' passed")

    # see if timeslot exists
    instance = TimeSlot.objects.get(pk=timeslot_id)
    if not instance:
        return HttpResponse("Error, 'timeslot_id' does not exist")

    # check if booking_team != host_team
    if instance.host_team and instance.opponent_team:

        # if POST request
        if request.method == 'POST':

            var = request.POST["submitbutton"]

            if var == "Yes, I won the game!":
                if instance.host_team.username == username:
                    instance.host_won = True
                    instance.save()

                elif instance.opponent_team.username == username:
                    instance.opponent_won = True
                    instance.save()

            elif var == "No, we lost the game!":
                if instance.host_team.username == username:
                    instance.host_won = False
                    instance.save()

                elif instance.opponent_team.username == username:
                    instance.opponent_won = False
                    instance.save()

            elif var == "Oops! I am not ready at this time!":
                if instance.host_team.username == username:
                    instance.host_won = None
                    instance.save()

                elif instance.opponent_team.username == username:
                    instance.opponent_won = None
                    instance.save()

            if (instance.opponent_won == False and instance.host_won == True) or (
                    instance.opponent_won == True and instance.host_won == False):

                hostObj = User.objects.get(id=instance.host_team_id)
                opponentObj = User.objects.get(id=instance.opponent_team_id)

                if instance.opponent_won == False:
                    opponentObj.mmrScore -= 5
                    hostObj.mmrScore += 5

                else:
                    opponentObj.mmrScore += 5
                    hostObj.mmrScore -= 5

            # go back to host team calendar
            host_calendar = "/pick_up_app/calendar/" + str(instance.host_team.username)
            messages.success(request, "Your submission was processed!")
            return HttpResponseRedirect(host_calendar)

        # else this is get request

        # variables to past to HTML
        context = {'team': cur_team.username,
                   'gameName': Games.objects.get(id=instance.game_id).game,
                   'gameType': Games.objects.get(id=instance.game_id).gameType,
                   'start': instance.slot_start,
                   'end': instance.slot_end,
                   'host': User.objects.get(id=instance.host_team_id).username,
                   'opponent': User.objects.get(id=instance.opponent_team_id).username
                   }

        return render(request, 'pick_up_app/submitGameResults.html', context)

    # else timeslot does not have enough teams to submit results
    else:
        return HttpResponse("Error, 'timeslot' does not have 'opponent_id'... or possibly 'host_id'")


# Views for displaying a finished game
def past_game(request, timeslot_id, game_id):
    # get game object
    gameObj = Games.objects.get(id=game_id)
    timeslotObj = TimeSlot.objects.get(id=timeslot_id)

    # default settings
    results = "Invalid!"
    winner = "Invalid!"
    loser = "Invalid!"

    # if there is a winner and loser
    if timeslotObj.host_won == (not timeslotObj.opponent_won):
        results = "Valid!"

        # set variables based on who won
        if timeslotObj.host_won:
            winner = User.objects.get(id=timeslotObj.host_team_id).username
            loser = User.objects.get(id=timeslotObj.opponent_team_id).username
        else:
            winner = User.objects.get(id=timeslotObj.opponent_team_id).username
            loser = User.objects.get(id=timeslotObj.host_team_id).username

    # appropriate context to be passed to HTML
    context = {'results': results,
               'gameName': gameObj.game,
               'gameType': gameObj.gameType,
               'start': timeslotObj.slot_start,
               'end': timeslotObj.slot_end,
               'host': User.objects.get(id=timeslotObj.host_team_id).username,
               'opponent': User.objects.get(id=timeslotObj.opponent_team_id).username,
               'winner': winner,
               'loser': loser,
               'current_team': request.user.username,
               'home_page': '/pick_up_app/'

               }

    return render(request, 'pick_up_app/past_game.html', context)


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
                instance = TimeSlot(host_team=cur_team)

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


# View where user can add a new game
def new_game(request):
    all_games = Games.objects.all()
    context = {'game_list': all_games}
    return render(request, 'pick_up_app/new_game.html', context)


# Save the new game that was added by the new game page
def save_game(request):
    curr_game = Games(game=request.POST['game_name'], gameType=request.POST['game_type'])
    curr_game.save()
    messages.success(request, 'New game added successfully!')
    return HttpResponse("New game saved.")


# Check that the new game given is not in the database yet
def check_game_list(request):
    curr_game = Games.verify(request.POST['game_name'], request.POST['game_type'])
    if curr_game:
        save_game(request)
    else:
        messages.error(request, 'Game could not be added.')
    return HttpResponseRedirect(reverse('new_game'))


def edit_team(request, username):
    curr_team = User.objects.filter(username=username)
    context = {'team_info': curr_team}
    return render(request, 'pick_up_app/edit_team.html', context)


def check_team_changes(request):
    curr_username = request.user.username
    my_user = User.objects.get(username=curr_username)

    new_username = request.POST['new_username']
    new_team_name = request.POST['new_team_name']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    new_email = request.POST['new_email']

    # If new username given, make sure username is unique and not current username before saving
    if new_username:
        if my_user.username == new_username:
            messages.error(request, "The username given is already this team's username.")

        # Check that username is unique from other users
        else:
            is_unique = True
            for check_user in User.objects.all():
                if check_user.username == new_username and my_user.id != check_user.id:
                    is_unique = False
            # If unique, save the new username
            if is_unique:
                my_user.username = new_username
                my_user.save()
                messages.success(request, "Username changed successfully.")
            # If not unique, sent error message
            else:
                messages.error(request, "This username is already taken.")

    # If new team name, save if not the same as current team name
    if new_team_name:
        if my_user.teamname == new_team_name:
            messages.error(request, "The team name given is already this team's team name.")
        else:
            my_user.teamname = new_team_name
            my_user.save()
            messages.success(request, "Team name changed successfully.")

    # If new password is not the same as old one, make sure it matches confirmation password before saving
    if new_password:
        if my_user.password == new_password:
            messages.error(request, "The password given is already this team's password.")
        else:
            if new_password == confirm_password:
                my_user.password = new_password
                my_user.checkpassword = confirm_password
                my_user.save()
                messages.success(request, "Password changed successfully.")
            else:
                messages.error(request, "The new password and password confirmation do not match.")

    # If new email given, make sure that the email is not the current email before saving
    if new_email:
        if my_user.email == new_email:
            messages.error(request, "The email given is already this team's email.")
        else:
            my_user.email = new_email
            my_user.save()
            messages.success(request, "Team email changed successfully.")
    return HttpResponseRedirect(reverse('edit_team', args=(my_user.username,)))
