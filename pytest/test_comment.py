def test_add_comment(client):
    client.post('/register', json={'name': 'cuser', 'password': '123', 'photo_url': ''})
    login_res = client.post('/login', json={'name': 'cuser', 'password': '123'})
    user_id = login_res.get_json()['user_id']
    post_res = client.post('/posts', json={'user_id': user_id, 'content': 'Test'})
    post_id = post_res.get_json()['post_id']

    res = client.post('/comments', json={
        'post_id': post_id,
        'user_id': user_id,
        'content': 'Nice post!'
    })
    assert res.status_code == 200
    assert 'comment_id' in res.get_json()
