#-*-coding:utf8-*-
import jwt

from datetime import datetime

from jwt_auth.settings import api_settings

def jwt_payload_handler(user):
    try:
        username = user.get_username()
    except AttributeError:
        username = user.username

    return {
        'user_id': user.pk,
        'email': user.email,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

def jwt_encode_handler(payload):
    return jwt.encode(
        payload,
        api_settings.JWT_SECRET_KEY,
        api_settings.JWT_ALGORITHM
    ).decode('utf-8')

def jwt_decode_handler(token):
    return jwt.decode(
        token,
        api_settings.JWT_SECRET_KEY,
        api_settings.JWT_VERIFY,
        verify_expiration=api_settings.JWT_VERIFY_EXPIRATION,
        leeway=api_settings.JWT_LEEWAY
    )
