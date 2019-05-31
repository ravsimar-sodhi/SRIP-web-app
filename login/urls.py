from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views
# from mysite.core import views as core_views

urlpatterns = [
    # url(r'^$', views.home, name='home'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='main/home.html'), name='logout'),
    url(r'^is_registered', views.is_registered),
    # url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]