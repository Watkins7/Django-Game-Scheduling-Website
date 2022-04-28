from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('register/', views.register, name="register"),
    path('login/', views.index, name='index'),
    path('save/', views.save, name='save'),
    path('check/', views.check, name='check'),
    path('teampage/<username>', views.team_page, name="team_page"),
    path('calendar/<username>/', views.TeamCalendarView.as_view(), name='calendar'),
    path('timeslot/new/<username>', views.timeslot, name="timeslot_new"),
    path('timeslot/edit/<username>/int:<timeslot_id>', views.timeslot, name="timeslot_edit"),
    path('timeslot/delete/<username>/int:<timeslot_id>', views.timeslot, name="timeslot_delete"),
    path('<username>/', views.home_page, name='home_page'),
    path('team_search', views.team_search, name='team_search'),
]
