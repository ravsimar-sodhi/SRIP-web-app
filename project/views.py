from django.shortcuts import render
from .models import Project

# Create your views here.
def list_projects(request):
    projects = []
    if request.user.is_authenticated:
        for project in Project.objects.all():
            tempd = {}
            print(project.mentors.all())
            tempd['project_id'] = project.project_id
            tempd['level'] = project.level
            tempd['name'] = project.name
            tempd['url'] = project.url
            tempd['mentors'] = [mentor for mentor in project.mentors.all() ]
            tempd['students'] = [student for student in project.students.all() ]
            projects.append(tempd)
        return render(request, 'project/projectlist.html', {'projects': projects})