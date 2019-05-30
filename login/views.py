from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
# from django.contrib.auth import is_authenticated
from registration.models import Student

def log(request):
	if request.user.is_authenticated:
		print(request.user.username)
		try:
			student = Student.objects.get(handle=request.user.username)
		except Student.DoesNotExist:
			print("Does not exist")

	return redirect('/', message="hello")