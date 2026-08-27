def test_daily_water_and_exercise(client):
    uid = 'test_uid_activity'
    res = client.post('/api/daily-log', json={
        'firebase_uid': uid,
        'water_ml': 1250,
        'exercise_minutes': 30
    })
    assert res.status_code == 200
    assert res.json['water_ml'] == 1250
    assert res.json['exercise_minutes'] == 30

    get_res = client.get(f'/api/daily-log/{uid}')
    assert get_res.status_code == 200
    assert get_res.json['water_ml'] == 1250
