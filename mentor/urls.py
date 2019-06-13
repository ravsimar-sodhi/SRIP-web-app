from django.urls import path, include
from . import views

app_name = 'mentor'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('register', views.register_mentor, name='register_mentor'),
    path('profile', views.profile_mentor, name='profile_mentor'),
    path('evaluate', views.commit_evaluation, name='evaluation'),


]