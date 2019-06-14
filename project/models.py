from django.db import models
from mentor.models import Mentor
from registration.models import Student

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=120)
    url = models.URLField()
    level = models.PositiveSmallIntegerField(choices=((1,"Easy"),(2, "Medium"), (3, "Hard")), default = 2)
    mentors = models.ManyToManyField(Mentor)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name