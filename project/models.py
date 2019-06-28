from django.db import models
from django.conf import settings
from mentor.models import Mentor
from registration.models import Student
from django.contrib.auth.models import Group
# Create your models here.


class Project(models.Model):
    coordinator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='coordinator')
    name = models.CharField(max_length=120)
    owner = models.CharField(max_length=120)
    level = models.PositiveSmallIntegerField(choices=((1,"1"),(2, "2"), (3, "3")), default = 2)
    mentors = models.ManyToManyField(Mentor, blank=True, null=True)

    def __str__(self):
        return self.name
