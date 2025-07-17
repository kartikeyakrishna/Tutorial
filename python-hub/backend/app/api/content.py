from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db, limiter
from app.models.content import Tutorial, TutorialSection, Article, CodeSnippet
from app.schemas.content import TutorialSchema, TutorialSectionSchema, ArticleSchema, CodeSnippetSchema
from app.auth.roles import role_required
from sqlalchemy import desc
from math import ceil
from app.services.meili import index_tutorial, update_tutorial, delete_tutorial, index_article, update_article, delete_article, index_snippet, update_snippet, delete_snippet

content_bp = Blueprint('content', __name__, url_prefix='/api')

# --- Tutorials ---
@content_bp.route('/tutorials', methods=['GET'])
@limiter.limit('30 per minute')
def list_tutorials():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    q = Tutorial.query
    # Filtering
    if 'author_id' in request.args:
        q = q.filter_by(author_id=request.args['author_id'])
    if 'difficulty_level' in request.args:
        q = q.filter_by(difficulty_level=request.args['difficulty_level'])
    if 'language' in request.args:
        q = q.filter_by(language=request.args['language'])
    if 'is_published' in request.args:
        q = q.filter_by(is_published=request.args.get('is_published') == 'true')
    # Sorting
    if request.args.get('sort') == 'newest':
        q = q.order_by(desc(Tutorial.created_at))
    total = q.count()
    tutorials = q.paginate(page=page, per_page=per_page, error_out=False).items
    schema = TutorialSchema(many=True)
    return jsonify({
        'items': schema.dump(tutorials),
        'total': total,
        'page': page,
        'pages': ceil(total / per_page)
    })

@content_bp.route('/tutorials', methods=['POST'])
@jwt_required()
@limiter.limit('10 per minute')
def create_tutorial():
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    schema = TutorialSchema()
    try:
        validated = schema.load(data)
    except Exception as e:
        abort(400, description=str(e))
    tutorial = Tutorial(**validated, author_id=user_id)
    db.session.add(tutorial)
    db.session.commit()
    index_tutorial(schema.dump(tutorial))
    return jsonify(schema.dump(tutorial)), 201

@content_bp.route('/tutorials/<int:tutorial_id>', methods=['GET'])
@limiter.limit('30 per minute')
def get_tutorial(tutorial_id):
    tutorial = Tutorial.query.get(tutorial_id)
    if not tutorial:
        abort(404, description='Tutorial not found')
    schema = TutorialSchema()
    return jsonify(schema.dump(tutorial))

@content_bp.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
@jwt_required()
@limiter.limit('10 per minute')
def update_tutorial(tutorial_id):
    user_id = get_jwt_identity()['id']
    tutorial = Tutorial.query.get(tutorial_id)
    if not tutorial:
        abort(404, description='Tutorial not found')
    if tutorial.author_id != user_id:
        abort(403, description='Not authorized')
    data = request.get_json()
    schema = TutorialSchema()
    try:
        validated = schema.load(data, partial=True)
    except Exception as e:
        abort(400, description=str(e))
    for key, value in validated.items():
        setattr(tutorial, key, value)
    db.session.commit()
    update_tutorial(schema.dump(tutorial))
    return jsonify(schema.dump(tutorial))

@content_bp.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit('5 per minute')
def delete_tutorial(tutorial_id):
    user_id = get_jwt_identity()['id']
    tutorial = Tutorial.query.get(tutorial_id)
    if not tutorial:
        abort(404, description='Tutorial not found')
    if tutorial.author_id != user_id:
        abort(403, description='Not authorized')
    db.session.delete(tutorial)
    db.session.commit()
    delete_tutorial(tutorial_id)
    return jsonify({'msg': 'Tutorial deleted'})

# --- Articles ---
@content_bp.route('/articles', methods=['GET'])
@limiter.limit('30 per minute')
def list_articles():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    q = Article.query
    if 'author_id' in request.args:
        q = q.filter_by(author_id=request.args['author_id'])
    if 'category' in request.args:
        q = q.filter_by(category=request.args['category'])
    if 'is_featured' in request.args:
        q = q.filter_by(is_featured=request.args.get('is_featured') == 'true')
    if request.args.get('sort') == 'newest':
        q = q.order_by(desc(Article.created_at))
    total = q.count()
    articles = q.paginate(page=page, per_page=per_page, error_out=False).items
    schema = ArticleSchema(many=True)
    return jsonify({
        'items': schema.dump(articles),
        'total': total,
        'page': page,
        'pages': ceil(total / per_page)
    })

