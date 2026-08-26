from datetime import date
from flask import Blueprint, request, jsonify
from backend.models import db, DailyLog

daily_log_bp = Blueprint('daily_log', __name__, url_prefix='/api/daily-log')

@daily_log_bp.route('', methods=['POST'])
def log_daily_activity():
    data = request.get_json() or {}
    uid = data.get('firebase_uid')
    if not uid:
        return jsonify(error='firebase_uid is required'), 400

    today = date.today()
    log = DailyLog.query.filter_by(firebase_uid=uid, log_date=today).first()
    if not log:
        log = DailyLog(firebase_uid=uid, log_date=today)
        db.session.add(log)

    if 'water_ml' in data:
        log.water_ml = max(0, int(data['water_ml']))
    if 'exercise_minutes' in data:
        log.exercise_minutes = max(0, int(data['exercise_minutes']))

    db.session.commit()
    return jsonify(log.to_dict()), 200

@daily_log_bp.route('/<uid>', methods=['GET'])
def get_daily_activity(uid):
    today = date.today()
    log = DailyLog.query.filter_by(firebase_uid=uid, log_date=today).first()
    if not log:
        return jsonify(water_ml=0, exercise_minutes=0, log_date=today.isoformat()), 200
    return jsonify(log.to_dict()), 200
