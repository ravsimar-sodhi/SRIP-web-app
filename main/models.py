from django.db import models
from datetime import datetime
# from django.contrib.auth.models import User
# from registration.models import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.
class LoggedIssue(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # username = models.CharField(max_length=50)
    commit_id = models.CharField(max_length=40,unique=True)
    url = models.URLField(default="https://www.google.com/")

    html_ip = models.FloatField(default=0)
    css_ip = models.FloatField(default=0)
    js_ip = models.FloatField(default=0)
    py_ip = models.FloatField(default=0)

    issue_points = models.FloatField(default=0)

    mentor = models.CharField(max_length=100,blank=True,null=True)
    handle = models.CharField(max_length=25,blank=True,null=True,unique=False)
    toc = models.DateTimeField(default=datetime.now)        ## time of creation
    is_added = models.BooleanField(default=False)
    remark = models.CharField(default="-",max_length=1000,unique=False)

    def __str__(self):
        return self.commit_id

# class LoggedIssueForm(ModelForm):
#     class Meta:
#         model = LoggedIssue
#         exclude = ['user',
#         'html_ip',
#         'css_ip',
#         'js_ip',
#         'python_ip',
#         'issue_points',
#         'mentor',
#         'handle',
#         'toc',
#         'is_added',
#         'remark',
#         ]
#         labels = {
#             'commit_id':_("Commit ID"),
#             'url':_("URL"),
#         }