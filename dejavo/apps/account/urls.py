from django.conf.urls import patterns, include, url
from dejavo.apps.account import views

urlpatterns = patterns('',
    url(r'^$', views.main),
    url(r'^create/$', views.create),
    url(r'^edit/$', views.edit),
    url(r'^show/(?P<username>\w+)/$', views.show_user),
    url(r'^participate/(?P<article_id>\d+)/$', views.participate),
    url(r'^unparticipate/(?P<article_id>\d+)/$', views.unparticipate),
)
