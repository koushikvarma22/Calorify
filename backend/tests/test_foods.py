def test_add_and_list_foods(client):
    uid = 'test_uid_food'
    food_data = {
        'firebase_uid': uid,
        'food_name': 'Oatmeal with Honey',
        'meal': 'Breakfast',
        'calories': 250.0,
        'protein': 8.0,
        'carbs': 45.0,
        'fat': 4.0,
        'fiber': 5.0
    }
    res = client.post('/api/foods', json=food_data)
    assert res.status_code == 201
    item_id = res.json['id']

    # Get summary
    sum_res = client.get(f'/api/summary/{uid}')
    assert sum_res.status_code == 200
    assert sum_res.json['calories'] == 250.0

    # Delete entry
    del_res = client.delete(f'/api/foods/{item_id}')
    assert del_res.status_code == 200
