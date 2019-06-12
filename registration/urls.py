from django.urls import path
from . import views

app_name = 'registration'
urlpatterns = [
    path('register/student', views.register_student, name = 'register_student'),
    path('register/mentor', views.register_mentor, name = 'register_mentor'),
    path('mentor/profile', views.profile_mentor, name='profile_mentor'),
    path('student/profile', views.profile_student, name='profile_student'),
]
