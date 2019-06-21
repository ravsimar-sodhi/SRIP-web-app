from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect
from .models import StudentForm, Student, StudentProfileForm
from django.contrib import messages
from mentor.models import Mentor
from django.core.mail import EmailMessage


def register_student(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST, request.FILES)
        # check whether it's valid:

        if form.is_valid():
            form.save()
            email = EmailMessage('SRIP Registration Successful.',
           'Hello {0},\n\t You have been registered successfully.\n\tYou will be able to login once admin approves your registration.'.format(form.cleaned_data['handle']),
           to=[form.cleaned_data['email']],)
            email.send()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    return render(request, 'registration/register.html', {'form': form})


def create_user(request, strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}
    flag = 0
    try:
        instance = Student.objects.get(handle=details.get('username'))
    except Student.DoesNotExist:
        try:
            instance = Mentor.objects.get(handle = details.get('username'))
        except Mentor.DoesNotExist:
            messages.info(request, "You are not registered with SRIP.")
            return redirect('/')

    if instance.status == "REJECTED":
        return render_to_response('main/home.html', {'regstatus': 'Rejected'})
    elif instance.status == "PENDING":
        return render_to_response('main/home.html', {'regstatus': 'Pending'})
    else:
        USER_FIELDS = ['username','email',]
        fields = dict(
                (name, kwargs.get(name, details.get(name))
                 )
                      for name in USER_FIELDS)
        if not fields:
            return
        fields['role'] = instance.role
        return {'is_new': True, 'user': strategy.create_user(**fields)}


def profile_student(request):
    instance = Student.objects.get(handle=request.user)
    form = StudentProfileForm(instance=instance)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if 'resume' not in request.FILES:
            request.FILES['resume'] = instance.resume
        if 'st_id' not in request.FILES:
            request.FILES['st_id'] = instance.st_id

        if form.is_valid():
            student = instance
            student.name = form.cleaned_data['name']
            student.email = form.cleaned_data['email']
            student.rollno = form.cleaned_data['rollno']
            student.area_interest = form.cleaned_data['area_interest']
            student.branch_year = form.cleaned_data['branch_year']
            student.clg_name = form.cleaned_data['clg_name']
            student.st_id = request.FILES['st_id']
            student.resume = request.FILES['resume']
            student.save()
            return HttpResponseRedirect('/')

    else:
        form = StudentProfileForm(instance=instance)
    return render(request, 'registration/profile.html', {'form':form})