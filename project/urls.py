from django.urls import path, include
from . import views

app_name = 'project'
urlpatterns = [
    path('projects', views.list_projects, name = 'list_projects'),
]