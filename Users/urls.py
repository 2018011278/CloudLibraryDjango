from django.conf.urls import url
from . import views

app_name = 'Users'
urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/change/$', views.change_profile, name='change_profile'),
    url(r'^(?P<pk>\d+)$', views.info_detail_view, name='info_detail'),
    url(r'^verify/$', views.verify, name='verify'),
]
