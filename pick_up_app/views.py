from django.http import HttpResponse
from django.shortcuts import render

from .models import User

def main_page(request):
    # This is just a message for the app's index view page, can be changed later.
    return HttpResponse("You're looking at the default main page.")


def home_page(request, username):
    top_teams_list = User.objects.order_by('-mmr_score')[:5]
    context = {'top_teams_list': top_teams_list}
    return render(request, 'pick_up_app/home_page.html', context)
    # return HttpResponse("This is the %s home page." % username)