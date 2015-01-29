from settings import api_settings

import jwt
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

from jwt_auth.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

class JWTAuthMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):

        auth = request.META.get('HTTP_AUTHORIZATION', '').split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth or smart_text(auth[0].lower()) != auth_header_prefix:
            return

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            return
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            return

        try:
            payload = jwt_decode_handler(auth[1])
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            return
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            return

        # Remove if there is authorized session
        if request.user and request.session:
            request.session.flush()

        request.user = get_user_model()._default_manager.get(pk = payload.get('user_id'))
        return
