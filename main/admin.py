from django.contrib import admin
from .models import LoggedCommit

def approve_status(modeladmin, request, queryset):
    queryset.update(status = "APPROVED")
approve_status.short_description = "Mark selected Commits as approved"

class LoggedCommitAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ['user', 'commit_id','url', 'issue_points','toc', 'remark','status', 'project', 'evaluated_by', 'time_eval']
    actions = [approve_status]

admin.site.register(LoggedCommit, LoggedCommitAdmin)