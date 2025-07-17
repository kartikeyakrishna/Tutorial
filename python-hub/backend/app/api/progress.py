from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db, limiter
from app.models.progress import UserProgress, Bookmark
from app.schemas.progress import UserProgressSchema, BookmarkSchema
from app.models.activity import ActivityLog
from app.schemas.activity import ActivityLogSchema
from datetime import datetime

progress_bp = Blueprint('progress', __name__, url_prefix='/api/progress')

# --- User Progress Endpoints ---
@progress_bp.route('', methods=['GET'])
@jwt_required()
@limiter.limit('30 per minute')
def list_progress():
    user_id = get_jwt_identity()['id']
    progress = UserProgress.query.filter_by(user_id=user_id).all()
    schema = UserProgressSchema(many=True)
    return jsonify(schema.dump(progress))

@progress_bp.route('', methods=['POST'])
@jwt_required()
@limiter.limit('10 per minute')
def create_progress():
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    schema = UserProgressSchema()
    try:
        validated = schema.load(data)
    except Exception as e:
        abort(400, description=str(e))
    progress = UserProgress(**validated, user_id=user_id, last_accessed=datetime.utcnow())
    db.session.add(progress)
    db.session.commit()
    # Activity log
    log = ActivityLog(user_id=user_id, session_id=None, interaction_type='progress_create', content=str(progress.id), activity_metadata=None, timestamp=datetime.utcnow(), created_at=datetime.utcnow())
    db.session.add(log)
    db.session.commit()
    return jsonify(schema.dump(progress)), 201

@progress_bp.route('/<int:progress_id>', methods=['GET'])
@jwt_required()
@limiter.limit('30 per minute')
def get_progress(progress_id):
    user_id = get_jwt_identity()['id']
    progress = UserProgress.query.get(progress_id)
    if not progress or progress.user_id != user_id:
        abort(404, description='Progress not found')
    schema = UserProgressSchema()
    return jsonify(schema.dump(progress))

@progress_bp.route('/<int:progress_id>', methods=['PUT'])
@jwt_required()
@limiter.limit('10 per minute')
def update_progress(progress_id):
    user_id = get_jwt_identity()['id']
    progress = UserProgress.query.get(progress_id)
    if not progress or progress.user_id != user_id:
        abort(404, description='Progress not found')
    data = request.get_json()
    schema = UserProgressSchema()
    try:
        validated = schema.load(data, partial=True)
    except Exception as e:
        abort(400, description=str(e))
    for key, value in validated.items():
        setattr(progress, key, value)
    progress.last_accessed = datetime.utcnow()
    db.session.commit()
    # Activity log
    log = ActivityLog(user_id=user_id, session_id=None, interaction_type='progress_update', content=str(progress.id), activity_metadata=None, timestamp=datetime.utcnow(), created_at=datetime.utcnow())
    db.session.add(log)
    db.session.commit()
    return jsonify(schema.dump(progress))

@progress_bp.route('/<int:progress_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit('5 per minute')
def delete_progress(progress_id):
    user_id = get_jwt_identity()['id']
    progress = UserProgress.query.get(progress_id)
    if not progress or progress.user_id != user_id:
        abort(404, description='Progress not found')
    db.session.delete(progress)
    db.session.commit()
    # Activity log
    log = ActivityLog(user_id=user_id, session_id=None, interaction_type='progress_delete', content=str(progress_id), activity_metadata=None, timestamp=datetime.utcnow(), created_at=datetime.utcnow())
    db.session.add(log)
    db.session.commit()
    return jsonify({'msg': 'Progress deleted'})

# --- Bookmark Endpoints ---
@progress_bp.route('/bookmarks', methods=['GET'])
@jwt_required()
@limiter.limit('30 per minute')
def list_bookmarks():
    user_id = get_jwt_identity()['id']
    bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
    schema = BookmarkSchema(many=True)
    return jsonify(schema.dump(bookmarks))

@progress_bp.route('/bookmarks', methods=['POST'])
@jwt_required()
@limiter.limit('10 per minute')
def create_bookmark():
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    schema = BookmarkSchema()
    try:
        validated = schema.load(data)
    except Exception as e:
        abort(400, description=str(e))
    bookmark = Bookmark(**validated, user_id=user_id)
    db.session.add(bookmark)
    db.session.commit()
    # Activity log
    log = ActivityLog(user_id=user_id, session_id=None, interaction_type='bookmark_create', content=str(bookmark.id), activity_metadata=None, timestamp=datetime.utcnow(), created_at=datetime.utcnow())
    db.session.add(log)
    db.session.commit()
    return jsonify(schema.dump(bookmark)), 201

@progress_bp.route('/bookmarks/<int:bookmark_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit('5 per minute')
def delete_bookmark(bookmark_id):
    user_id = get_jwt_identity()['id']
    bookmark = Bookmark.query.get(bookmark_id)
    if not bookmark or bookmark.user_id != user_id:
        abort(404, description='Bookmark not found')
    db.session.delete(bookmark)
    db.session.commit()
    # Activity log
    log = ActivityLog(user_id=user_id, session_id=None, interaction_type='bookmark_delete', content=str(bookmark_id), activity_metadata=None, timestamp=datetime.utcnow(), created_at=datetime.utcnow())
    db.session.add(log)
    db.session.commit()
    return jsonify({'msg': 'Bookmark deleted'}) 