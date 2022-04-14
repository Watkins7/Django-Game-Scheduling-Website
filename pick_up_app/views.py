# HTTP libraries
# from curses.ascii import HT
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect


# Forms
from .forms import NewPickupUserForm

# Models
from .models import User


def main_page(request):
    # This is just a message for the app's index view page, can be changed later.
    return HttpResponse("You're looking at the default main page.")


def home_page(request):
    # List of the top 5 teams in User model database to be displayed on the
    # team homepage. Note: Uses a placeholder mmr_score in the User model,
    # will need to be properly implemented and tested later.
    top_teams_list = User.objects.order_by('-mmr_score')[:5]
    context = {'top_teams_list': top_teams_list}
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
        # Temporary redirection link/code, need to fix authentication
        url = "http://127.0.0.1:8000/pick_up_app/home/"
        return HttpResponseRedirect(url)
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
