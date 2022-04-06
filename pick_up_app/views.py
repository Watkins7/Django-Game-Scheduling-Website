# HTTP libraries
# from curses.ascii import HT
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

import pick_up_app


# Forms
from .forms import NewPickupUserForm

# Models
from .models import User

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
    # List of the top 5 teams in User model database to be displayed on the
    # team homepage.
    top_teams_list = User.objects.order_by('-mmr_score')[:5]
    teams =  User.objects.all()
    teamNames = []
    for i in range(len(teams)):
        teamNames.append(teams[i].teamName)
    context = {'top_teams_list': top_teams_list, "teams": teamNames}
    return render(request, 'pick_up_app/home_page.html', context)


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
        return HttpResponse("logged in!")
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
                new_user.teamaccount = User.objects.create_user(username=new_user.teamname,
                                                                email=new_user.email,
                                                                password=new_user.password,)
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
