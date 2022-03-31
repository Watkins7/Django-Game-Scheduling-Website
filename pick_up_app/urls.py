from django.urls import path

from . import views

app_name = 'pick_up_app'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('register/', views.register, name="register"),
    path('<username>/', views.home_page, name='home_page'),
]
