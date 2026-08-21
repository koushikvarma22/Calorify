import os, base64, json
from datetime import datetime, date
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL','sqlite:///calorify_dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app, origins=os.getenv('FRONTEND_ORIGIN','http://localhost:5173').split(','))

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firebase_uid=db.Column(db.String(128),unique=True,nullable=False)
    name=db.Column(db.String(120),default='')
    email=db.Column(db.String(255),default='')
    calorie_goal=db.Column(db.Integer,default=2000)

class FoodEntry(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firebase_uid=db.Column(db.String(128),nullable=False,index=True)
    food_name=db.Column(db.String(255),nullable=False)
    meal=db.Column(db.String(50),default='Snack')
    calories=db.Column(db.Float,default=0)
    protein=db.Column(db.Float,default=0)
    carbs=db.Column(db.Float,default=0)
    fat=db.Column(db.Float,default=0)
    fiber=db.Column(db.Float,default=0)
    consumed_at=db.Column(db.DateTime,default=datetime.utcnow)

class DailyLog(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firebase_uid=db.Column(db.String(128),nullable=False)
    log_date=db.Column(db.Date,nullable=False)
    water_ml=db.Column(db.Integer,default=0)
    exercise_minutes=db.Column(db.Integer,default=0)

@app.get('/api/health')
def health(): return jsonify(status='ok',service='Calorify API')

@app.post('/api/users')
def users():
    d=request.get_json() or {}; uid=d.get('firebase_uid')
    if not uid:return jsonify(error='firebase_uid required'),400
    u=User.query.filter_by(firebase_uid=uid).first()
    if not u:u=User(firebase_uid=uid);db.session.add(u)
    u.name=d.get('name',u.name);u.email=d.get('email',u.email);u.calorie_goal=int(d.get('calorie_goal',u.calorie_goal or 2000))
    db.session.commit();return jsonify(id=u.id,name=u.name,email=u.email,calorie_goal=u.calorie_goal)

@app.get('/api/summary/<uid>')
def summary(uid):
    items=FoodEntry.query.filter(FoodEntry.firebase_uid==uid,db.func.date(FoodEntry.consumed_at)==date.today()).all()
    u=User.query.filter_by(firebase_uid=uid).first(); log=DailyLog.query.filter_by(firebase_uid=uid,log_date=date.today()).first()
    return jsonify(calories=sum(x.calories for x in items),protein=sum(x.protein for x in items),carbs=sum(x.carbs for x in items),fat=sum(x.fat for x in items),goal=u.calorie_goal if u else 2000,water_ml=log.water_ml if log else 0,exercise_minutes=log.exercise_minutes if log else 0)

@app.get('/api/foods/<uid>')
def foods(uid):
    items=FoodEntry.query.filter_by(firebase_uid=uid).order_by(FoodEntry.consumed_at.desc()).all()
    return jsonify([{'id':x.id,'food_name':x.food_name,'meal':x.meal,'calories':x.calories,'protein':x.protein,'carbs':x.carbs,'fat':x.fat,'fiber':x.fiber,'consumed_at':x.consumed_at.isoformat()} for x in items])

@app.post('/api/foods')
def add_food():
    d=request.get_json() or {}
    if not d.get('firebase_uid') or not d.get('food_name'):return jsonify(error='firebase_uid and food_name required'),400
    x=FoodEntry(firebase_uid=d['firebase_uid'],food_name=d['food_name'],meal=d.get('meal','Snack'),calories=float(d.get('calories',0)),protein=float(d.get('protein',0)),carbs=float(d.get('carbs',0)),fat=float(d.get('fat',0)),fiber=float(d.get('fiber',0)))
    db.session.add(x);db.session.commit();return jsonify(id=x.id),201

@app.delete('/api/foods/<int:item_id>')
def delete_food(item_id):
    x=FoodEntry.query.get_or_404(item_id);db.session.delete(x);db.session.commit();return jsonify(message='deleted')

@app.post('/api/daily-log')
def daily_log():
    d=request.get_json() or {};uid=d.get('firebase_uid')
    if not uid:return jsonify(error='firebase_uid required'),400
    x=DailyLog.query.filter_by(firebase_uid=uid,log_date=date.today()).first()
    if not x:x=DailyLog(firebase_uid=uid,log_date=date.today());db.session.add(x)
    x.water_ml=int(d.get('water_ml',x.water_ml));x.exercise_minutes=int(d.get('exercise_minutes',x.exercise_minutes));db.session.commit()
    return jsonify(water_ml=x.water_ml,exercise_minutes=x.exercise_minutes)

@app.post('/api/analyze-food')
def analyze_food():
    if not os.getenv('OPENAI_API_KEY'):return jsonify(error='OPENAI_API_KEY is not configured'),503
    image=request.files.get('image')
    if not image:return jsonify(error='Food image required'),400
    encoded=base64.b64encode(image.read()).decode();data_url=f"data:{image.mimetype or 'image/jpeg'};base64,{encoded}"
    client=OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt='''Analyze this food image for calorie tracking. Return ONLY JSON with food_name, estimated_calories, protein_g, carbs_g, fat_g, fiber_g, confidence, portion_note. Give a realistic estimate and clearly treat it as an estimate, not an exact measurement.'''
    r=client.chat.completions.create(model='gpt-4.1-mini',response_format={'type':'json_object'},messages=[{'role':'user','content':[{'type':'text','text':prompt},{'type':'image_url','image_url':{'url':data_url}}]}])
    return jsonify(json.loads(r.choices[0].message.content))

with app.app_context():db.create_all()
if __name__=='__main__':app.run(debug=True,port=8000)
