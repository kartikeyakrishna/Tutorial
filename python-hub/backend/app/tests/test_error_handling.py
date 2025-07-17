def test_404_error(client):
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Not Found' 