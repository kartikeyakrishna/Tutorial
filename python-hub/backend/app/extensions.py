from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_talisman import Talisman
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
talisman = Talisman()
ma = Marshmallow()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address)
csrf = CSRFProtect()

def test_db_connection(app):
    """Test DB connection by querying for User table."""
    try:
        with app.app_context():
            db.session.execute('SELECT 1')
        return True
    except Exception as e:
        app.logger.error(f"Database connection failed: {e}")
        return False 