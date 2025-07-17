from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db, limiter
from app.models.activity import ActivityLog
from app.schemas.activity import ActivityLogSchema
from datetime import datetime

activity_bp = Blueprint('activity', __name__, url_prefix='/api/activity')

@activity_bp.route('/log', methods=['POST'])
@jwt_required()
@limiter.limit('20 per minute')
def log_activity():
    user_id = get_jwt_identity().get('id')
    data = request.get_json()
    schema = ActivityLogSchema()
    try:
        validated = schema.load(data)
    except Exception as e:
        abort(400, description=str(e))
    log = ActivityLog(
        session_id=validated['session_id'],
        user_id=user_id,
        interaction_type=validated.get('interaction_type'),
        content=validated.get('content'),
        activity_metadata=validated.get('activity_metadata'),
        timestamp=datetime.utcnow(),
        created_at=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()
    return jsonify(schema.dump(log)), 201

@activity_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    user_id = get_jwt_identity().get('id')
    sessions = db.session.query(ActivityLog.session_id).filter_by(user_id=user_id).distinct().all()
    return jsonify({'sessions': [s[0] for s in sessions]})

@activity_bp.route('/sessions/<string:session_id>', methods=['GET'])
@jwt_required()
def get_session_logs(session_id):
    user_id = get_jwt_identity().get('id')
    logs = ActivityLog.query.filter_by(user_id=user_id, session_id=session_id).all()
    schema = ActivityLogSchema(many=True)
    return jsonify(schema.dump(logs)) 