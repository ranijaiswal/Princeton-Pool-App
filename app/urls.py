from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import django_cas_ng.views
from . import views
from .views import RidesList

urlpatterns = [
    # url(r'^$', views.public_index, name='public_index'),
    url(r'^$', views.index, name='index'),
    url(r'about/$', views.about, name='about'),
    url(r'faq/$', views.faq, name='faq'),
    url(r'feedback/$', views.feedback, name='feedback'),
    url(r'feedback/thanks/$', views.feedback_thanks, name='feedback_thanks'),
    url(r'my-rides/$', views.my_rides, name='my_rides'),
    url(r'open/$', views.open_requests, name='open_requests'),
    url(r'open/select/(?P<ride_id>[0-9]+)$', views.join_ride, name='join_ride'),
    url(r'open/select/confirm/(?P<ride_id>[0-9]+)$', views.confirm_join_ride, name='confirm_join_ride'),
    url(r'my-rides/drop/(?P<ride_id>[0-9]+)$', views.drop_ride, name='drop_ride'),
    url(r'open/new/$', views.create_new_request, name='create_new_request'),
    url(r'open/new/confirm/$', views.confirm_new_request, name='confirm_new_request'),
    url(r'open/new/confirm/confirmation/$', views.confirmation_new_request, name='confirmation_new_request'),
   	url(r'accounts/login/$', django_cas_ng.views.login, name='login_view'),
   	url(r'accounts/logout/$', django_cas_ng.views.logout, name='logout_view'),
    url(r'^search/', RidesList.as_view(), name='rides_list')
   ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
