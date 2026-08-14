"""
All Flask extensions are instantiated here (no app context yet).
Call init_extensions(app) inside the app factory.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_caching import Cache
from flask_cors import CORS
from celery import Celery

db   = SQLAlchemy()
jwt  = JWTManager()
mail = Mail()
cache = Cache()
cors  = CORS()

def safe_cache_clear():
    try:
        cache.clear()
    except Exception as e:
        import logging
        logging.warning(f"Cache clear skipped/failed (likely Redis connection unavailable): {e}")

# Celery instance – fully configured in init_celery()
celery = Celery(__name__)


def init_extensions(app):
    """Bind every extension to the Flask app."""
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["FRONTEND_URL"]}},
        supports_credentials=True,
    )
    _init_celery(app)
    _init_jwt_handlers(app)
    return app


def _init_celery(app):
    """Configure Celery so tasks run inside Flask app context."""
    celery.conf.update(
        broker_url          = app.config["CELERY_BROKER_URL"],
        result_backend      = app.config["CELERY_RESULT_BACKEND"],
        task_always_eager   = app.config["CELERY_TASK_ALWAYS_EAGER"],
        task_serializer     = app.config["CELERY_TASK_SERIALIZER"],
        accept_content      = app.config["CELERY_ACCEPT_CONTENT"],
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    import tasks


def _init_jwt_handlers(app):
    """Custom JWT error responses."""
    from flask import jsonify

    @jwt.unauthorized_loader
    def missing_token(reason):
        return jsonify({"error": "Authentication required", "detail": reason}), 401

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_data):
        return jsonify({"error": "Token expired. Please login again."}), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify({"error": "Invalid token", "detail": reason}), 422
