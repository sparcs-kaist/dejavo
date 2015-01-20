from django.conf.urls import patterns, include, url
from dejavo.apps.manage import views

urlpatterns = patterns('',
    url(r'^$', views.main),

    url(r'^claim/$', views.list_claim),
    url(r'^claim/(?P<claim_id>\d+)/$', views.view_claim),

    url(r'^log/$', views.list_log),

    url(r'^block/$', views.list_block),
    url(r'^block/article/(?P<article_id>\d+)/$', views.set_article_block),
    url(r'^block/account/(?P<account_id>\d+)/$', views.set_account_block),
)