@content_bp.route('/articles', methods=['POST'])
@jwt_required()
@limiter.limit('10 per minute')
def create_article():
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    schema = ArticleSchema()
    try:
        validated = schema.load(data)
    except Exception as e:
        abort(400, description=str(e))
    article = Article(**validated, author_id=user_id)
    db.session.add(article)
    db.session.commit()
    index_article(schema.dump(article))
    return jsonify(schema.dump(article)), 201

@content_bp.route('/articles/<int:article_id>', methods=['GET'])
@limiter.limit('30 per minute')
def get_article(article_id):
    article = Article.query.get(article_id)
    if not article:
        abort(404, description='Article not found')
    schema = ArticleSchema()
    return jsonify(schema.dump(article))

@content_bp.route('/articles/<int:article_id>', methods=['PUT'])
@jwt_required()
@limiter.limit('10 per minute')
def update_article(article_id):
    user_id = get_jwt_identity()['id']
    article = Article.query.get(article_id)
    if not article:
        abort(404, description='Article not found')
    if article.author_id != user_id:
        abort(403, description='Not authorized')
    data = request.get_json()
    schema = ArticleSchema()
    try:
        validated = schema.load(data, partial=True)
    except Exception as e:
        abort(400, description=str(e))
    for key, value in validated.items():
        setattr(article, key, value)
    db.session.commit()
    update_article(schema.dump(article))
    return jsonify(schema.dump(article))

@content_bp.route('/articles/<int:article_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit('5 per minute')
def delete_article(article_id):
    user_id = get_jwt_identity()['id']
    article = Article.query.get(article_id)
    if not article:
        abort(404, description='Article not found')
    if article.author_id != user_id:
        abort(403, description='Not authorized')
    db.session.delete(article)
    db.session.commit()
    delete_article(article_id)
    return jsonify({'msg': 'Article deleted'})

# --- Code Snippets ---
@content_bp.route('/code-snippets', methods=['GET'])
@limiter.limit('30 per minute')
def list_code_snippets():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    q = CodeSnippet.query
    if 'author_id' in request.args:
        q = q.filter_by(author_id=request.args['author_id'])
    if 'language' in request.args:
        q = q.filter_by(language=request.args['language'])
    if 'is_public' in request.args:
        q = q.filter_by(is_public=request.args.get('is_public') == 'true')
    if request.args.get('sort') == 'newest':
        q = q.order_by(desc(CodeSnippet.created_at))
    total = q.count()
    snippets = q.paginate(page=page, per_page=per_page, error_out=False).items
    schema = CodeSnippetSchema(many=True)
    return jsonify({
        'items': schema.dump(snippets),
        'total': total,
        'page': page,
        'pages': ceil(total / per_page)
    })

@content_bp.route('/code-snippets', methods=['POST'])
@jwt_required()
@limiter.limit('10 per minute')
def create_code_snippet():
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    schema = CodeSnippetSchema()
    try:
        validated = schema.load(data)
    except Exception as e:
        abort(400, description=str(e))
    snippet = CodeSnippet(**validated, author_id=user_id)
    db.session.add(snippet)
    db.session.commit()
    index_snippet(schema.dump(snippet))
    return jsonify(schema.dump(snippet)), 201

@content_bp.route('/code-snippets/<int:snippet_id>', methods=['GET'])
@limiter.limit('30 per minute')
def get_code_snippet(snippet_id):
    snippet = CodeSnippet.query.get(snippet_id)
    if not snippet:
        abort(404, description='Code snippet not found')
    schema = CodeSnippetSchema()
    return jsonify(schema.dump(snippet))

@content_bp.route('/code-snippets/<int:snippet_id>', methods=['PUT'])
@jwt_required()
@limiter.limit('10 per minute')
def update_code_snippet(snippet_id):
    user_id = get_jwt_identity()['id']
    snippet = CodeSnippet.query.get(snippet_id)
    if not snippet:
        abort(404, description='Code snippet not found')
    if snippet.author_id != user_id:
        abort(403, description='Not authorized')
    data = request.get_json()
    schema = CodeSnippetSchema()
    try:
        validated = schema.load(data, partial=True)
    except Exception as e:
        abort(400, description=str(e))
    for key, value in validated.items():
        setattr(snippet, key, value)
    db.session.commit()
    update_snippet(schema.dump(snippet))
    return jsonify(schema.dump(snippet))

@content_bp.route('/code-snippets/<int:snippet_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit('5 per minute')
def delete_code_snippet(snippet_id):
    user_id = get_jwt_identity()['id']
    snippet = CodeSnippet.query.get(snippet_id)
    if not snippet:
        abort(404, description='Code snippet not found')
    if snippet.author_id != user_id:
        abort(403, description='Not authorized')
    db.session.delete(snippet)
    db.session.commit()
    delete_snippet(snippet_id)
    return jsonify({'msg': 'Code snippet deleted'}) 