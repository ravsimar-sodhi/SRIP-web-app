from django.db import models
from datetime import datetime
# from django.contrib.auth.models import User
# from registration.models import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from project.models import Project

# Create your models here.
STATUS = [
('PENDING', 'Pending'),
('REJECTED', 'Rejected'),
('APPROVED', 'Approved'),
]

class LoggedIssue(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='student')
    commit_id = models.CharField(max_length=40,unique=True)
    url = models.URLField(default="https://www.google.com/")
    html_ip = models.FloatField(default=0)
    css_ip = models.FloatField(default=0)
    js_ip = models.FloatField(default=0)
    py_ip = models.FloatField(default=0)
    issue_points = models.FloatField(default=0)
    # mentor = models.CharField(max_length=100,blank=True,null=True)
    toc = models.DateTimeField(default=datetime.now)        ## time of creation
    status = models.CharField(max_length=8, choices = STATUS, default="PENDING")
    remark = models.CharField(default="-",max_length=1000,unique=False)
    # project = models.CharField(max_length=100, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    # evaluated_by = models.CharField(max_length=100, blank=True, null=True)
    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='mentor')
    time_eval = models.DateTimeField(default=datetime.now)
            ## time of creation
    def __str__(self):
        return self.commit_id
