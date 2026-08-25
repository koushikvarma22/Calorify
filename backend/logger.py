import logging
import uuid
from flask import request, g

def setup_logger(app):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
    )
    logger = logging.getLogger('calorify')

    @app.before_request
    def set_request_id():
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4())[:8])
        logger.info(f"[{g.request_id}] {request.method} {request.path}")

    @app.after_request
    def log_response(response):
        req_id = getattr(g, 'request_id', '-')
        logger.info(f"[{req_id}] status={response.status_code}")
        response.headers['X-Request-ID'] = req_id
        return response

    return logger
