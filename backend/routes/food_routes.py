from datetime import date
from flask import Blueprint, request, jsonify
from backend.models import db, FoodEntry, User, DailyLog
from backend.validators import validate_food_payload

food_bp = Blueprint('foods', __name__, url_prefix='/api')

@food_bp.route('/summary/<uid>', methods=['GET'])
def get_summary(uid):
    today = date.today()
    items = FoodEntry.query.filter(
        FoodEntry.firebase_uid == uid,
        db.func.date(FoodEntry.consumed_at) == today
    ).all()
    user = User.query.filter_by(firebase_uid=uid).first()
    log = DailyLog.query.filter_by(firebase_uid=uid, log_date=today).first()

    return jsonify(
        calories=round(sum(x.calories for x in items), 1),
        protein=round(sum(x.protein for x in items), 1),
        carbs=round(sum(x.carbs for x in items), 1),
        fat=round(sum(x.fat for x in items), 1),
        fiber=round(sum(x.fiber for x in items), 1),
        goal=user.calorie_goal if user else 2000,
        water_ml=log.water_ml if log else 0,
        exercise_minutes=log.exercise_minutes if log else 0
    ), 200

@food_bp.route('/foods/<uid>', methods=['GET'])
def get_foods(uid):
    items = FoodEntry.query.filter_by(firebase_uid=uid).order_by(FoodEntry.consumed_at.desc()).all()
    return jsonify([x.to_dict() for x in items]), 200

@food_bp.route('/foods', methods=['POST'])
def add_food():
    data = request.get_json() or {}
    is_valid, err_msg = validate_food_payload(data)
    if not is_valid:
        return jsonify(error=err_msg), 400

    entry = FoodEntry(
        firebase_uid=data['firebase_uid'],
        food_name=data['food_name'].strip(),
        meal=data.get('meal', 'Snack'),
        calories=data['calories'],
        protein=data['protein'],
        carbs=data['carbs'],
        fat=data['fat'],
        fiber=data['fiber']
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201

@food_bp.route('/foods/<int:item_id>', methods=['DELETE'])
def delete_food(item_id):
    entry = FoodEntry.query.get_or_404(item_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify(message='Food entry deleted successfully', id=item_id), 200
