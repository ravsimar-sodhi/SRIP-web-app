from django.db import models
from mentor.models import Mentor
from registration.models import Student

# Create your models here.
class Project(models.Model):
    project_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=120)
    url = models.URLField()
    level = models.PositiveSmallIntegerField(choices=((1,"Easy"),(2, "Medium"), (3, "Hard")), default = 2)
    mentors = models.ManyToManyField(Mentor, blank=True, null=True)
    students = models.ManyToManyField(Student, blank=True,null=True)

    def __str__(self):
        return self.name