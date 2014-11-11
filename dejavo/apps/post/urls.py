from django.conf.urls import patterns, include, url
from dejavo.apps.post import views

urlpatterns = patterns('',
    url(r'category/', views.category),
    url(r'club/', views.club),
    url(r'register/', views.register),
    url(r'search/', views.search),
    url(r'^$', views.main_redirect),
)
