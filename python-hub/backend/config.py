from decouple import config
import os

class BaseConfig:
    """Base configuration with defaults."""
    SECRET_KEY = config('SECRET_KEY', default='super-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='jwt-secret-key')
    CORS_ORIGINS = config('CORS_ORIGINS', default='*')
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://redis:6379/0')
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://redis:6379/0') 
    # Add more shared config as needed

class DevelopmentConfig(BaseConfig):
    """Development config: uses localhost DB by default."""
    SQLALCHEMY_DATABASE_URI = config(
        'DEV_DATABASE_URL',
        default='postgresql://postgres:postgres@localhost:5432/postgres'
    )

class DockerConfig(BaseConfig):
    """Docker Compose config: uses 'db' service name."""
    SQLALCHEMY_DATABASE_URI = config(
        'DOCKER_DATABASE_URL',
        default='postgresql://postgres:postgres@db:5432/postgres'
    )

class ProductionConfig(BaseConfig):
    """Production config: expects DATABASE_URL env var (e.g., Railway)."""
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')

class TestingConfig(BaseConfig):
    """Testing config: uses SQLite in-memory DB."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

# Environment detection logic
def get_config():
    env = os.environ.get('PYTHON_HUB_ENV', '').lower()
    if env == 'production':
        return ProductionConfig
    elif env == 'docker':
        return DockerConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig

# Configuration validation utility
def validate_config(cfg):
    required = ['SQLALCHEMY_DATABASE_URI', 'SECRET_KEY', 'JWT_SECRET_KEY']
    for key in required:
        if not getattr(cfg, key, None):
            raise RuntimeError(f"Missing required config: {key}") 