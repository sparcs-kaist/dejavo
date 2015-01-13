from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from dejavo.apps.zabo.models import Article

class UserProfile(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', unique=True)
    profile_image = models.ImageField(upload_to = 'profile', default='default_profile.png')
    phone = models.CharField(max_length = 50)
    bio = models.TextField()
    bookmark = models.ManyToManyField(Article)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Notification(models.Model):

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'receiver')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'sender')
    title = models.CharField(max_length = 100) # title not for user, but system
    content = models.TextField(null = False)
    receive_date = models.DateTimeField(auto_now_add = True)
