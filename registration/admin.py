from django.contrib import admin
from .models import Student

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['handle', 'name', 'status', 'mentor','function_points', 'effort', 'report']

admin.site.register(Student, StudentAdmin)

# class UserStudentAdmin(admin.ModelAdmin):
    # pass

# admin.site.register(UserStudent, UserStudentAdmin)