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
    if request.user.is_authenticated:
        for project in Project.objects.all():
            tempd = project_info(project.name, project.owner)
            tempd['level'] = project.level
            tempd['name'] = project.name
            tempd['mentors'] = [mentor for mentor in project.mentors.all() ]
            tempd['students'] = [student for student in project.students.all() ]
            projects.append(tempd)
        return render(request, 'project/projectlist.html', {'projects': projects})

def add_project(name, owner, level):
    obj = Project(name = name, owner = owner, level = level)
    obj.save()

def add_projects_bulk(request, o_type, owner, level):
    url = "https://api.github.com" + o_type +"s/" + owner + "/repos"
    raw = requests.get(url = url)
    json = raw.json()
    for item in json:
        owner, name = item['name'], item['owner']['login']
        add_project(name, owner, level)
    return