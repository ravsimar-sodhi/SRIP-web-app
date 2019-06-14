from django.contrib import admin
from .models import LoggedCommit

class LoggedCommitAdmin(admin.ModelAdmin):
    pass
    # list_filter = ('status', 'mentor')
    # list_display = ['user', 'commit_id', 'mentor','url', 'toc', 'remark','status']

admin.site.register(LoggedCommit, LoggedCommitAdmin)