from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_request, name="register_request"),
    path('done/', views.done, name='done')
]