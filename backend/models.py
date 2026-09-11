from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), default='')
    email = db.Column(db.String(255), default='')
    calorie_goal = db.Column(db.Integer, default=2000)

    def to_dict(self):
        return {'id': self.id, 'firebase_uid': self.firebase_uid, 'name': self.name, 'email': self.email, 'calorie_goal': self.calorie_goal}


class FoodEntry(db.Model):
    __tablename__ = 'food_entries'
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), nullable=False, index=True)
    food_name = db.Column(db.String(255), nullable=False)
    meal = db.Column(db.String(50), default='Snack')
    calories = db.Column(db.Float, default=0.0)
    protein = db.Column(db.Float, default=0.0)
    carbs = db.Column(db.Float, default=0.0)
    fat = db.Column(db.Float, default=0.0)
    fiber = db.Column(db.Float, default=0.0)
    consumed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'firebase_uid': self.firebase_uid, 'food_name': self.food_name,
            'meal': self.meal, 'calories': round(self.calories, 1), 'protein': round(self.protein, 1),
            'carbs': round(self.carbs, 1), 'fat': round(self.fat, 1), 'fiber': round(self.fiber, 1),
            'consumed_at': self.consumed_at.isoformat()
        }


class DailyLog(db.Model):
    __tablename__ = 'daily_logs'
    __table_args__ = (db.UniqueConstraint('firebase_uid', 'log_date', name='uk_user_date'),)
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), nullable=False, index=True)
    log_date = db.Column(db.Date, nullable=False)
    water_ml = db.Column(db.Integer, default=0)
    exercise_minutes = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id, 'firebase_uid': self.firebase_uid,
            'log_date': self.log_date.isoformat(), 'water_ml': self.water_ml,
            'exercise_minutes': self.exercise_minutes
        }
