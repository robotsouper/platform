def test_create_post(client):
    # Create user first
    client.post('/register', json={
        'name': 'poster',
        'password': '1234',
        'photo_url': ''
    })
    login_res = client.post('/login', json={'name': 'poster', 'password': '1234'})
    user_id = login_res.get_json()['user_id']

    response = client.post('/posts', json={
        'user_id': user_id,
        'content': 'Hello world!',
        'image_urls': '../app/staitc/photos/user/1.jpg'
    })
    assert response.status_code == 200
    assert 'post_id' in response.get_json()
