import secrets
from flask import request
from functools import wraps
from app.utils.response import error_message
from jwt import (
    encode,
    decode,
    ExpiredSignatureError,
    InvalidTokenError,
)
from datetime import (
    datetime,
    timedelta,
)


secret_key = secrets.token_hex(16)

def encode_auth_token(user_id):
    """
    Generates the auth token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=720),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(f):
    """
    Decorator for decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authentication' in request.headers:
            token = request.headers['Authentication']

        if not token:
            return error_message(401, "Token is missing !!")

        try:
            payload = decode(
                token,
                secret_key,
                algorithms='HS256'
            )
            current_user = payload['sub']
        except ExpiredSignatureError:
            return error_message(401, 'Signature expired. Please log in again.')
        except InvalidTokenError:
            return error_message(401, 'Invalid token. Please log in again.')
        return f(current_user, *args, **kwargs)

    return decorated