# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length = 64)
    description = models.TextField()


class Poster(models.Model):
    article = models.ForeignKey(Article)
    poster_image = models.ImageField(upload_to="poster/")
