# HTTP libraries
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse

# Forms
from .forms import NewPickupUserForm

# Models
from django.contrib.auth.models import User

##########################################
# Create your views here.
##########################################

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
                new_user.save()
            except BaseException as E:
                return HttpResponse('Error in f.save()...', E)

            ##############################################################
            # Creates NEW 'User', ties User to ForeignKey in PickupTeam
            ##############################################################
            try:
                new_user.teamaccount = User.objects.create_user(username=new_user.teamname,
                                                                email=new_user.email,
                                                                password=new_user.password
                                                                )
            except BaseException as E:
                return HttpResponse('Error in User.create_user()...', E)

            # Send back success message
            messages.success(request, 'Registration submitted successfully! Welcome to PickupTeam')

    # GET request
    else:
        f = NewPickupUserForm()

    # if form invalid or form valid, redisplay orginal form with errors/messages
    return render(request, 'pick_up_app/register.html', {'form': f})
