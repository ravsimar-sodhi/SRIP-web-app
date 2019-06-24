import requests
from gitlab import Gitlab
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import LoggedCommit
from .forms import LoggedCommitForm, ReportForm
from registration.models import Student
from mentor.models import Mentor
from project.models import Project
from django.core.mail import EmailMessage

def home(request):
    if request.user.is_authenticated and request.user.role == 2:
        return HttpResponseRedirect('/mentor')
    orgs = ['virtual-labs', 'mozilla','google']
    res = {}
    data = github_search('', orgs, sort='forks')
    res['items'] = data[:6]
    dic = {'data':res}
    if request.user.is_authenticated:
        try:
            info = Student.objects.get(handle=request.user)
        except Student.DoesNotExist:
            print(request.user)
            info = Mentor.objects.get(handle=request.user)
        dic['info'] = info
    return render(request, 'main/home.html', dic)

def gitlab_search(keyword):
    gl = Gitlab('https://gitlab.com', private_token = 'bqfyAiHKF_zT1EFxT_Mz')
    gl.auth()
    data = gl.search('projects', keyword)
    for x in data:
        x['full_name'] = x['name']
        x["language"] = "NA"
        x["updated_at"] = x['last_activity_at']
        x['html_url'] = x['http_url_to_repo']
    return data

def github_search(keyword, orgs, sort=None):
    url = "https://api.github.com/search/repositories?q=" + keyword
    for username in orgs:
        url += "+user:" + username
    if sort is not None:
        url += "&sort:" + sort +"&order=desc"
    r = requests.get(url = url)
    data = r.json()
    return data['items']

def search(request):
    keyword = request.GET['searchword']
    # data = gitlab_search(keyword)
    orgs = ['virtual-labs', 'mozilla','google']
    data = github_search(keyword, orgs)
    res = {}
    res['items'] = data
    return render(request, 'main/search.html', {'data': res})


def leaderboard(request):
    students = Student.objects.all().order_by('-effort')
    return render(request, 'main/leaderboard.html', {'students': students})


def logcommit(request):
    if (not (request.user.is_authenticated)) or (request.user.role != 1):
        messages.add_message(request, messages.ERROR, "You must be logged in as student in for this action", extra_tags = 'danger')
        return render(request, 'main/home.html')
    if request.method == 'POST':
        form = LoggedCommitForm(request.POST)
        if form.is_valid():
            current_user = request.user
            cleaned_data = form.cleaned_data
            commit_id_form = cleaned_data.get('commit_id')
            url_form = cleaned_data.get('url')
            stud = Student.objects.get(handle=request.user.username)
            # mentor_name = stud.mentor
            project = Project.objects.get(project_id= cleaned_data.get('project_id'))
            obj = LoggedCommit(user=current_user, commit_id=commit_id_form, url=url_form, project= project)
            try:
                obj.save()
                email = EmailMessage('Commit Logged Successfully.',
               'Hello {0},\n\tYour commit has been submitted successfully.\n\tYou will be notified once it is evaluated.'.format(stud.handle),
               to=[stud.email],)
                email.send()
                messages.add_message(request, messages.SUCCESS, "Commit Logged Successfully!")
                messages.add_message(request, messages.SUCCESS, "Commit Logged Successfully!")
                return redirect('/portal/performance')
            except:
                messages.add_message(request, messages.ERROR, "Already existing commit! Please resubmit with a unique commit ID", extra_tags = 'danger')
        else:
            messages.add_message(request, messages.ERROR, "Invalid form submission", extra_tags = 'danger')
    else:
        form = LoggedCommitForm()
    return render(request, 'main/logcommit.html', {'form': form})

def submitreport(request):
    if (not (request.user.is_authenticated)) or (request.user.role != 1):
        messages.add_message(request, messages.ERROR, "You must be logged in as student in for this action", extra_tags = 'danger')
        return render(request, 'main/home.html')
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            report_url = cleaned_data.get('report')
            obj = Student.objects.get(handle = request.user.username)
            obj.report = report_url
            obj.save()
            messages.add_message(request, messages.SUCCESS, "Report Link submitted Successfully!")
            return redirect(request, 'main/performance.html')
        else:
            messages.add_message(request, messages.ERROR, "Invalid form submission", extra_tags = 'danger')
    else:
        form = ReportForm()
        return render(request, 'main/report.html', {'form':form})

def man_hour_equivalent(x):
    mul_fac = 3
    j = 0.45
    power = mul_fac * j
    res = ((x**power)*160)/27
    print(res)
    return ((x ** power)*160)/27

def calculate(request):

    pts_info = LoggedCommit.objects.filter(user = request.user, status = "APPROVED")
    len_com = len(pts_info)

    for i in range(len_com):
        html_ip = pts_info[i].html_ip
        css_ip = pts_info[i].css_ip
        js_ip = pts_info[i].js_ip
        py_ip = pts_info[i].py_ip
        pts_info[i].issue_points = html_ip + css_ip + js_ip + py_ip
        pts_info[i].save()

    total = 0
    html_ip = 0
    js_ip = 0
    css_ip = 0
    py_ip = 0
    try:
        ind = len(pts_info) -1
        total = pts_info[ind].issue_points
        html_ip = pts_info[ind].html_ip
        js_ip = pts_info[ind].js_ip
        css_ip = pts_info[ind].css_ip
        py_ip = pts_info[ind].py_ip
    except:
        pass

    user_info = Student.objects.get(handle = (request.user.username))
    user_info.function_points = total
    mh = man_hour_equivalent(html_ip)
    mh += man_hour_equivalent(css_ip)
    mh += man_hour_equivalent(js_ip)
    mh += man_hour_equivalent(py_ip)
    user_info.effort = mh
    user_info.save()

def displaypoints(request):
    if (not (request.user.is_authenticated)) or (request.user.role != 1):
        messages.add_message(request, messages.ERROR, "You must be logged in as student in for this action", extra_tags = 'danger')
        return render(request, 'main/home.html')
    calculate(request)
    info = Student.objects.get(handle = request.user.username)
    issue_info = LoggedCommit.objects.filter(user = request.user)

    # for i in range(len(issue_info)):
    if issue_info.exists():
        return render(request, 'main/performance.html', {'info': info, 'issue_info': issue_info})
    else:
        messages.add_message(request, messages.ERROR, "No Commit Logged yet", extra_tags = 'danger')
        return render(request, 'main/home.html', {'info': info})