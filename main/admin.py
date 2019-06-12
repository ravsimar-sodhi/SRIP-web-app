from django.contrib import admin
from .models import LoggedIssue

class LoggedIssueAdmin(admin.ModelAdmin):
    list_filter = ('is_added', 'mentor')
    list_display = ['user', 'commit_id', 'mentor','url', 'toc', 'remark','is_added']

admin.site.register(LoggedIssue, LoggedIssueAdmin)