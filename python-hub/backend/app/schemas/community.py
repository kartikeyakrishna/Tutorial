from marshmallow import Schema, fields, validate
from app.models.community import Comment, Vote

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    author_id = fields.Int(required=True)
    parent_type = fields.Str(required=True, validate=validate.Length(max=32))
    parent_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    is_edited = fields.Bool(dump_only=True)
    edited_at = fields.DateTime(allow_none=True)

class VoteSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    target_type = fields.Str(required=True, validate=validate.Length(max=32))
    target_id = fields.Int(required=True)
    vote_type = fields.Str(required=True, validate=validate.OneOf(['upvote', 'downvote']))
    created_at = fields.DateTime(dump_only=True) 