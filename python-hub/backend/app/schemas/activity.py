from marshmallow import Schema, fields
from app.models.activity import ActivityLog

class ActivityLogSchema(Schema):
    id = fields.Int(dump_only=True)
    session_id = fields.Str(required=True)
    user_id = fields.Int(allow_none=True)
    interaction_type = fields.Str()
    content = fields.Str()
    activity_metadata = fields.Str()
    timestamp = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True) 