from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, AbstractUser
from django.template.defaultfilters import filesizeformat
from django.conf import settings
from captcha.fields import CaptchaField
from django.forms import ValidationError

REGISTRATION_CHOICES = [('PENDING', 'Pending'), ('APPROVED', 'Approved'),('REJECTED', 'Rejected')]
def user_directory_path(instance, filename):
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


def validate_file_extension(value):
    print(value.file.size)
    # print(value.file._size)
    if value.file.content_type != 'application/pdf':
        raise ValidationError(_('Invalid File Type .'))

    if value.file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(_('File Too Large.'))


class User(AbstractUser):
    USER_TYPE_CHOICES = ((1, 'Student'),(2, 'Mentor'))
    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default = 1)

    def __str__(self):
        return self.username

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

    resume = models.FileField(upload_to = user_directory_path, validators=[validate_file_extension])
    st_id = models.FileField(upload_to = user_directory_path, validators=[validate_file_extension])
    status = models.CharField(max_length = 8, choices = REGISTRATION_CHOICES, default = "PENDING")
    function_points = models.FloatField(default=0)
    effort = models.FloatField(default=0)
    report = models.URLField(default="https://github.com/aditya3498/SRIP2019-Batch1/wiki")
    mentor = models.CharField(max_length=100,blank=True,null=True)

    role = models.PositiveSmallIntegerField(default = 1)
    def __str__(self):
        return self.name



class StudentForm(forms.ModelForm):
    confirm_handle = forms.CharField(max_length=120)
    captcha = CaptchaField()
    class Meta:
        model = Student
        fields = ('name', 'email', 'rollno','clg_name','branch', 'year','area_interest','handle','confirm_handle','batch', 'st_id', 'resume')
        labels = {
            'name': _('Name of Student'),
            'email':_("Email ID"),
            'rollno':_("Roll No."),
            'clg_name':_("College Name"),
            'branch':_("Branch"),
            'year':_("Year"),
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



class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['status', 'function_points', 'user','effort', 'report', 'mentor', 'batch', 'handle','role']
        labels = {
            'name': _('Name of Student'),
            'st_id': _("Student ID"),
            'email':_("Email ID"),
            'rollno':_("Roll No."),
            'clg_name':_("College Name"),
            'branch':_("Branch"),
            'year':_("Year"),
            'area_interest':_("Area of Interest"),
            'handle':_("Github Handle"),
            'resume':_("Resume"),
        }