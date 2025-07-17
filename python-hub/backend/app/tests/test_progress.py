import pytest

def test_list_progress(client, access_token):
    response = client.get('/api/progress', headers={'Authorization': f'Bearer {access_token}'} )
    assert response.status_code == 200
 
def test_list_bookmarks(client, access_token):
    response = client.get('/api/progress/bookmarks', headers={'Authorization': f'Bearer {access_token}'} )
    assert response.status_code == 200 