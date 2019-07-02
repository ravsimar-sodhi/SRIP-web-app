from django.db import models
from django.conf import settings
from mentor.models import Mentor
from registration.models import Student
from django.contrib.auth.models import Group


class Project(models.Model):
    name = models.CharField(max_length=120)
    owner = models.CharField(max_length=120)
    url = models.URLField(default='Not available')
    coordinator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='coordinator')
    mentors = models.ManyToManyField(Mentor, blank=True, null=True)
    issues = models.PositiveSmallIntegerField(default = 0)
    forks = models.PositiveSmallIntegerField(default = 0)
    description = models.CharField(max_length=500, null=True,blank=True)
    lang = models.CharField(default = 'Unknown', max_length = 120)
    level1 = models.BooleanField(default=False)
    level2 = models.BooleanField(default=False)
    level3 = models.BooleanField(default=False)

    def __str__(self):
        return self.name
