from django.shortcuts import render
import requests
from .models import LoggedIssue
from .forms import LoggedIssueForm
from django.http import HttpResponseRedirect
from registration.models import Student

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def gitlab_search(keyword):
    gl = gitlab.Gitlab('https://gitlab.com', private_token = 'bqfyAiHKF_zT1EFxT_Mz')
    gl.auth()
    data = gl.search('projects', keyword)
    for x in data:
        x['full_name'] = x['name']
        x["language"] = "NA"
        x["updated_at"] = x['last_activity_at']
        x['html_url'] = x['http_url_to_repo']
    return data

def github_search(keyword, username):
    url = "https://api.github.com/search/repositories?q=" + keyword +"+user:" + username
    r = requests.get(url = url)
    data = r.json()
    return data['items']

def search(request):
    keyword = request.GET['searchword']
    # data = gitlab_search(keyword)
    data = github_search(keyword, "virtual-labs")
    res = {}
    res['items'] = data
    return render(request, 'main/home.html', {'data': res})

def logissue(request):
    if request.method == 'POST':
        # request.POST['user'] = request.user
        # request.POST['mentor'] = 'Mentor'
        form = LoggedIssueForm(request.POST)
        if form.is_valid():
            current_user = request.user
            cleaned_data = form.cleaned_data
            commit_id_form = cleaned_data.get('commit_id')
            url_form = cleaned_data.get('url')
            mentor_name = Student.objects.get(handle=request.user.username).mentor
            handle_form = Student.objects.get(handle=request.user.username).handle
            obj = LoggedIssue(user=current_user, commit_id=commit_id_form, url=url_form, mentor=mentor_name, handle=handle_form)
            try:
                obj.save()
            except:
                return HttpResponse('Already Existing Commit! Please resubmit with proper commit id')
        else:
            print('here')
    else:
        form = LoggedIssueForm()
    return render(request, 'main/logissue.html', {'form': form})