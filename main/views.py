from django.shortcuts import render
import requests

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