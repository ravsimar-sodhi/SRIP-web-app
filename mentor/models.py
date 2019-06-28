from django.db import models
from django import forms
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _

REGISTRATION_CHOICES = [('PENDING', 'Pending'), ('APPROVED', 'Approved'),('REJECTED', 'Rejected')]

# Create your models here.
class Mentor(models.Model):
    name = models.CharField(max_length = 120)
    email = models.EmailField()
    handle = models.CharField(max_length = 120)
    status = models.CharField(max_length=8, choices = REGISTRATION_CHOICES, default = "PENDING")
    def __str__(self):
        return self.handle

class MentorForm(forms.ModelForm):
    confirm_handle = forms.CharField(max_length=120, label = 'Confirm Handle')
    captcha = CaptchaField()

    class Meta:
        model = Mentor
        fields = ('name', 'email','handle')

    def clean(self):
        cleaned_data = super(MentorForm, self).clean()
        handle = cleaned_data.get('handle')
        c_handle = cleaned_data.get('confirm_handle')

        if handle and c_handle and handle != c_handle:
                raise forms.ValidationError("Handles do not match")

class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = Mentor
        exclude = ['handle','status']
        labels = {
            'name': _('Name of Student'),
            'email':_("Email ID"),
        }