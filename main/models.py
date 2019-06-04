from django.db import models
from datetime import datetime

# Create your models here.
class LoggedIssue(models.Model):
    username = models.CharField(max_length=50)
    commit_id = models.CharField(max_length=40,unique=True)
    url = models.URLField(default="https://www.google.com/")
    html_ip = models.FloatField(default=0)
    css_ip = models.FloatField(default=0)
    js_ip = models.FloatField(default=0)
    python_ip = models.FloatField(default=0)

    issue_points = models.FloatField(default=0)
    mentor = models.CharField(max_length=100,blank=True,null=True)
    handle = models.CharField(max_length=25,blank=True,null=True,unique=False)
    toc = models.DateTimeField(default=datetime.now)        ## time of creation
    is_added = models.BooleanField(default=False)
    remark = models.CharField(default="-",max_length=1000,unique=False)

    def __str__(self):
        return self.commit_id