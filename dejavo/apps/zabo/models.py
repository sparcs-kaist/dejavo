# -*- coding: utf-8

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

import os
import datetime


class Article(models.Model):

    CATEGORY_TYPE = (
            ('recruit', '리쿠르팅'),
            ('performance', '공연'),
            ('competition', '대회'),
            ('display', '전시'),
            ('briefing', '설명회'),
            ('lecture', '강연'),
            ('event', '행사'),
            ('etc', '기타'),
            )

    owner = models.ManyToManyField(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length = 150)
    subtitle = models.CharField(max_length = 150, blank = True)
    location = models.CharField(max_length = 200, blank = True)
    content = models.TextField()
    announcement = models.TextField()
    image = models.ImageField(upload_to = 'poster')
    category = models.CharField(max_length = 20, choices = CATEGORY_TYPE)
    # Article host group
    host_name = models.CharField(max_length = 50)
    host_image = models.ImageField(upload_to = 'host')
    host_description = models.CharField(max_length = 150)
    is_blocked = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)
    is_published = models.BooleanField(default = False)
    # Article creation timestamp
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True, auto_now_add = True)

    def set_fields(self, fields, posts, files):
        for field_name in fields:
            if field_name == 'created_date' or field_name == 'updated_date':
                continue

            field = Article._meta.get_field(field_name)
            _type = type(field)

            if _type == models.ImageField:
                if field_name not in files:
                    raise ValidationError({field_name : 'Invalid value'})
                setattr(self, field_name, files[field_name])

            else:
                if field_name not in posts:
                    raise ValidationError({field_name : 'Invalid value'})

                if _type == models.BooleanField:
                    setattr(self, field_name,
                            True if posts.get(field_name, 'false') == 'true' \
                                    else False)
                else:
                    setattr(self, field_name, posts[field_name])

    def clean(self):

        if self.is_published:
            unsatisfied_field = {}
            if self.title.strip() == '':
                unsatisfied_field['title'] = 'Unfilled field'
            if self.content.strip() == '':
                unsatisfied_field['content'] = 'Unfilled field'
            if not self.category:
                unsatisfied_field['category'] = 'Value not set'

            if len(unsatisfied_field) > 0:
                raise ValidationError(unsatisfied_field)

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
        timeslot_q_list = list(Timeslot.objects.filter(article = self))
        for timeslot in timeslot_q_list:
            timeslot_list.append({
                'timeslot_type' : timeslot.timeslot_type,
                'start_time' : timeslot.start_time,
                'end_time' : timeslot.end_time,
                'label' : timeslot.label,
                })

        d_day = 999
        day = ""
        for timeslot in timeslot_q_list:
            delta = timeslot.start_time.replace(tzinfo=None) - datetime.datetime.now()
            if delta.days > 0:
                day = timeslot.start_time.strftime("%m월 %d일")
                d_day = delta.days
                pass

        attach_list = []
        for attach in list(Attachment.objects.filter(article = self)):
            attach_list.append({
                'file_url' : attach.filepath.url,
                'filename' : os.path.basename(attach.filepath.file.name),
                })

        return {
                'id' : self.id,
                'title' : self.title,
                'subtitle' : self.subtitle,
                'owner' : owner_list,
                'category' : self.get_category_display(),
                'location' : self.location,
                'announcement' : self.announcement,
                'created_date' : self.created_date,
                'updated_date' : self.updated_date,
                'content' : self.content,
                'contact' : contact_list,
                'timeslot' : timeslot_list,
                'poster' : None if not bool(self.image) else self.image.url,
                'host' : {
                    'name' : self.host_name,
                    'image' : None if not bool(self.host_image) else self.host_image.url,
                    'description' : self.host_description,
                    },
                'attachment' : attach_list,
                'd_day': d_day,
                'day': day,
                }

    def __unicode__(self):
        return unicode(self.title) + ' ::' + str(self.id)


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
    end_time = models.DateTimeField(blank = True, null = True)
    label = models.CharField(max_length = 50, blank = True)

    def as_json(self):
        return {
                'id' : self.id,
                'type' : self.timeslot_type,
                'start_time' : self.start_time,
                'end_time' : self.end_time,
                'label' : self.label,
            }


class Attachment(models.Model):
    filepath = models.FileField(upload_to = 'attachment')
    article = models.ForeignKey(Article, related_name = 'attachment')


class Question(models.Model):
    article = models.ForeignKey(Article)
    content = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_blocked = models.BooleanField(default = False)
    is_private = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)
    created_date = models.DateTimeField(auto_now_add = True)

    def clean(self):
        if self.content.strip() == '':
            raise ValidationError({'content': 
                'Content should not be empty string'})

    def as_json(self):

        answer_list = []
        for answer in list(Answer.objects.filter(question = self)):
            answer_list.append({
                'writer' : {
                    'username' : answer.writer.username,
                    'image_url' : answer.writer.profile.profile_image.url,
                    },
                'created_date' : answer.created_date,
                'content' : answer.content,
                })

        return {
                'content' : self.content,
                'created_date' : self.created_date,
                'answer' : answer_list,
                }

    def __unicode__(self):
        return self.article.title + ' ::' + str(self.id) + ' ::' + self.writer.username


class Answer(models.Model):
    question = models.ForeignKey(Question)
    content = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add = True)
    is_blocked = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)

    def clean(self):
        if self.content.strip() == '':
            raise ValidationError({'content': 
                'Content should not be empty string'})

    def as_json(self):
        return {
                'writer' : {
                    'username' : self.writer.username,
                    'image_url' : self.writer.profile.profile_image.url,
                    },
                'created_date' : self.created_date,
                'content' : self.content,
            }
