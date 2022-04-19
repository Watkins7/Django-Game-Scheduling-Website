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
    path('teampage/', views.team_page, name="team_page"),
    path('calendar/', views.TeamCalendarView.as_view(), name='calendar'),
    path('<username>/', views.home_page, name='home_page'),
    path('team_search', views.team_search, name='team_search'),
]
