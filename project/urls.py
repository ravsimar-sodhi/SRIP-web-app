from django.urls import path, include
from . import views

app_name = 'project'
urlpatterns = [
    path('list', views.list_projects, name = 'list_projects'),
    path('<int:id>/mentors', views.list_project_mentors, name = 'list_project_mentors'),
]