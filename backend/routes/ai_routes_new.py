import base64
import json
import os
from flask import Blueprint, request, jsonify
from openai import OpenAI

ai_bp = Blueprint('ai', __name__, url_prefix='/api')

PROMPT = '''Analyze this food for calorie and macronutrient tracking.
Estimate a realistic standard serving when the portion is not visible.
Return nutrition values suitable for a calorie diary.'''

SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'food_name': {'type': 'string'},
        'estimated_calories': {'type': 'number'},
        'protein_g': {'type': 'number'},
        'carbs_g': {'type': 'number'},
        'fat_g': {'type': 'number'},
        'fiber_g': {'type': 'number'},
        'confidence': {'type': 'string', 'enum': ['High', 'Medium', 'Low']},
        'portion_note': {'type': 'string'},
    },
    'required': ['food_name', 'estimated_calories', 'protein_g', 'carbs_g', 'fat_g', 'fiber_g', 'confidence', 'portion_note'],
}


def _analyze(input_content):
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    if not api_key:
        return jsonify(error='Cali is not configured yet. Add OPENAI_API_KEY to the Render environment.'), 503
    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini').strip(),
            input=[{'role': 'user', 'content': input_content}],
            text={'format': {'type': 'json_schema', 'name': 'food_nutrition', 'strict': True, 'schema': SCHEMA}},
        )
        raw = response.output_text
        if not raw:
            return jsonify(error='Cali returned an empty analysis. Please try again.'), 502
        return jsonify(json.loads(raw)), 200
    except Exception as exc:
        print(f'[AI ERROR] {type(exc).__name__}: {exc}')
        return jsonify(error='Cali could not analyze the food. Check the Render OpenAI settings and try again.'), 502


@ai_bp.route('/analyze-food', methods=['POST'])
def analyze_food():
    image = request.files.get('image')
    food_name = (request.form.get('food_name') or '').strip()
    if not image and not food_name:
        data = request.get_json(silent=True) or {}
        food_name = str(data.get('food_name') or '').strip()
    if image:
        if image.mimetype not in {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}:
            return jsonify(error='Please upload a JPG, PNG, WEBP, or GIF image.'), 400
        image_bytes = image.read()
        if not image_bytes:
            return jsonify(error='The uploaded image is empty.'), 400
        if len(image_bytes) > 10 * 1024 * 1024:
            return jsonify(error='Image is too large. Please use an image under 10 MB.'), 413
        encoded = base64.b64encode(image_bytes).decode('utf-8')
        data_url = f'data:{image.mimetype};base64,{encoded}'
        return _analyze([
            {'type': 'input_text', 'text': PROMPT},
            {'type': 'input_image', 'image_url': data_url, 'detail': 'auto'},
        ])
    if not food_name:
        return jsonify(error='Enter a food name or upload a food image.'), 400
    return _analyze([{'type': 'input_text', 'text': f'{PROMPT}\nFood entered by the user: {food_name}'}])
