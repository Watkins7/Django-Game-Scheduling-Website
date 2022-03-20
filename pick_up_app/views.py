from django.shortcuts import render

# Needed for registration
from .forms import NewPickupUser
from django.contrib.auth import login
from django.contrib import messages
##########################################

# Create your views here.
##########################################
# Register Request
def register_request(request):

    from django.contrib.auth import get_user_model
    User = get_user_model()
    users = User.objects.all()

    print(users)

    # If /register http request was POST information
    if request.method == "POST":

        # Call register Pickup class and request POST
        form = NewPickupUser(request.POST)

        # Check to see if information recorded is valid
        if form.is_valid():

            user = form.save()
            login(request, user)

            messages.success(request, "Successfully Registered New Team!")

            # Put in redirect to homepage
            #return redirect()

        messages.error(request, "Was unable to succesfully register team")

    # Else it was a GET method to get userform
    form = NewPickupUser()
    return render (request=request, template_name='pick_up_app/register.html', context={"register_form":form})