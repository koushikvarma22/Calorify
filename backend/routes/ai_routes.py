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
    'required': [
        'food_name', 'estimated_calories', 'protein_g', 'carbs_g',
        'fat_g', 'fiber_g', 'confidence', 'portion_note'
    ],
}


def _get_api_key():
    return (os.getenv('OPENAI_API_KEY') or '').strip()


@ai_bp.route('/ai-health', methods=['GET'])
def ai_health():
    """Safe diagnostic endpoint: never exposes the API key."""
    api_key = _get_api_key()
    return jsonify({
        'openai_key_configured': bool(api_key),
        'openai_key_prefix': api_key[:7] + '...' if api_key else None,
        'model': (os.getenv('OPENAI_MODEL') or 'gpt-4.1-mini').strip(),
    }), 200


def _analyze(content):
    api_key = _get_api_key()
    if not api_key:
        return jsonify(error='OPENAI_API_KEY is not configured on the server'), 503

    model = (os.getenv('OPENAI_MODEL') or 'gpt-4.1-mini').strip()

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            input=[{'role': 'user', 'content': content}],
            text={
                'format': {
                    'type': 'json_schema',
                    'name': 'food_nutrition',
                    'strict': True,
                    'schema': SCHEMA,
                }
            },
        )
        raw = response.output_text
        if not raw:
            return jsonify(error='AI returned an empty response'), 502
        return jsonify(json.loads(raw)), 200
    except Exception as exc:
        print(f'[AI ERROR] {type(exc).__name__}: {exc}')
        # Return the provider error message temporarily so Render/browser testing
        # can identify configuration problems without exposing the secret itself.
        return jsonify(error=f'AI configuration error: {str(exc)}'), 502


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
            {'type': 'input_text', 'text': PROMPT},
            {'type': 'input_image', 'image_url': data_url, 'detail': 'auto'},
        ]
        return _analyze(content)

    content = [{
        'type': 'input_text',
        'text': f'{PROMPT}\n\nEstimate the nutrition for this manually entered food: {food_name}',
    }]
    return _analyze(content)
