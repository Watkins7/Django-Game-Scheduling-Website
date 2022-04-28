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
    path('teampage/<teamname>', views.team_page, name="team_page"),
    path('calendar/', views.TeamCalendarView.as_view(), name='calendar'),
    path('team_search', views.team_search, name='team_search'),
    path('new_game/', views.new_game, name='new_game'),
    path('save_game/', views.save_game, name='save_game'),
    path('check_game_list/', views.check_game_list, name='check_game_list'),
    # path('teampage/<teamname>/edit_team/', views.edit_team, name='edit_team'),
    path('<username>/edit_team/', views.edit_team, name='edit_team'),  # <-- replace later with above line
    path('check_team_changes/', views.check_team_changes, name='check_team_changes'),
    path('<username>/', views.home_page, name='home_page'),
]
