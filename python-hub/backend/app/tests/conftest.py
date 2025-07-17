import pytest
from app import create_app, db as _db
from flask_jwt_extended import create_access_token
import os

@pytest.fixture(scope='session')
def app():
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app('TestingConfig')
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db(app):
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()

@pytest.fixture
def access_token():
    # Example user id 1
    return create_access_token(identity={'id': 1}) 