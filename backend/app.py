import os
from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import config
from backend.models import db
from backend.logger import setup_logger
from backend.errors import register_error_handlers
from backend.routes.user_routes import user_bp
from backend.routes.food_routes import food_bp
from backend.routes.daily_log_routes import daily_log_bp
from backend.routes.ai_routes import ai_bp

def create_app(config_name=None):
    if not config_name:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    db.init_app(app)
    CORS(app, origins=app.config.get('FRONTEND_ORIGINS', '*'))
    setup_logger(app)
    register_error_handlers(app)

    @app.get('/api/health')
    def health():
        return jsonify(status='ok', service='Calorify API', version='1.0.0'), 200

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(daily_log_bp)
    app.register_blueprint(ai_bp)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
