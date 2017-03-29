from django.conf.urls import url
import django_cas_ng.views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
   	url(r'accounts/login/$', django_cas_ng.views.login),
   	url(r'accounts/logout/$', django_cas_ng.views.logout),
   ]
