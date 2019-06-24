from django.contrib import admin
from .models import Mentor

# Register your models here.
class MentorAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change == True:
            if 'status' in form.changed_data:
                email = EmailMessage('SRIP Registration Status Update.',
                'Hello {0},\n\tYour registration form was reviewed by the admin and your registration has been {1}.'.format(obj.handle, obj.status),
                to=[obj.email],)
                email.send()

        super().save_model(request, obj, form, change)
admin.site.register(Mentor, MentorAdmin)