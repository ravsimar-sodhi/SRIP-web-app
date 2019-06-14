from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from .models import  Mentor, MentorForm, MentorProfileForm
from main.models import LoggedIssue
# Create your views here.
def home(request):
    dic = {}
    if request.user.is_authenticated and request.user.role == 2:
        info = Mentor.objects.get(handle = request.user)
        dic['info'] = info
    return render(request, 'mentor/home.html', dic)

def register_mentor(request):
    if request.method == 'POST':
        form = MentorForm(request.POST)
        if form.is_valid():
            print('form valid')
            form.save()
            return HttpResponseRedirect('/')
        else:
            print('form invalid')
    else:
        print('x')
        form = MentorForm()
    return render(request, 'registration/register.html', {'form': form})

def profile_mentor(request):
    instance = Mentor.objects.get(handle=request.user)
    form = MentorProfileForm(instance=instance)
    if request.method == 'POST':
        form = MentorProfileForm(request.POST, request.FILES)
        if form.is_valid():
            mentor = instance
            mentor.name = form.cleaned_data['name']
            mentor.email = form.cleaned_data['email']
            mentor.save()
            return HttpResponseRedirect('/')
    else:
        form = MentorProfileForm(instance=instance)
    return render(request, 'registration/profile.html', {'form':form})

def commit_evaluation(request):
    if request.user.is_authenticated and request.user.role == 2:
        # Get list of projects and query logged issues according 
        issue_info = LoggedIssue.objects.filter(mentor=request.user)
    else:
        messages.add_message(request, messages.ERROR, "You must be logged in as a Mentor in for this action", extra_tags = 'danger')

    return render(request, 'mentor/evaluation.html',{'issue_info': issue_info})
