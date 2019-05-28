from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

REGISTRATION_CHOICES = [('PENDING', 'Pending'), ('APPROVED', 'Approved'),('REJECTED', 'Rejected')]
def user_directory_path(instance, filename):
    # file will be uploaded to ME   DIA_ROOT/user_<id>/<filename>
    return 'registrations/{0}'.format(filename)

class Student(models.Model):
    name = models.CharField(max_length = 120)
    email = models.EmailField()
    rollno = models.CharField(max_length = 10)
    clg_name = models.CharField(max_length = 120)
    branch_year = models.CharField(max_length = 120)
    area_interest = models.CharField(max_length = 120)
    handle = models.CharField(max_length = 120)
    resume = models.FileField(upload_to = user_directory_path)
    st_id = models.FileField(upload_to = user_directory_path)

    status = models.CharField(max_length = 8, choices = REGISTRATION_CHOICES, default = "PENDING")
    def __str__(self):
        return self.name

class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['status']
        labels = {
            'name': _('Name of Student'),
            'st_id': _("Student ID"),
        }
        # labels = {
        #     'name': _('Writer'),
        # }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }