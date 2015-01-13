from django.db import models
from django.conf import settings

class Article(models.Model):

    DATE_TYPE = (
            ('point', 'Point'),
            ('range', 'Range'),
            )

    CATEGORY_TYPE = (
            ('event', 'Event'),
            ('recruit', 'Recruit'),
            )

    owner = models.ManyToManyField(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length = 150)
    location = models.CharField(max_length = 200)
    content = models.TextField()
    category = models.CharField(max_length = 20, choices = CATEGORY_TYPE)
    # Date of Article
    date_type = models.CharField(max_length = 20, choices = DATE_TYPE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # Article creation timestamp
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True, auto_now_add = True)


class Poster(models.Model):
    image = models.ImageField(upload_to = 'poster')
    alert = models.CharField(max_length = 150)
    post = models.ForeignKey(Article, related_name = 'images')


class Announcement(models.Model):
    article = models.ForeignKey(Article)
    title = models.CharField(max_length = 150)
    content = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True, auto_now_add = True)


class Question(models.Model):
    article = models.ForeignKey(Article)
    content = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True, auto_now_add = True)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    content = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True, auto_now_add = True)
