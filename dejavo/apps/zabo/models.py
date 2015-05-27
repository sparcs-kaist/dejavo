# -*- coding: utf-8

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from sorl.thumbnail import ImageField, get_thumbnail

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
    announcement = models.TextField(blank = True)
    image = models.ImageField(upload_to = 'poster')
    category = models.CharField(max_length = 20, choices = CATEGORY_TYPE)
    # Article host group
    host_name = models.CharField(max_length = 50)
    host_image = models.ImageField(upload_to = 'host', default='default/default_host.png')
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

    def as_json(self, ex = []):

        owner_list = []
        for owner in list(self.owner.all()):
            owner_list.append(owner.id)

        contact_list = []
        for contact in list(Contact.objects.filter(article = self)):
            contact_list.append({
                'contact_type' : contact.contact_type,
                'info' : contact.info
                })

        timeslot_list = []
        timeslot_q_list = list(Timeslot.objects.filter(article = self).order_by('-start_time'))
        for timeslot in timeslot_q_list:
            timeslot_list.append({
                'timeslot_type' : timeslot.timeslot_type,
                'start_time' : timeslot.start_time,
                'end_time' : timeslot.end_time,
                'label' : timeslot.label,
                })

        attach_list = []
        for attach in list(Attachment.objects.filter(article = self)):
            attach_list.append({
                'file_url' : attach.filepath.url,
                'filename' : os.path.basename(attach.filepath.file.name),
                })

        poster = {'origin' : None, 'main_thumb' : None, 'category_thumb': None }
        if (bool(self.image)):
            poster['origin'] = self.image.url
            poster['main_thumb'] = get_thumbnail(self.image, '600', quality=85).url

            is_portrait = self.image.width < self.image.height
            to_scale = [222, 321] if is_portrait else [468, 321]
            geometry = None
            scale = 1

            height = self.image.height
            width = self.image.width

            if width > to_scale[0] or height > to_scale[1]:
                if height > to_scale[1]:
                    scale = height / to_scale[1]
                    height /= scale
                    width /= scale
                if width > to_scale[0]:
                    scale = width / to_scale[0]
                    height /= scale
                    width /= scale

                geometry = str(width) + 'x' + str(height)

            poster['category_thumb'] = get_thumbnail(self.image, geometry, quality=85).url

        ctx = {
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
                'poster' : poster,
                'host' : {
                    'name' : self.host_name,
                    'image' : None if not bool(self.host_image) else self.host_image.url,
                    'description' : self.host_description,
                    },
                'attachment' : attach_list,
                }

        for elem in ex:
            ctx.pop(elem)

        return ctx

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
    is_main = models.BooleanField(default = False)
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
                    'id' : answer.writer.id,
                    'image_url' : answer.writer.profile.profile_image.url,
                    'first_name' : self.writer.first_name,
                    'last_name' : self.writer.last_name,
                    },
                'created_date' : answer.created_date,
                'content' : answer.content,
                'id' : answer.id,
                })

        return {
                'id' : self.id,
                'writer' : {
                    'id' : self.writer.id,
                    'first_name' : self.writer.first_name,
                    'last_name' : self.writer.last_name,
                    'image_url' : self.writer.profile.profile_image.url,
                    },
                'content' : self.content,
                'created_date' : self.created_date,
                'answer' : answer_list,
                }

    def __unicode__(self):
        return self.article.title + ' ::' + str(self.id) + ' ::' + self.writer.email


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
                    'id' : self.writer.id,
                    'image_url' : self.writer.profile.profile_image.url,
                    'first_name' : self.writer.first_name,
                    'last_name' : self.writer.last_name,
                    },
                'created_date' : self.created_date,
                'content' : self.content,
                'id': self.id,
            }
