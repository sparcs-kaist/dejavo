# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user")
    en_club_name = models.CharField(max_length = 32)
    ko_club_name = models.CharField(max_length = 32)
    profile_image = models.ImageField(upload_to="profile/", default="profile/no-img.jpg")
    bio = models.TextField()
