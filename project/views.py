from django.shortcuts import render
from .models import Project
import requests
# Create your views here.

def project_info(name, owner):
    url = "https://api.github.com/repos/" + owner + "/" + name
    raw = requests.get(url = url)
    json = raw.json()
    return json

def list_projects(request):
    projects = []
    # if request.user.is_authenticated:
    for project in Project.objects.all():
        tempd = project_info(project.name, project.owner)
        tempd['level'] = project.level
        tempd['name'] = project.name
        tempd['mentors'] = [mentor for mentor in project.mentors.all() ]
        tempd['students'] = [student for student in project.students.all() ]
        projects.append(tempd)
        print(tempd)
    return render(request, 'project/projectlist.html', {'projects': projects})

def list_project_mentors(request, id):
    project = Project.objects.get(id=id)
    for mentor in project.mentors.all():
        print(mentor)
