from marshmallow import Schema, fields, validate
from app.models.progress import UserProgress, Bookmark

class UserProgressSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    tutorial_id = fields.Int(required=True)
    completed_sections = fields.Str()
    completion_percentage = fields.Float()
    last_accessed = fields.DateTime(allow_none=True)
    completed_at = fields.DateTime(allow_none=True)

class BookmarkSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    content_type = fields.Str(required=True, validate=validate.Length(max=32))
    content_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True) 