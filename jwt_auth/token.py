#-*-coding:utf8-*-
import jwt

from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

from jwt_auth import utils
from jwt_auth.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

def generate_jwt(user):

    payload = jwt_payload_handler(user)

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    return {
        'token': jwt_encode_handler(payload),
        'user': user.as_json()
    }

def refresh_jwt(user, token):

    try:
        payload = jwt_decode_handler(token)
    except jwt.ExpiredSignature:
        msg = _('Signature has expired.')
        raise ValidationError(msg)
    except jwt.DecodeError:
        msg = _('Error decoding signature.')
        raise ValidationError(msg)

    # Make sure user exists (may want to refactor this)
    try:
        User = get_user_model()
        user_id = payload.get('user_id')

        if user_id is not None:
            user = User.objects.get(pk=user_id, is_active=True)
        else:
            msg = _('Invalid payload.')
            raise ValidationError(msg)

    except User.DoesNotExist:
        msg = _("User doesn't exist.")
        raise ValidationError(msg)

    # Get and check 'orig_iat'
    orig_iat = payload.get('orig_iat')

    if orig_iat:
        # Verify expiration
        refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA

        if isinstance(refresh_limit, timedelta):
            refresh_limit = (refresh_limit.days * 24 * 3600 +
                             refresh_limit.seconds)

        expiration_timestamp = orig_iat + int(refresh_limit)
        now_timestamp = timegm(datetime.utcnow().utctimetuple())

        if now_timestamp > expiration_timestamp:
            msg = _('Refresh has expired.')
            raise ValidationError(msg)
    else:
        msg = _('orig_iat field is required.')
        raise ValidationError(msg)

    new_payload = jwt_payload_handler(user)
    new_payload['orig_iat'] = orig_iat

    return {
        'token': jwt_encode_handler(new_payload),
        'user': user.as_json()
    }
