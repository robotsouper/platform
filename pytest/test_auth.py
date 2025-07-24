def test_register(client):
    response = client.post('/register', json={
        'name': 'testuser',
        'password': 'testpass',
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User registered'

def test_login(client):
    client.post('/register', json={
        'name': 'testuser2',
        'password': 'testpass2',
        'photo_url': ''
    })

    response = client.post('/login', json={
        'name': 'testuser2',
        'password': 'testpass2'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()
