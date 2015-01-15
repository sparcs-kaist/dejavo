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

def user_to_json(self):
    return {
            'username' : self.username,
            'email' : self.email,
            'phone' : self.profile.phone,
            'bio' : self.profile.bio,
            }

# Add profile property to User model to create and read UserProfile easily
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
# Add class bound method 'as_json'
setattr(User, 'as_json', user_to_json)

class Notification(models.Model):

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'receiver')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'sender')
    title = models.CharField(max_length = 100) # title not for user, but system
    content = models.TextField(null = False)
    receive_date = models.DateTimeField(auto_now_add = True)

    def as_json(self):
        return {
                'title' : self.title,
                'sender' : {
                    'username' : self.sender.username,
                    'email' : self.sender.profile.profile_image.url,
                    },
                'content' : self.content,
                'receive_date' : self.receive_date,
                }
