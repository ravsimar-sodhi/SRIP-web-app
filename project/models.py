from django.db import models
from mentor.models import Mentor
from registration.models import Student, User
# Create your models here.
class Project(models.Model):
    coordinators = models.ManyToManyField(User,blank= True, null=True)
    name = models.CharField(max_length=120)
    owner = models.CharField(max_length=120)
    level = models.PositiveSmallIntegerField(choices=((1,"Easy"),(2, "Medium"), (3, "Hard")), default = 2)
    mentors = models.ManyToManyField(Mentor, blank=True, null=True)
    students = models.ManyToManyField(Student, blank=True,null=True)


    def __str__(self):
        return self.name