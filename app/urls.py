from django.conf.urls import url
import django_cas_ng.views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about/$', views.about, name='about'),
    url(r'faq/$', views.faq, name='faq'),
    url(r'airport/open/$', views.open_airport, name='open_airport'),
    url(r'shopping/open/$', views.open_shopping, name='open_shopping'),
   	url(r'accounts/login/$', django_cas_ng.views.login),
   	url(r'accounts/logout/$', django_cas_ng.views.logout),
   ]
