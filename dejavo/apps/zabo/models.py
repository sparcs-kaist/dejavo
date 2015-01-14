from django.db import models
from django.conf import settings

class Article(models.Model):

    CATEGORY_TYPE = (
            ('event', 'Event'),
            ('recruit', 'Recruit'),
            )

    owner = models.ManyToManyField(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length = 150)
    location = models.CharField(max_length = 200)
    content = models.TextField()
    category = models.CharField(max_length = 20, choices = CATEGORY_TYPE)
    # Article creation timestamp
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True, auto_now_add = True)


class Contact(models.Model):

    CONTACT_TYPE = (
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('facebook', 'Facebook'),
            ('twitter', 'Twitter'),
            ('url', 'URL'),
            ('etc', 'Etc'),
            )

    article = models.ForeignKey(Article, related_name = 'contact')
    contact_type = models.CharField(max_length = 20, choices = CONTACT_TYPE)
    info = models.CharField(max_length = 200)


class Timeslot(models.Model):

    TIMESLOT_TYPE = (
            ('point', 'Point'),
            ('range', 'Range'),
            )

    article = models.ForeignKey(Article, related_name = 'timeslot')
    timeslot_type = models.CharField(max_length = 20, choices = TIMESLOT_TYPE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null = True)
    label = models.CharField(max_length = 50)


class Poster(models.Model):
    image = models.ImageField(upload_to = 'poster')
    alert = models.CharField(max_length = 150)
    article = models.ForeignKey(Article, related_name = 'images')


class Attachment(models.Model):
    filepath = models.FileField(upload_to = 'attachment')
    article = models.ForeignKey(Article, related_name = 'attachment')


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
