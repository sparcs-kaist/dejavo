#-*-coding:utf8-*-

from requests import request, HTTPError

from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from social.apps.django_app.utils import psa

def activate_new_user(backend, user, response, details,
                         is_new=False,*args,**kwargs):
    if is_new and backend.name == 'facebook':
        user.is_active = True
        user.save()

def save_profile_picture(backend, user, response, details,
                         is_new=False,*args,**kwargs):

    if is_new and backend.name == 'facebook':
        url = 'https://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            response = request('GET', url, params={'width': '320', 'height' : '320'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            user.profile.profile_image.save('{0}_social.jpg'.format(user.username),
                                   ContentFile(response.content))
            user.profile.save()

def check_fields(strategy, details, user=None, *args, **kwargs):

    if not user:
        fields = dict((name, kwargs.get(name) or details.get(name))
                        for name in ['email'])

        if fields['email'] == '':
            raise ValidationError("Email field does not exist")
