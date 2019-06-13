from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def home(request):
    dic = {}
    if request.user.is_authenticated and request.user.role == 2:
        info = Mentor.objects.get(handle = request.user)
        dic['info'] = info
    return render(request, 'mentor/home.html', dic)