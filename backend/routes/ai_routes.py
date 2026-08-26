import base64
import json
import os
from flask import Blueprint, request, jsonify
from openai import OpenAI

ai_bp = Blueprint('ai', __name__, url_prefix='/api')

PROMPT = '''Analyze this food image for calorie and macronutrient tracking.
Return ONLY a valid JSON object with the following keys:
- food_name: concise title of the dish
- estimated_calories: numeric integer or float kcal
- protein_g: numeric float grams
- carbs_g: numeric float grams
- fat_g: numeric float grams
- fiber_g: numeric float grams
- confidence: string ("High", "Medium", "Low")
- portion_note: brief estimate note of serving size

Always treat estimates conservatively and realistically.'''

@ai_bp.route('/analyze-food', methods=['POST'])
def analyze_food():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return jsonify(error='OPENAI_API_KEY is not configured on the server'), 503

    image = request.files.get('image')
    if not image:
        return jsonify(error='Food image is required in multipart/form-data'), 400

    try:
        encoded = base64.b64encode(image.read()).decode('utf-8')
        mimetype = image.mimetype or 'image/jpeg'
        data_url = f"data:{mimetype};base64,{encoded}"

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model='gpt-4.1-mini',
            response_format={'type': 'json_object'},
            messages=[
                {
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': PROMPT},
                        {'type': 'image_url', 'image_url': {'url': data_url}}
                    ]
                }
            ]
        )
        content = response.choices[0].message.content
        return jsonify(json.loads(content)), 200
    except Exception as exc:
        return jsonify(error=f"AI food analysis error: {str(exc)}"), 500
