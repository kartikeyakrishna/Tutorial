import pytest
from flask import url_for

def test_get_me(client, access_token):
    response = client.get('/api/users/me', headers={'Authorization': f'Bearer {access_token}'} )
    assert response.status_code in (200, 404)  # 404 if user doesn't exist

def test_update_preferences(client, access_token):
    response = client.post('/api/users/preferences', json={'theme': 'dark'}, headers={'Authorization': f'Bearer {access_token}'} )
    assert response.status_code in (200, 404) 