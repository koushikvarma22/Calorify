from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(success=False, error=str(error.description if hasattr(error, 'description') else error)), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(success=False, error="Resource not found"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify(success=False, error="Internal server error"), 500
