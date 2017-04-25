from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import django_cas_ng.views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about/$', views.about, name='about'),
    url(r'faq/$', views.faq, name='faq'),
    url(r'airport/open/$', views.open_airport, name='open_airport'),
    url(r'airport/open/select/(?P<ride_id>[0-9]+)$', views.join_airport_ride, name='join_airport_ride'),
    url(r'airport/open/select/confirm/(?P<ride_id>[0-9]+)$', views.confirm_join_airport, name='confirm_join_airport'),
    url(r'airport/open/new$', views.open_airport_new, name='open_airport_new'),
    url(r'^airport/open/new/confirm$', views.confirm_new_airport, name='confirm_new_airport'),
    url(r'airport/open/new/confirm/confirmation$', views.confirmation_new_airport, name='confirmation_new_airport'),
    url(r'shopping/open/$', views.open_shopping, name='open_shopping'),
    url(r'other/open/$', views.open_other, name='open_other'),
   	url(r'accounts/login/$', django_cas_ng.views.login),
   	url(r'accounts/logout/$', django_cas_ng.views.logout),
   ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
