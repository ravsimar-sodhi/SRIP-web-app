from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import StudentForm, Student, ProfileForm

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
        # else:
        #     print('here')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    return render(request, 'registration/register.html', {'form': form})

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}
    flag = 0
    for x in Student.objects.filter(status = "APPROVED"):
        if details.get('username') == x.handle:
            flag = 1
            print("Matched")

    if flag == 0:
        return redirect('/register')

    # print(details)
    USER_FIELDS = ['username','email']
    fields = dict(
            (name, kwargs.get(name, details.get(name))
             )
                  for name in USER_FIELDS)
    if not fields:
        return
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