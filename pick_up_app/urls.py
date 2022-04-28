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
    path('calendar/<teamname>/', views.TeamCalendarView.as_view(), name='calendar'),
    path('timeslot/new/<teamname>', views.timeslot, name="timeslot_new"),
    path('timeslot/edit/<teamname>/int:<timeslot_id>', views.timeslot, name="timeslot_edit"),
    path('timeslot/delete/<teamname>/int:<timeslot_id>', views.timeslot, name="timeslot_delete"),
    path('team_search', views.team_search, name='team_search'),
    path('<username>/', views.home_page, name='home_page'),
    path('teampage/<teamname>', views.team_page, name="team_page"),
]
