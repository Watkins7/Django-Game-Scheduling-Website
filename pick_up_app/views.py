from django.shortcuts import render

# Needed for registration
from .forms import NewPickupUserForm
# from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse


##########################################

# Create your views here.
##########################################
# Register Request
def register(request):
    if request.method == 'POST':
        f = NewPickupUserForm(request.POST)
        if f.is_valid():
            new_user = f.save()
            #new_user.refresh_from_db()
            #new_user.pickupteam.longitude = f.longitude
            #new_user.pickupteam.latitude = f.latitude
            new_user.save()
            print("Saved?")
        else:
            print("Not valid")
            print(f.errors)
        return redirect('done/')

    else:
        f = NewPickupUserForm()

    return render(request, 'pick_up_app/register.html', {'form': f})

# Shows Account was made
def done(request):
    return HttpResponse('Account Made')
