from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db, limiter
from app.models.user import User, UserProfile, UserPreferences
from app.schemas.user import UserSchema, UserProfileSchema, UserPreferencesSchema
from app.auth.roles import role_required
from app.models.activity import ActivityLog
from app.schemas.activity import ActivityLogSchema
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/me', methods=['GET'])
@jwt_required()
@limiter.limit('20 per minute')
def get_me():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)
    if not user:
        abort(404, description='User not found')
    schema = UserSchema()
    return jsonify(schema.dump(user))

@user_bp.route('/me', methods=['PUT'])
@jwt_required()
@limiter.limit('10 per minute')
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

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@limiter.limit('20 per minute')
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description='User not found')
    schema = UserSchema()
    return jsonify(schema.dump(user))

@user_bp.route('/me', methods=['DELETE'])
@jwt_required()
@limiter.limit('5 per minute')
def delete_me():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)
    if not user:
        abort(404, description='User not found')
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'Account deleted'})

@user_bp.route('/preferences', methods=['POST'])
@jwt_required()
@limiter.limit('10 per minute')
def update_preferences():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)
    if not user:
        abort(404, description='User not found')
    data = request.get_json()
    preferences = user.preferences
    schema = UserPreferencesSchema()
    try:
        validated = schema.load(data, partial=True)
    except Exception as e:
        abort(400, description=str(e))
    for key, value in validated.items():
        setattr(preferences, key, value)
    db.session.commit()
    return jsonify({'msg': 'Preferences updated'}) 