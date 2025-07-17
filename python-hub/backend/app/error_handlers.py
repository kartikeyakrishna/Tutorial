from flask import jsonify
from werkzeug.exceptions import HTTPException
import traceback
import logging

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        app.logger.warning(f"HTTPException: {e.description}")
        response = e.get_response()
        response.data = jsonify({
            'error': e.name,
            'description': e.description,
            'code': e.code
        }).data
        response.content_type = "application/json"
        return response, e.code

    @app.errorhandler(Exception)
    def handle_exception(e):
        tb = traceback.format_exc()
        app.logger.error(f"Unhandled Exception: {str(e)}\n{tb}")
        return jsonify({
            'error': 'Internal Server Error',
            'description': str(e),
            'trace': tb
        }), 500 