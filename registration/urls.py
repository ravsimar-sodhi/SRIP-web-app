from django.urls import path
from . import views

app_name = 'registration'
urlpatterns = [
    path('student/register', views.register_student, name = 'register_student'),
    path('student/profile', views.profile_student, name='profile_student'),
]
