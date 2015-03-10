#-*-coding:utf8-*-

from requests import request, HTTPError

from django.core.files.base import ContentFile
from social.apps.django_app.utils import psa

def save_profile_picture(backend, user, response, details,
                         is_new=False,*args,**kwargs):

    if is_new and backend.name == 'facebook':
        url = 'https://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            user.profile.profile_image.save('{0}_social.jpg'.format(user.username),
                                   ContentFile(response.content))
            user.profile.save()
