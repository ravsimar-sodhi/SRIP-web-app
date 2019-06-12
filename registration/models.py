from django.db import models
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

REGISTRATION_CHOICES = [('PENDING', 'Pending'), ('APPROVED', 'Approved'),('REJECTED', 'Rejected')]
def user_directory_path(instance, filename):
    # file will be uploaded to ME   DIA_ROOT/user_<id>/<filename>
    return 'registrations/{0}'.format(filename)


BATCHES = [
    ("Batch1", "Batch 1"),
    ("Batch2", "Batch 2"),
]
YEAR = [
    ("FirstYear", "First Year"),
    ("SecondYear", "Second Year"),
    ("ThirdYear", "Third Year"),
    ("FourthYear", "Fourth Year"),
]
AREA_OF_INTEREST = [
    ("MachineLearning", "Machine Learning"),
    ("Programming", "Programming"),
    ("WebDev", "Web Development"),
]
class Student(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    rollno = models.CharField(max_length = 10)
    clg_name = models.CharField(max_length = 120)
    branch = models.CharField(max_length = 100)
    year = models.CharField(max_length=100, choices = YEAR, default="FirstYear")
    area_interest = models.CharField(max_length = 120, default="Programming")
    handle = models.CharField(max_length = 120)
    batch = models.CharField(max_length=100, choices = BATCHES, default="Batch1")

    resume = models.FileField(upload_to = user_directory_path)
    st_id = models.FileField(upload_to = user_directory_path)

    status = models.CharField(max_length = 8, choices = REGISTRATION_CHOICES, default = "PENDING")

    function_points = models.FloatField(default=0)
    effort = models.FloatField(default=0)
    report = models.URLField(default="https://github.com/aditya3498/SRIP2019-Batch1/wiki")
    mentor = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['status',
        'user',
        'function_points',
        'effort',
        'report',
        'mentor',
        ]
        labels = {
            'name': _('Name of Student'),
            'st_id': _("Student ID"),
            'email':_("Email ID"),
            'rollno':_("Roll No."),
            'clg_name':_("College Name"),
            'branch_year':_("Branch & Year"),
            'area_interest':_("Area of Interest"),
            'handle':_("Github Handle"),
            'resume':_("Resume"),
        }

class ProfileForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['status', 'function_points', 'user','effort', 'report', 'mentor', 'batch', 'handle']
        labels = {
            'name': _('Name of Student'),
            'st_id': _("Student ID"),
            'email':_("Email ID"),
            'rollno':_("Roll No."),
            'clg_name':_("College Name"),
            'branch_year':_("Branch & Year"),
            'area_interest':_("Area of Interest"),
            'handle':_("Github Handle"),
            'resume':_("Resume"),
        }