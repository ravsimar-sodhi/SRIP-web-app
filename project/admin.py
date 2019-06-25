from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from django.conf.urls import url
from django.shortcuts import render
from .models import Project
from .forms import ProjectBulkAddForm
import requests

# Register your models here.
class ProjectAdmin(GuardedModelAdmin):
    user_can_access_owned_objects_only = True
    user_owned_objects_field = 'coordinators'

    def queryset(self, request):
        qs = super(GuardedModelAdmin, self).queryset(request)
        if self.user_can_access_owned_objects_only and \
            not request.user.is_superuser:
            filters = {self.user_owned_objects_field: request.user}
            qs = qs.filter(**filters)
        return qs

    def add_project(self, name, owner, level):
        obj = Project(name = name, owner = owner, level = level)
        obj.save()
        return

    def add_projects_bulk(self, request):
        if request.method == "POST":
            form = ProjectBulkAddForm(request.POST)
            if form.is_valid():
                owner = form.cleaned_data['owner']
                level = form.cleaned_data['level']
                o_type = form.cleaned_data['o_type']
                url = "https://api.github.com/" + o_type +"s/" + owner + "/repos"
                print(url)
                raw = requests.get(url = url)
                json = raw.json()
                print(json)
                for item in json:
                    name = item['name']
                    owner = item['owner']['login']
                    self.add_project(name, owner, level)
        else:
            form = ProjectBulkAddForm()
        return render(request, 'admin/project/bulk_change_form.html',{'form': form})

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^bulkadd$',
                self.admin_site.admin_view(self.add_projects_bulk), name='bulk_add',
            ),
        ]
        return custom_urls + urls

admin.site.register(Project, ProjectAdmin)