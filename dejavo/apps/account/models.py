# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

class Club(models.Model):

    en_name = models.CharField(max_length = 100)
    ko_name = models.CharField(max_length = 100)

class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user")
    club = models.ForeignKey(Club, related_name = "club", null=True)
    profile_image = models.ImageField(upload_to="profile/", default="profile/no-img.jpg")
    bio = models.TextField()
