from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db, limiter
from app.models.community import Comment, Vote
from app.schemas.community import CommentSchema, VoteSchema
from app.models.activity import ActivityLog
from datetime import datetime

community_bp = Blueprint('community', __name__, url_prefix='/api/community')

# --- Comment Endpoints ---
@community_bp.route('/comments', methods=['GET'])
@limiter.limit('30 per minute')
def list_comments():
    parent_type = request.args.get('parent_type')
    parent_id = request.args.get('parent_id')
    q = Comment.query
    if parent_type:
        q = q.filter_by(parent_type=parent_type)
    if parent_id:
        q = q.filter_by(parent_id=parent_id)
    comments = q.all()
    schema = CommentSchema(many=True)
    return jsonify(schema.dump(comments))

@community_bp.route('/comments', methods=['POST'])
@jwt_required()
@limiter.limit('10 per minute')
def create_comment():
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    schema = CommentSchema()
    try:
        validated = schema.load(data)
    except Exception as e:
        abort(400, description=str(e))
    comment = Comment(**validated, author_id=user_id, created_at=datetime.utcnow())
    db.session.add(comment)
    db.session.commit()
    # Activity log
    log = ActivityLog(user_id=user_id, session_id=None, interaction_type='comment_create', content=str(comment.id), activity_metadata=None, timestamp=datetime.utcnow(), created_at=datetime.utcnow())
    db.session.add(log)
    db.session.commit()
    return jsonify(schema.dump(comment)), 201

@community_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
@limiter.limit('10 per minute')
def update_comment(comment_id):
    user_id = get_jwt_identity()['id']
    comment = Comment.query.get(comment_id)
    if not comment or comment.author_id != user_id:
        abort(404, description='Comment not found or not authorized')
    data = request.get_json()
    schema = CommentSchema()
    try:
        validated = schema.load(data, partial=True)
    except Exception as e:
        abort(400, description=str(e))
    for key, value in validated.items():
        setattr(comment, key, value)
    comment.is_edited = True
    comment.edited_at = datetime.utcnow()
    db.session.commit()
    # Activity log
    log = ActivityLog(user_id=user_id, session_id=None, interaction_type='comment_update', content=str(comment.id), activity_metadata=None, timestamp=datetime.utcnow(), created_at=datetime.utcnow())
    db.session.add(log)
    db.session.commit()
    return jsonify(schema.dump(comment))

@community_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit('5 per minute')
def delete_comment(comment_id):
    user_id = get_jwt_identity()['id']
    comment = Comment.query.get(comment_id)
    if not comment or comment.author_id != user_id:
        abort(404, description='Comment not found or not authorized')
    db.session.delete(comment)
    db.session.commit()
    # Activity log
    log = ActivityLog(user_id=user_id, session_id=None, interaction_type='comment_delete', content=str(comment_id), activity_metadata=None, timestamp=datetime.utcnow(), created_at=datetime.utcnow())
    db.session.add(log)
    db.session.commit()
    return jsonify({'msg': 'Comment deleted'})

# --- Vote Endpoints ---
@community_bp.route('/votes', methods=['POST'])
@jwt_required()
@limiter.limit('10 per minute')
def create_vote():
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    schema = VoteSchema()
    try:
        validated = schema.load(data)
    except Exception as e:
        abort(400, description=str(e))
    # Prevent duplicate votes
    existing = Vote.query.filter_by(user_id=user_id, target_type=validated['target_type'], target_id=validated['target_id']).first()
    if existing:
        abort(400, description='Already voted')
    vote = Vote(**validated, user_id=user_id, created_at=datetime.utcnow())
    db.session.add(vote)
    db.session.commit()
    # Activity log
    log = ActivityLog(user_id=user_id, session_id=None, interaction_type='vote_create', content=str(vote.id), activity_metadata=None, timestamp=datetime.utcnow(), created_at=datetime.utcnow())
    db.session.add(log)
    db.session.commit()
    return jsonify(schema.dump(vote)), 201

@community_bp.route('/votes/<int:vote_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit('5 per minute')
def delete_vote(vote_id):
    user_id = get_jwt_identity()['id']
    vote = Vote.query.get(vote_id)
    if not vote or vote.user_id != user_id:
        abort(404, description='Vote not found or not authorized')
    db.session.delete(vote)
    db.session.commit()
    # Activity log
    log = ActivityLog(user_id=user_id, session_id=None, interaction_type='vote_delete', content=str(vote_id), activity_metadata=None, timestamp=datetime.utcnow(), created_at=datetime.utcnow())
    db.session.add(log)
    db.session.commit()
    return jsonify({'msg': 'Vote deleted'}) 