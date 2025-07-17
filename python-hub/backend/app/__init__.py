from .extensions import db, migrate, jwt, cors, talisman, ma, bcrypt, limiter, csrf
from flask import Flask
from config import get_config, validate_config
import logging

def create_app(config_class=None):
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    else:
        cfg = get_config()
        validate_config(cfg)
        app.config.from_object(cfg)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    talisman.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from .api import activity_bp, user_bp, content_bp, progress_bp, community_bp
    app.register_blueprint(activity_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(community_bp)
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    from .api import search_bp
    app.register_blueprint(search_bp)

    # Register error handlers
    from .error_handlers import register_error_handlers
    register_error_handlers(app)

    # Setup logging
    from .log_config import setup_logging
    setup_logging(app)

    # Setup Swagger/OpenAPI
    from .swagger import setup_swagger
    setup_swagger(app)

    return app 