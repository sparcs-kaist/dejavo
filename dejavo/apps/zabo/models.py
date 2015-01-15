from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site

import os

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

    def as_json(self):

        owner_list = []
        for owner in list(self.owner.all()):
            owner_list.append(owner.username)

        contact_list = []
        for contact in list(Contact.objects.filter(article = self)):
            contact_list.append({
                'contact_type' : contact.contact_type,
                'info' : contact.info
                })

        timeslot_list = []
        for timeslot in list(Timeslot.objects.filter(article = self)):
            timeslot_list.append({
                'timeslot_type' : timeslot.timeslot_type,
                'start_time' : timeslot.start_time,
                'end_time' : timeslot.end_time,
                'label' : timeslot.label,
                })

        poster_list = []
        for poster in list(Poster.objects.filter(article = self)):
            poster_list.append({
                'image_url' : poster.image.url,
                'alert' : poster.alert,
                })

        attach_list = []
        for attach in list(Attachment.objects.filter(article = self)):
            attach_list.append({
                'file_url' : attach.filepath.url,
                'filename' : os.path.basename(attach.filepath.file.name),
                })

        return {
                'title' : self.title,
                'owner' : owner_list,
                'category' : self.category,
                'created_date' : self.created_date,
                'updated_date' : self.updated_date,
                'content' : self.content,
                'contact' : contact_list,
                'timeslot' : timeslot_list,
                'poster' : poster_list,
                'attachment' : attach_list,
                }


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

    def as_json(self):
        return {
                'title' : self.title,
                'writer' : {
                    'username' : self.writer.username,
                    'image_url' : self.writer.profile.profile_image.url,
                    },
                'created_date' : self.created_date,
                'updated_date' : self.updated_date,
                }


class Question(models.Model):
    article = models.ForeignKey(Article)
    content = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True, auto_now_add = True)

    def as_json(self):

        answer_list = []
        for answer in list(Answer.objects.filter(question = self)):
            answer_list.append({
                'writer' : {
                    'username' : answer.writer.username,
                    'image_url' : answer.wirter.profile.profile_image.url,
                    },
                'created_date' : answer.created_date,
                'content' : answer.content,
                })

        return {
                'title' : self.title,
                'content' : self.content,
                'created_date' : self.created_date,
                'answer' : answer_list,
                }


class Answer(models.Model):
    question = models.ForeignKey(Question)
    content = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True, auto_now_add = True)
