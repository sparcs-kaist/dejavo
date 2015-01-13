from django.conf.urls import patterns, include, url
from dejavo.apps.zabo import views

urlpatterns = patterns('',
    url(r'^create/$', views.create),
    url(r'^(?P<article_id>\d+)/$', views.view_article),
    url(r'^(?P<article_id>\d+)/edit/$', views.edit_article),

    url(r'^(?P<article_id>\d+)/qna/$', views.view_qna),
    url(r'^(?P<article_id>\d+)/qna/create/$', views.create_qna),
    url(r'^(?P<article_id>\d+)/qna/(?P<question_id>\d+)/delete$', views.delete_question),
    url(r'^(?P<article_id>\d+)/qna/(?P<question_id>\d+)/edit$', views.edit_question),

    url(r'^(?P<article_id>\d+)/qna/(?P<question_id>\d+)/create/$', views.create_answer),
    url(r'^(?P<article_id>\d+)/qna/(?P<question_id>\d+)/(?P<answer_id>\d+)/delete/$', views.delete_answer),
    url(r'^(?P<article_id>\d+)/qna/(?P<question_id>\d+)/(?P<answer_id>\d+)/edit/$', views.edit_answer),

    url(r'^(?P<article_id>\d+)/announcement/create/$', views.create_announcement),
    url(r'^(?P<article_id>\d+)/announcement/(?P<announcement_id>\d+)/delete/$', views.delete_announcement),
    url(r'^(?P<article_id>\d+)/announcement/(?P<announcement_id>\d+)/edit/$', views.edit_announcement),
)
