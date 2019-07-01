from django.contrib import admin
#from guardian.admin import GuardedModelAdmin
from django.core.mail import EmailMessage
from .models import Student, User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['handle', 'name', 'status','function_points', 'effort', 'report']
    readonly_fields = ["resume", "st_id",]

    def save_model(self, request, obj, form, change):
        if change == True:
            if 'status' in form.changed_data:
                email = EmailMessage('SRIP Registration Status Update.',
                'Hello {0},\n\tYour registration form was reviewed by the admin and your registration has been {1}.'.format(obj.handle, obj.status),
                to=[obj.email],)
                email.send()

        super().save_model(request, obj, form, change)

admin.site.register(Student, StudentAdmin)
