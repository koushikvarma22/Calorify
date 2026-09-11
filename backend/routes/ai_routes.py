import base64
import json
import os
from flask import Blueprint, request, jsonify
from openai import OpenAI

ai_bp = Blueprint('ai', __name__, url_prefix='/api')

PROMPT = '''Analyze this food for calorie and macronutrient tracking.
Return ONLY the requested JSON.
Be conservative and realistic. If the portion is not clear, make a reasonable standard-serving estimate.
Required fields:
- food_name: concise food/dish name
- estimated_calories: numeric kcal
- protein_g: numeric grams
- carbs_g: numeric grams
- fat_g: numeric grams
- fiber_g: numeric grams
- confidence: exactly High, Medium, or Low
- portion_note: short serving-size explanation'''

RESPONSE_FORMAT = {
    'type': 'json_schema',
    'json_schema': {
        'name': 'food_nutrition',
        'strict': True,
        'schema': {
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
            'required': [
                'food_name', 'estimated_calories', 'protein_g', 'carbs_g',
                'fat_g', 'fiber_g', 'confidence', 'portion_note'
            ],
        },
    },
}

def _analyze(content):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return jsonify(error='OPENAI_API_KEY is not configured on the server'), 503

    try:
        client = OpenAI(api_key=api_key)
        model = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')
        response = client.chat.completions.create(
            model=model,
            response_format=RESPONSE_FORMAT,
            messages=[{'role': 'user', 'content': content}],
        )
        raw = response.choices[0].message.content
        if not raw:
            return jsonify(error='AI returned an empty response'), 502
        return jsonify(json.loads(raw)), 200
    except Exception as exc:
        print(f'[AI ERROR] {type(exc).__name__}: {exc}')
        return jsonify(error='Cali could not analyze the food right now. Check the AI configuration and try again.'), 502

@ai_bp.route('/analyze-food', methods=['POST'])
def analyze_food():
    image = request.files.get('image')
    food_name = (request.form.get('food_name') or '').strip()

    if not image and not food_name:
        data = request.get_json(silent=True) or {}
        food_name = str(data.get('food_name') or '').strip()

    if image:
        if not image.mimetype or not image.mimetype.startswith('image/'):
            return jsonify(error='Please upload a valid image file'), 400
        image_bytes = image.read()
        if not image_bytes:
            return jsonify(error='The uploaded image is empty'), 400
        if len(image_bytes) > 10 * 1024 * 1024:
            return jsonify(error='Image is too large. Please use an image under 10 MB.'), 413

        encoded = base64.b64encode(image_bytes).decode('utf-8')
        mimetype = image.mimetype or 'image/jpeg'
        data_url = f'data:{mimetype};base64,{encoded}'
        content = [
            {'type': 'text', 'text': PROMPT},
            {'type': 'image_url', 'image_url': {'url': data_url, 'detail': 'auto'}},
        ]
        return _analyze(content)

    content = [{
        'type': 'text',
        'text': f'{PROMPT}\n\nEstimate the nutrition for this manually entered food: {food_name}',
    }]
    return _analyze(content)
