from flask import Blueprint, request, jsonify, abort
from app.extensions import db, jwt, limiter
from app.models.user import User, UserProfile, UserPreferences
from app.schemas.user import UserSchema, UserProfileSchema, UserPreferencesSchema
from app.auth.utils import hash_password, check_password, generate_access_token, generate_refresh_token, generate_email_token, is_strong_password
from app.auth.email import send_verification_email, send_password_reset_email
from app.auth.roles import role_required
from app.auth.social import social_login_google, social_login_github
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from app.extensions import csrf
import functools

# Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Rate limiting
@limiter.limit('5 per minute')
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    if not email or not username or not password:
        abort(400, description='Missing required fields')
    if not is_strong_password(password):
        abort(400, description='Password is not strong enough')
    if User.query.filter((User.email == email) | (User.username == username)).first():
        abort(409, description='Email or username already exists')
    user = User(email=email, username=username, password_hash=hash_password(password))
    db.session.add(user)
    db.session.commit()
    # Create profile and preferences
    profile = UserProfile(user_id=user.id)
    preferences = UserPreferences(user_id=user.id)
    db.session.add(profile)
    db.session.add(preferences)
    db.session.commit()
    # Email verification
    token = generate_email_token()
    send_verification_email(user, token)
    return jsonify({'msg': 'Registration successful. Please verify your email.'}), 201

@limiter.limit('5 per minute')
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not check_password(password, user.password_hash):
        abort(401, description='Invalid credentials')
    if not user.is_active:
        abort(403, description='Account is inactive')
    access_token = generate_access_token({'id': user.id, 'role': user.role})
    refresh_token = generate_refresh_token({'id': user.id, 'role': user.role})
    response = jsonify({'access_token': access_token, 'refresh_token': refresh_token})
    set_access_cookies(response, access_token)
    return response

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = generate_access_token(identity)
    response = jsonify({'access_token': access_token})
    set_access_cookies(response, access_token)
    return response

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'msg': 'Logout successful'})
    unset_jwt_cookies(response)
    return response

@limiter.limit('5 per minute')
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        abort(404, description='User not found')
    token = generate_email_token()
    send_password_reset_email(user, token)
    return jsonify({'msg': 'Password reset email sent'})

@limiter.limit('5 per minute')
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')
    token = data.get('token')
    user = User.query.filter_by(email=email).first()
    if not user:
        abort(404, description='User not found')
    if not is_strong_password(new_password):
        abort(400, description='Password is not strong enough')
    user.password_hash = hash_password(new_password)
    db.session.commit()
    return jsonify({'msg': 'Password reset successful'})

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)
    if not user:
        abort(404, description='User not found')
    schema = UserSchema()
    return jsonify(schema.dump(user))

@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_me():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)
    if not user:
        abort(404, description='User not found')
    data = request.get_json()
    profile = user.profile
    if 'display_name' in data:
        profile.display_name = data['display_name']
    if 'bio' in data:
        profile.bio = data['bio']
    if 'avatar_url' in data:
        profile.avatar_url = data['avatar_url']
    if 'github_username' in data:
        profile.github_username = data['github_username']
    db.session.commit()
    return jsonify({'msg': 'Profile updated'})

@limiter.limit('5 per minute')
@auth_bp.route('/social/google', methods=['POST'])
def social_google():
    data = request.get_json()
    token = data.get('token')
    user_info = social_login_google(token)
    if not user_info:
        abort(401, description='Invalid Google token')
    # Find or create user logic here
    return jsonify({'msg': 'Google login not implemented'}), 501

@limiter.limit('5 per minute')
@auth_bp.route('/social/github', methods=['POST'])
def social_github():
    data = request.get_json()
    token = data.get('token')
    user_info = social_login_github(token)
    if not user_info:
        abort(401, description='Invalid GitHub token')
    # Find or create user logic here
    return jsonify({'msg': 'GitHub login not implemented'}), 501 