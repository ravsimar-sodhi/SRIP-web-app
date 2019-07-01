from django.contrib import admin
from .models import LoggedCommit
from mentor.models import Mentor

def approve_status(modeladmin, request, queryset):
    queryset.update(status = "APPROVED")
approve_status.short_description = "Mark selected Commits as approved"

class LoggedCommitAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ['user', 'commit_id','url', 'issue_points','toc', 'remark','status', 'project', 'evaluated_by', 'time_eval']
    actions = [approve_status]

    def get_queryset(self, request):
        qs = super(admin.ModelAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            mentor = Mentor.objects.get(handle=request.user)
            projects = mentor.project_set.all()
            qs = qs.filter(project__in=projects)
        return qs

admin.site.register(LoggedCommit, LoggedCommitAdmin)