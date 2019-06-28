from django.contrib import admin
from django.shortcuts import render
from django.utils.html import format_html
from django.urls import path, reverse
from .models import Mentor
from registration.models import User
from main.models import LoggedCommit

# Register your models here.
class MentorAdmin(admin.ModelAdmin):
    list_display = ['name', 'handle', 'id','mentor_actions']

    def list_projects(self, request, id):
        mentor = Mentor.objects.get(id=id)
        projects = mentor.project_set.all()
        return render(request, 'admin/mentor/proj_list.html',{'projects': projects})

    def list_evals(self, request, id):
        mentor = Mentor.objects.get(id=id)
        mentor = User.objects.get(username=mentor)
        evals = LoggedCommit.objects.filter(evaluated_by=mentor)
        return render(request, 'admin/mentor/eval_list.html', {'evals': evals})

    def mentor_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">View Evaluations</a>&nbsp;'
            '<a class="button" href="{}">View Projects</a>&nbsp;',
            reverse('admin:list_evals', args=[obj.pk]),
            reverse('admin:list_projects', args=[obj.pk]),
        )
    mentor_actions.short_description = 'Mentor Actions'
    mentor_actions.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<int:id>/evals", self.admin_site.admin_view(self.list_evals), name = 'list_evals'),
            path("<int:id>/projects", self.admin_site.admin_view(self.list_projects), name = 'list_projects'),
        ]
        return custom_urls + urls

    def save_model(self, request, obj, form, change):
        if change == True:
            if 'status' in form.changed_data:
                email = EmailMessage('SRIP Registration Status Update.',
                'Hello {0},\n\tYour registration form was reviewed by the admin and your registration has been {1}.'.format(obj.handle, obj.status),
                to=[obj.email],)
                email.send()
        super().save_model(request, obj, form, change)

admin.site.register(Mentor, MentorAdmin)