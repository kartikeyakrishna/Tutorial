from marshmallow import Schema, fields, validate
from app.models.content import Tutorial, TutorialSection, Article, CodeSnippet

class TutorialSectionSchema(Schema):
    id = fields.Int(dump_only=True)
    tutorial_id = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(max=255))
    content = fields.Str()
    order_index = fields.Int()
    code_examples = fields.Str()

class TutorialSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=255))
    description = fields.Str()
    content = fields.Str()
    author_id = fields.Int(required=True)
    difficulty_level = fields.Str(validate=validate.OneOf(['beginner', 'intermediate', 'advanced']))
    estimated_time = fields.Int()
    language = fields.Str(validate=validate.Length(max=32))
    is_published = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    sections = fields.List(fields.Nested(TutorialSectionSchema), dump_only=True)

class ArticleSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=255))
    content = fields.Str(required=True)
    author_id = fields.Int(required=True)
    category = fields.Str(validate=validate.Length(max=64))
    tags = fields.Str()
    is_featured = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class CodeSnippetSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=255))
    code = fields.Str(required=True)
    language = fields.Str(validate=validate.Length(max=32))
    author_id = fields.Int(required=True)
    is_public = fields.Bool()
    description = fields.Str()
    created_at = fields.DateTime(dump_only=True)
 