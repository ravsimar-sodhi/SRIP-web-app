from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('oauth/', include('social_django.urls', namespace = 'social')),
    path('search', views.search, name = 'search')
]