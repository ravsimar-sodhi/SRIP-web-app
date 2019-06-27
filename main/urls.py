from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('oauth/', include('social_django.urls', namespace = 'social')),
    path('search', views.search, name = 'search'),
    path('portal/logcommit', views.logcommit, name='logcommit'),
    path('portal/report', views.submitreport, name='submitreport'),
    path('portal/performance/', views.displaypoints, name = 'displaypoints'),
    path('portal/leaderboard/', views.leaderboard, name = 'leaderboard'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='main/home.html'), name='logout'),
]