from curses.ascii import HT
from django.shortcuts import render
from django.http import HttpResponse
from .models import User

# Create your views here.
def index(request):
    allUsers = User.objects.all()
    context = {'userList': allUsers}
    return render(request, 'pick_up_app/index.html', context)

def save(request):
    newUser = User(username=request.POST['username'], password=request.POST['password'], teamName=request.POST['teamName'])
    print(newUser)
    newUser.save()
    return HttpResponse("New User Saved")

def check(request):
    currUser = User.authenticate(request.POST['username'], request.POST['password'])
    if(currUser):
        return HttpResponse("ya yo yaaaa yooooo")
    else:
        return HttpResponse("y u like this")


