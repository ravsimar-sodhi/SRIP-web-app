import requests
from django.shortcuts import render
from .models import LoggedIssue
from .forms import LoggedIssueForm, ReportForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from registration.models import Student
from gitlab import Gitlab

# Create your views here.
def home(request):
    orgs = ['virtual-labs', 'mozilla','google']
    res = {}
    data = github_search('', orgs, sort='forks')
    res['items'] = data[:6]
    dic = {'data':res}
    if request.user.is_authenticated:
        info = Student.objects.get(handle=request.user)
        dic['info'] = info
        return render(request, 'main/home.html',dic )
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

# def update_profile(request):
    # if request.method == 'POST':

def logissue(request):
    # if not (request.user.is_authenticated):
        # return render(request, 'main/home.html')
    if request.method == 'POST':
        form = LoggedIssueForm(request.POST)
        if form.is_valid():
            current_user = request.user
            cleaned_data = form.cleaned_data
            commit_id_form = cleaned_data.get('commit_id')
            url_form = cleaned_data.get('url')
            stud = Student.objects.get(handle=request.user.username)
            mentor_name = stud.mentor
            handle_form = stud.handle
            obj = LoggedIssue(user=current_user, commit_id=commit_id_form, url=url_form, mentor=mentor_name, handle=handle_form)
            try:
                obj.save()
            except:
                return HttpResponse('Already Existing Commit! Please resubmit with proper commit id')
            return HttpResponseRedirect('/')
        else:
            print('form invalid')
            return HttpResponse('Invalid Submission')
    else:
        form = LoggedIssueForm()
    return render(request, 'main/logissue.html', {'form': form})

def submitreport(request):
    # if not (request.user.is_authenticated):
        # return render(request, 'main/home.html')
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            report_url = cleaned_data.get('report')
            obj = Student.objects.get(handle = request.user.username)
            obj.report = report_url
            obj.save()
            return HttpResponseRedirect('/')
        else:
            print('form invalid')
            return HttpResponse('Invalid Submission')
    else:
        form = ReportForm()
        return render(request, 'main/report.html', {'form':form})

def man_hour_equivalent(x):
    mul_fac = 3
    j = 0.45
    power = mul_fac * j
    return ((x ** power)*160)/27

def calculate(request):

    pts_info = LoggedIssue.objects.filter(handle = request.user.username, is_added = True)
    len_com = len(pts_info)

    for i in range(len_com):
        html_ip = pts_info[i].html_ip
        css_ip = pts.info[i].css_ip
        js_ip = pts.info[i].js_ip
        py_ip = pts.info[i].py_ip
        pts_info[i].issue_points = html_ip + css_ip + js_ip + py_ip
        pts_info[i].save()

    total = 0
    html_ip = 0
    js_ip = 0
    css_ip = 0
    py_ip = 0
    try:
        total = pts_info[-1].issue_points
        html_ip = pts_info[-1].html_ip
        js_ip = pts_info[-1].js_ip
        css_ip = pts_info[-1].css_ip
        py_ip = pts_info[-1].py_ip
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
    calculate(request)
    info = Student.objects.get(handle = request.user.username)
    issue_info = LoggedIssue.objects.filter(user = request.user)

    # for i in range(len(issue_info)):
    if issue_info.exists():
        return render(request, 'main/performance.html', {'info': info, 'issue_info': issue_info})
    else:
        return HttpResponse("No Commit Logged Yet")
