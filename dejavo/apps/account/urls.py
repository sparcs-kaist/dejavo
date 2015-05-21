from django.conf.urls import patterns, include, url
from dejavo.apps.account import views
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    url(r'^$', views.main, name='account_main'),
    url(r'^articles/$', views.my_articles),
#   url(r'^profile/$', views.my_profile),
    url(r'^participation/$', views.my_p_articles),
    url(r'^register/$', views.register),
    url(r'^email_check/$', views.email_check),
    url(r'^activate/(?P<activation_key>\w+)/$', views.activate, name='registration_activate'),
    url(r'^edit/$', views.edit),
    url(r'^show/(?P<username>\w+)/$', views.show_user),
    url(r'^search/$', views.search_user),
    url(r'^participate/(?P<article_id>\d+)/$', views.participate),
    url(r'^check_participate/(?P<article_id>\d+)/$', views.check_participate),
    url(r'^unparticipate/(?P<article_id>\d+)/$', views.unparticipate),

    url(r'^login_form/$', TemplateView.as_view(template_name='account/login_form.html')),
    url(r'^registration_form/$', TemplateView.as_view(template_name='account/registration_form.html')),
)
