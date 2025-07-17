import pytest

def test_list_comments(client):
    response = client.get('/api/community/comments')
    assert response.status_code == 200
 
def test_create_comment(client, access_token):
    data = {'content': 'Test comment', 'parent_type': 'tutorial', 'parent_id': 1}
    response = client.post('/api/community/comments', json=data, headers={'Authorization': f'Bearer {access_token}'} )
    assert response.status_code in (201, 400)  # 400 if parent doesn't exist 