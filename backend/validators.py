ALLOWED_MEALS = {'Breakfast', 'Lunch', 'Dinner', 'Snack'}

def validate_food_payload(data):
    if not isinstance(data, dict):
        return False, "Payload must be a JSON object"
    
    if not data.get('firebase_uid'):
        return False, "Field 'firebase_uid' is required"
        
    if not data.get('food_name') or not str(data['food_name']).strip():
        return False, "Field 'food_name' cannot be empty"

    meal = data.get('meal', 'Snack')
    if meal not in ALLOWED_MEALS:
        data['meal'] = 'Snack'

    numeric_fields = ['calories', 'protein', 'carbs', 'fat', 'fiber']
    for field in numeric_fields:
        try:
            val = float(data.get(field, 0))
            if val < 0:
                return False, f"Field '{field}' cannot be negative"
            data[field] = val
        except (ValueError, TypeError):
            return False, f"Field '{field}' must be a numeric value"

    return True, None
