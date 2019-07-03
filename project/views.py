from django.shortcuts import render
from .models import Project
from registration.models import Student
import requests
# Create your views here.

def project_info(name, owner):
    url = "https://api.github.com/repos/" + owner + "/" + name
    raw = requests.get(url = url)
    json = raw.json()
    return json

def list_projects(request):
    projects = []
    projectList = Project.objects.all()
    if request.user.is_authenticated and request.user.role == 1:
        level = Student.objects.get(handle=request.user.username).level
        print(level)
        if level == 1:
            projectList = Project.objects.filter(level1=True)
        elif level == 2:
            projectList = Project.objects.filter(level2=True)
        elif level == 3:
            projectList = Project.objects.filter(level3=True)

    for project in projectList:
        tempd = project.__dict__
        tempd['mentors'] = [mentor for mentor in project.mentors.all() ]
        projects.append(tempd)
    return render(request, 'project/projectlist.html', {'projects': projects})

def list_project_mentors(request, id):
    project = Project.objects.get(id=id)
    for mentor in project.mentors.all():
        print(mentor)
