import re
from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import bcrypt
from datetime import timedelta
from flask import current_app
import secrets

def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password, rounds=12).decode('utf-8')

def check_password(password: str, hash_: str) -> bool:
    return bcrypt.check_password_hash(hash_, password)

def generate_access_token(identity, additional_claims=None):
    return create_access_token(identity=identity, expires_delta=timedelta(minutes=15), additional_claims=additional_claims)

def generate_refresh_token(identity):
    return create_refresh_token(identity=identity, expires_delta=timedelta(days=7))

def generate_email_token():
    return secrets.token_urlsafe(32)

def is_strong_password(password: str) -> bool:
    # At least 8 chars, 1 upper, 1 lower, 1 digit, 1 special
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:\\|,.<>\/?]).{8,}$', password)) 