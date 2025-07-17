import logging
import logging.handlers
import json
import os
from pythonjsonlogger import jsonlogger
from flask import request

def setup_logging(app):
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'app.log')

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if app.config.get('DEBUG') else logging.INFO)
    console_handler.setFormatter(formatter)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers = []
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Flask request logging
    @app.before_request
    def log_request():
        app.logger.info({
            'event': 'request',
            'method': request.method,
            'path': request.path,
            'remote_addr': request.remote_addr,
            'args': request.args.to_dict(),
            'json': request.get_json(silent=True)
        })

    @app.after_request
    def log_response(response):
        app.logger.info({
            'event': 'response',
            'status': response.status_code,
            'path': request.path
        })
        return response 