from django.http import HttpResponse
from django.shortcuts import render


def main_page(request):
    # This is just a message for the app's index view page, can be changed later.
    return HttpResponse("You're looking at the default main page.")
