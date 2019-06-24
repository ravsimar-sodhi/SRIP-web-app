
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.core.mail import EmailMessage
from datetime import datetime
from main.models import LoggedCommit
from .models import  Mentor, MentorForm, MentorProfileForm
from .forms import CommitEvaluationForm
from registration.models import User, Student

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
            email = EmailMessage('SRIP Registration Successful.',
            'Hello {0},\n\t You have been registered successfully.\n\tYou will be able to login once admin approves your registration.'.format(form.cleaned_data['handle']),
            to=[form.cleaned_data['email']],)
            email.send()

            # print('form valid')
            form.save()
            return HttpResponseRedirect('/')
        # else:
            # print('form invalid')
    else:
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
        mentor = Mentor.objects.get(handle=request.user)
        projects = mentor.project_set.all()
        print(projects)
        commits = LoggedCommit.objects.filter(project__in=projects)
        print(commits)
        # issue_info = LoggedCommit.objects.filter()
    else:
        messages.add_message(request, messages.ERROR, "You must be logged in as a Mentor in for this action", extra_tags = 'danger')

    return render(request, 'mentor/evaluation.html',{'commit_info': commits})

def review_commit(request, commit_id):
    if (not (request.user.is_authenticated)) or (request.user.role != 2):
        messages.add_message(request, messages.ERROR, "You must be logged in as a Mentor in for this action", extra_tags = 'danger')
        return render(request, 'main/evaluation.html')
    else:
        mentor = Mentor.objects.get(handle=request.user)
        projects = mentor.project_set.all()
        try:
            commit = LoggedCommit.objects.get(project__in=projects, commit_id = commit_id)
        except LoggedCommit.DoesNotExist:
            messages.add_message(request, messages.ERROR, "No such commit exists under your projects", extra_tags = 'danger')
            return render(request, 'main/evaluation.html')
        if request.method == "POST":
            form = CommitEvaluationForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                commit.html_ip = cleaned_data.get('html_fp')
                commit.css_ip = cleaned_data.get('css_fp')
                commit.js_ip = cleaned_data.get('js_fp')
                commit.py_ip = cleaned_data.get('py_fp')
                commit.status = cleaned_data.get('status')
                commit.remark = cleaned_data.get('remark')
                commit.evaluated_by = User.objects.get(username=request.user)
                commit.time_eval = datetime.now()
                try:
                    commit.save()
                    student = Student.objects.get(handle=commit.user)
                    emailID = student.email
                    email = EmailMessage('Commit reviewed successfully.',
                    'Hello {0},\n\tThe status of the commit {1} is {2}.'.format(commit.user, commit.commit_id, commit.status),
                    to=[emailID],)
                    email.send()

                    messages.add_message(request, messages.SUCCESS, "Commit Evaluated Successfully!")
                    return redirect('mentor/evaluate')
                except:
                    messages.add_message(request, messages.ERROR, "Commit not evaluated", extra_tags = 'danger')
            else:
                messages.add_message(request, messages.ERROR, "Invalid form submission", extra_tags = 'danger')
        else:
            form = CommitEvaluationForm(initial={'user': commit.user,
            'project':commit.project,
            'commit_id': commit.commit_id,
            'url':commit.url,
            'html_fp':commit.html_ip,
            'css_fp':commit.css_ip,
            'js_fp':commit.js_ip,
            'py_fp':commit.py_ip,
            'status': commit.status,
            'remark': commit.remark})
    return render(request, 'mentor/evaluation_form.html', {'form': form})