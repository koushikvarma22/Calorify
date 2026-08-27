def test_health_check(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    assert res.json['status'] == 'ok'

def test_create_and_update_user(client):
    payload = {
        'firebase_uid': 'test_uid_1',
        'name': 'Alex Runner',
        'email': 'alex@example.com',
        'calorie_goal': 2200
    }
    res = client.post('/api/users', json=payload)
    assert res.status_code == 200
    data = res.json
    assert data['firebase_uid'] == 'test_uid_1'
    assert data['calorie_goal'] == 2200

    # Retrieve user
    get_res = client.get('/api/users/test_uid_1')
    assert get_res.status_code == 200
    assert get_res.json['name'] == 'Alex Runner'
