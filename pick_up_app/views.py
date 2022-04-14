# HTTP libraries
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse

# Forms
from .forms import NewPickupUserForm

# Models
from .models import User
from .models import PickupTeam

# Import settings and API keys
from django.conf import settings


##########################################
# Create your views here.
##########################################
def main_page(request):
    # This is just a message for the app's index view page, can be changed later.
    return HttpResponse("You're looking at the default main page.")

def testMap(request):
    all_teams = PickupTeam.objects.order_by('teamname')

    centered_team = PickupTeam.objects.get(teamname="sara")

    context = {'all_teams': all_teams,
               'centered_team': centered_team,
               'api_key': settings.GOOGLE_MAPS_API_KEY}

    if PickupTeam.objects.filter(teamname='sara').exists():
        return render(request, 'pick_up_app/testMap.html', context)

    else:
        return HttpResponse("ERROR, Team does not exist")
1
def home_page(request, username):

    # Top Teams to be displayed
    top_teams_list = PickupTeam.objects.order_by('-mmr_score')[:5]

    # All the teams to add markers
    all_teams = PickupTeam.objects.order_by('teamname')

    # Centered team "username"
    try:
        centered_team = PickupTeam.objects.get(teamname=username)
    except Exception:
        return HttpResponse("ERROR, Team does not exist")

    context = {'top_teams_list': top_teams_list,
               'all_teams': all_teams,
               'centered_team': centered_team,
               'api_key': settings.GOOGLE_MAPS_API_KEY
               }

    return render(request, 'pick_up_app/home_page.html', context)

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
                                                                password=new_user.password, )
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
