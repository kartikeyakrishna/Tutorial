from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import abort

ROLES = ['admin', 'moderator', 'user']

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if 'role' not in claims or claims['role'] not in roles:
                abort(403, description='Insufficient permissions')
            return fn(*args, **kwargs)
        return wrapper
    return decorator 