from django.urls import path, include
from . import views

app_name = 'mentor'
urlpatterns = [
    path('', views.home, name = 'home')
]