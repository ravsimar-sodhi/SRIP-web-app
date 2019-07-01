from django.contrib import admin
from django.http import HttpResponseRedirect
from guardian.admin import GuardedModelAdmin
from django.urls import path, reverse
from django.shortcuts import render
from django.utils.html import format_html

from .models import Project
from .forms import ProjectBulkAddForm
import requests

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner','id', 'project_actions']
    user_can_access_owned_objects_only = True
    user_owned_objects_field = 'coordinator'

    def add_project(self, name, owner, url, issues, forks, lang):
        obj = Project(name = name, owner = owner, url = url, issues = issues, forks = forks, lang = lang)
        obj.save()
        return

    def add_projects_bulk(self, request):
        if request.method == "POST":
            form = ProjectBulkAddForm(request.POST)
            if form.is_valid():
                owner = form.cleaned_data['owner']
                o_type = form.cleaned_data['o_type']
                url = "https://api.github.com/" + o_type +"s/" + owner + "/repos"
                print(url)
                raw = requests.get(url = url)
                json = raw.json()
                print(json)
                for item in json:
                    name = item['name']
                    owner = item['owner']['login']
                    url = item['html_url']
                    issues = item['open_issues']
                    forks = item['forks']
                    lang = item['language']
                    self.add_project(name, owner, url, issues, forks, lang)
                return HttpResponseRedirect('/admin/project/project')
        else:
            form = ProjectBulkAddForm()
        return render(request, 'admin/project/bulk_change_form.html', context={'form': form})

    def list_project_mentors(self, request, id):
        project = Project.objects.get(id=id)
        mentors = project.mentors.all()
        return render(request, 'admin/project/mentor_list.html', {'mentors':mentors})


    def project_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">View Mentors</a>&nbsp;',
            reverse('admin:list_project_mentors', args=[obj.pk]),
        )
    project_actions.short_description = 'Project Actions'
    project_actions.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulkadd', self.admin_site.admin_view(self.add_projects_bulk), name = 'bulk_add'),
            path('<int:id>/mentors', self.admin_site.admin_view(self.list_project_mentors), name = 'list_project_mentors'),
        ]
        return custom_urls + urls

admin.site.register(Project, ProjectAdmin)
