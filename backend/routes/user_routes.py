from flask import Blueprint, request, jsonify
from backend.models import db, User

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('', methods=['POST'])
def sync_or_create_user():
    data = request.get_json() or {}
    uid = data.get('firebase_uid')
    if not uid:
        return jsonify(error='firebase_uid is required'), 400

    user = User.query.filter_by(firebase_uid=uid).first()
    if not user:
        user = User(firebase_uid=uid)
        db.session.add(user)

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    if 'calorie_goal' in data:
        try:
            user.calorie_goal = max(500, int(data['calorie_goal']))
        except (ValueError, TypeError):
            pass

    db.session.commit()
    return jsonify(user.to_dict()), 200

@user_bp.route('/<uid>', methods=['GET'])
def get_user(uid):
    user = User.query.filter_by(firebase_uid=uid).first()
    if not user:
        return jsonify(error='User not found'), 404
    return jsonify(user.to_dict()), 200
