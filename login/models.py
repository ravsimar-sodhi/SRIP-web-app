from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class custom_user(User):
	REGISTRATION_STATUS = (
		('R', 'Rejected'),
		('P', 'Pending'),
		('A', 'Accepted'),
	)
	# user = models.OneToOneField(User, on_delete=models.CASCADE)
	approved = models.CharField(max_length=1, choices=REGISTRATION_STATUS, default='R')
