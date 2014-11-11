from django.conf.urls import patterns, include, url
from dejavo.apps.account import views

urlpatterns = patterns('',
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^ch_passwd/', views.ch_passwd),
    url(r'^$', views.main),
)
