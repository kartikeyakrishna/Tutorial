import pytest

def test_list_tutorials(client):
    response = client.get('/api/tutorials')
    assert response.status_code == 200

def test_list_articles(client):
    response = client.get('/api/articles')
    assert response.status_code == 200

def test_list_code_snippets(client):
    response = client.get('/api/code-snippets')
    assert response.status_code == 200
