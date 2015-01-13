from django.conf.urls import patterns, include, url
from dejavo.apps.manage import views

urlpatterns = patterns('',
    url(r'^$', views.main),
)
