from django.contrib import admin
from .models import LoggedIssue

class LoggedIssueAdmin(admin.ModelAdmin):
    pass

admin.site.register(LoggedIssue, LoggedIssueAdmin)
# Register your models here.
