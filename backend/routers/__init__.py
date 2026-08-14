"""
RBAC decorators shared across all routers.
"""
from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from extensions import db
from models.models import User



def _load_user():
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None



def require_auth(fn):
    """Any authenticated user."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = _load_user()
        if not user or not user.is_active:
            return jsonify({"error": "Account not found or inactive"}), 401
        return fn(*args, **kwargs)
    return wrapper


def require_admin(fn):
    """Admin role only."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = _load_user()
        if not user or not user.is_active:
            return jsonify({"error": "Authentication required"}), 401
        if user.role != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


def optional_auth(fn):
    """Proceed whether or not a JWT is present."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
        except Exception:
            pass
        return fn(*args, **kwargs)
    return wrapper


def get_current_user() -> User | None:
    """Return the current user from JWT, or None."""
    try:
        verify_jwt_in_request(optional=True)
        return _load_user()
    except Exception:
        return None
