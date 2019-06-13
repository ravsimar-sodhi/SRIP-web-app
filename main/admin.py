from django.contrib import admin
from .models import LoggedIssue

class LoggedIssueAdmin(admin.ModelAdmin):
    list_filter = ('status', 'mentor')
    list_display = ['user', 'commit_id', 'mentor','url', 'toc', 'remark','status']

admin.site.register(LoggedIssue, LoggedIssueAdmin)