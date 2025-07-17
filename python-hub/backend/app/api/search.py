from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.meili import search_tutorials, search_articles, search_snippets
from app.extensions import limiter

search_bp = Blueprint('search', __name__, url_prefix='/api/search')

@search_bp.route('/tutorials', methods=['GET'])
@limiter.limit('30 per minute')
def search_tutorials_api():
    q = request.args.get('q', '')
    filters = request.args.get('filters')
    facets = request.args.get('facets')
    result = search_tutorials(q, filters=filters, facets=facets)
    return jsonify(result)

@search_bp.route('/articles', methods=['GET'])
@limiter.limit('30 per minute')
def search_articles_api():
    q = request.args.get('q', '')
    filters = request.args.get('filters')
    facets = request.args.get('facets')
    result = search_articles(q, filters=filters, facets=facets)
    return jsonify(result)

@search_bp.route('/snippets', methods=['GET'])
@limiter.limit('30 per minute')
def search_snippets_api():
    q = request.args.get('q', '')
    filters = request.args.get('filters')
    facets = request.args.get('facets')
    result = search_snippets(q, filters=filters, facets=facets)
    return jsonify(result) 