from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect
from .models import StudentForm, Student, ProfileForm, MentorForm, Mentor
# from .forms import MentorRegistrationForm

def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST, request.FILES)
        # check whether it's valid:

        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')
        else:
            print('here')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    return render(request, 'registration/register.html', {'form': form})

def register_mentor(request):
    print('pls')
    if request.method == 'POST':
        form = MentorForm(request.POST)
        if form.is_valid():
            print('form valid')
            form.save()
            return HttpResponseRedirect('../')
        else:
            print('form invalid')
    else:
        print('x')
        form = MentorForm()
    return render(request, 'registration/register_mentor.html', {'form': form})

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}
    flag = 0

    try:
        print('x')
        instance = Student.objects.get(handle=details.get('username'))
    except Student.DoesNotExist:
        try:
            print('h')
            instance = Mentor.objects.get(handle = details.get('username'))
        except Mentor.DoesNotExist:
            return redirect('/register')

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


def profile(request):
    instance = Student.objects.filter(handle=request.user).first()
    form = ProfileForm(instance=instance)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if 'resume' not in request.FILES:
            request.FILES['resume'] = instance.resume
        if 'st_id' not in request.FILES:
            request.FILES['st_id'] = instance.st_id

        if form.is_valid():
            student = Student.objects.filter(handle=request.user).first()
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
        form = ProfileForm(instance=instance)
    return render(request, 'registration/profile.html', {'form':form})