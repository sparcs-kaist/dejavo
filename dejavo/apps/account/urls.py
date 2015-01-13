from django.conf.urls import patterns, include, url
from dejavo.apps.account import views

urlpatterns = patterns('',
    url(r'^$', views.main),
    url(r'^create/$', views.create),
    url(r'^edit/$', views.edit),
    url(r'^unsubscribe/$', views.unsubscribe),
)
