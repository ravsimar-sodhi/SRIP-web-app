from django.db import models
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, AbstractUser

REGISTRATION_CHOICES = [('PENDING', 'Pending'), ('APPROVED', 'Approved'),('REJECTED', 'Rejected')]
def user_directory_path(instance, filename):
    return 'registrations/{0}'.format(filename)

class User(AbstractUser):
    USER_TYPE_CHOICES = ((1, 'Student'),(2, 'Mentor'))
    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default = 1)

    def __str__(self):
        return self.username

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
    function_points = models.FloatField(default=0)
    effort = models.FloatField(default=0)
    report = models.URLField(default="https://github.com/aditya3498/SRIP2019-Batch1/wiki")
    mentor = models.CharField(max_length=100,blank=True,null=True)
    batch = models.CharField(max_length=100,default="SRIP19-BATCH1")
    role = models.PositiveSmallIntegerField(default = 1)
    def __str__(self):
        return self.name

class Mentor(models.Model):
    name = models.CharField(max_length = 120)
    email = models.EmailField()
    handle = models.CharField(max_length = 120)
    status = models.CharField(max_length=8, choices = REGISTRATION_CHOICES, default = "PENDING")
    role = models.PositiveSmallIntegerField(default = 2)
    def __str__(self):
        return self.handle

class StudentForm(ModelForm):
    # handle = forms.CharField(max_length=120)
    confirm_handle = forms.CharField(max_length=120)
    class Meta:
        model = Student
        fields = ('name', 'email', 'rollno','clg_name','branch_year','area_interest','handle','confirm_handle', 'st_id', 'resume')
        labels = {
            'name': _('Name of Student'),
            'email':_("Email ID"),
            'rollno':_("Roll No."),
            'clg_name':_("College Name"),
            'branch_year':_("Branch & Year"),
            'area_interest':_("Area of Interest"),
            'handle':_("Github Handle"),
            'confirm_handle':_("Confirm Handle"),
            'st_id': _("Student ID"),
            'resume':_("Resume"),
        }
        def clean(self):
            cleaned_data = super(StudentForm, self).clean()
            handle = cleaned_data.get('handle')
            c_handle = cleaned_data.get('confirm_handle')

            if handle and c_handle and handle != c_handle:
                    raise forms.ValidationError("Handles do not match")

class MentorForm(ModelForm):
    confirm_handle = forms.CharField(max_length=120, label = 'Confirm Handle')

    class Meta:
        model = Mentor
        fields = ('name', 'email','handle')

    def clean(self):
        cleaned_data = super(MentorForm, self).clean()
        handle = cleaned_data.get('handle')
        c_handle = cleaned_data.get('confirm_handle')

        if handle and c_handle and handle != c_handle:
                raise forms.ValidationError("Handles do not match")

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