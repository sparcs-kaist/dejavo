from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import _user_has_module_perms, _user_has_perm
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from dejavo.apps.zabo.models import Article

class ZaboUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        # TODO email validate
        user =  self.model(email = email,
                is_staff = is_staff,
                is_superuser = is_superuser,
                date_joined = now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Create profile
        profile = ZaboProfile.objects.create(user=user)
        profile.save()

        return user

    def create_user(self, email, password=None):
        return self._create_user(email, password, False, False, is_active=False)

    def create_superuser(self, email, password):
        return self._create_user(email, password, True, True, is_active=True)


class ZaboUser(AbstractBaseUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = ZaboUserManager()

    email = models.EmailField(_('email address'), blank=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    @property
    def username(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def as_json(self):
        return {
                'id' : self.id,
                'username' : self.email,
                'first_name' : self.first_name,
                'last_name' : self.last_name,
                'profile_image' : self.profile.profile_image.url,
                }


class ZaboProfile(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', unique=True)
    profile_image = models.ImageField(upload_to = 'profile', default='default_profile.png')
    phone = models.CharField(max_length = 50)
    bio = models.TextField()

ZaboUser.profile = property(lambda u: ZaboProfile.objects.get(user = u))


class RegistrationManager(models.Manager):

    def activate_user(self, key):
        return False

    def create_inactivate_user(self, user=None, send_email=True, request=None):
        return False


class RegistrationProfile(models.Model):
    objects = RegistrationManager()

    user = models.OneToOneField(ZaboUser)
    activation_key = models.CharField(_('activation_key'), max_length = 40)


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


class Participation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    article = models.ForeignKey(Article)

    class Meta:
        unique_together = (('user', 'article'))
