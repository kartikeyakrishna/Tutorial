from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.user import User, UserProfile, UserPreferences
import re

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(max=255))
    username = fields.Str(required=True, validate=[validate.Length(min=3, max=64)])
    is_active = fields.Bool(dump_only=True)
    is_verified = fields.Bool(dump_only=True)
    role = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('username')
    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValidationError('Username must be alphanumeric with underscores only.')

class UserProfileSchema(Schema):
    user_id = fields.Int(dump_only=True)
    display_name = fields.Str(validate=validate.Length(max=128))
    bio = fields.Str(validate=validate.Length(max=1000))
    avatar_url = fields.Url(allow_none=True)
    github_username = fields.Str(validate=validate.Length(max=64))
    learning_streak = fields.Int(dump_only=True)
    total_tutorials_completed = fields.Int(dump_only=True)

class UserPreferencesSchema(Schema):
    user_id = fields.Int(dump_only=True)
    theme = fields.Str(validate=validate.OneOf(['light', 'dark']))
    email_notifications = fields.Bool()
    language_preference = fields.Str(validate=validate.Length(max=32)) 