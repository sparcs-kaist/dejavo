from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from dejavo.apps.zabo.models import Article
from django.db.models.signals import post_save

class UserProfile(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', unique=True)
    profile_image = models.ImageField(upload_to = 'profile', default='default_profile.png')
    phone = models.CharField(max_length = 50)
    bio = models.TextField()
    participation = models.ManyToManyField(Article)

def post_save_user(signal, sender, instance, **kwargs):
    created = kwargs['created']

    if created:
        profile = UserProfile.objects.create(user=instance)

post_save.connect(post_save_user, sender=settings.AUTH_USER_MODEL)

def user_to_json(self):
    return {
            'id' : self.id,
            'username' : self.username,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'profile_image' : self.profile.profile_image.url,
            }

# Add profile property to User model to create and read UserProfile easily
User.profile = property(lambda u: UserProfile.objects.get(user = u))
# Add class bound method 'as_json'
setattr(User, 'as_json', user_to_json)

class Notification(models.Model):

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'receiver')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'sender')
    title = models.CharField(max_length = 100) # title not for user, but system
    content = models.TextField(null = False)
    receive_date = models.DateTimeField(auto_now_add = True)
    is_read = models.BooleanField(default = False)

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
