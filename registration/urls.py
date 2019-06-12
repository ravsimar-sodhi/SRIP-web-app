from django.urls import path
from . import views

app_name = 'registration'
urlpatterns = [
    path('register/student', views.register, name='register_student'),
    path('register/mentor', views.register_mentor, name='register_mentor'),
    path('Profile/', views.profile, name='profile'),
]
