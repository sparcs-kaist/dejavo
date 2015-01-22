from django.conf.urls import patterns, include, url
from dejavo.apps.zabo import views

urlpatterns = patterns('',
    url(r'^create/$', views.create),
    url(r'^(?P<article_id>\d+)/$', views.view_article),
    url(r'^(?P<article_id>\d+)/edit/$', views.edit_article), # editing page

    url(r'^(?P<article_id>\d+)/timeslot/create/$', views.create_timeslot),
    url(r'^(?P<article_id>\d+)/timeslot/delete/(?P<timeslot_id>\d+)/$', views.delete_timeslot),

    url(r'^(?P<article_id>\d+)/qna/$', views.view_qna),
    url(r'^(?P<article_id>\d+)/qna/create/$', views.create_question),
    url(r'^(?P<article_id>\d+)/qna/load/$', views.load_question),
    url(r'^(?P<article_id>\d+)/qna/delete/(?P<question_id>\d+)/$', views.delete_question),

    url(r'^(?P<article_id>\d+)/qna/(?P<question_id>\d+)/create/$', views.create_answer),
    url(r'^(?P<article_id>\d+)/qna/(?P<question_id>\d+)/delete/(?P<answer_id>\d+)/$', views.delete_answer),

    # When updating annoucement (not in editting page), changer can choose 
    # to notify participants
    url(r'^(?P<article_id>\d+)/announcement/edit/$', views.edit_announcement),
)
