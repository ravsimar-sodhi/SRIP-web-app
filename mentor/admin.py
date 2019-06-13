from django.contrib import admin
from .models import Mentor

# Register your models here.
class MentorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Mentor, MentorAdmin)