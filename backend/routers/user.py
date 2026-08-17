"""
Public + authenticated user routes
  /api/auth/*        – register, login, logout, me, profile
  /api/products      – browse products
  /api/orders        – place & view own orders
  /api/settings/public – site settings visible to frontend
"""
import os
import re

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request

from extensions import db, cache, safe_cache_clear
from models.models import User, Product, Order, OrderStatusHistory, SiteSetting, ContactMessage
from routers import require_auth, optional_auth, get_current_user

user_bp = Blueprint("user", __name__, url_prefix="/api")


# ─────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────
def _err(msg, code=400):
    return jsonify({"error": msg}), code


def _valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


# ─────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────
@user_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name     = data.get("name", "").strip()
    email    = data.get("email", "").strip().lower()
    phone    = data.get("phone", "").strip()
    password = data.get("password", "")

    if not all([name, email, password]):
        return _err("Name, email and password are required")
    if not _valid_email(email):
        return _err("Invalid email address")
    if len(password) < 6:
        return _err("Password must be at least 6 characters")
    if User.query.filter_by(email=email).first():
        return _err("Email already registered", 409)

    user = User(name=name, email=email, phone=phone)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token, "user": user.to_dict()}), 201


@user_bp.route("/auth/login", methods=["POST"])
def login():
    data     = request.get_json() or {}
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return _err("Email and password required")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return _err("Invalid email or password", 401)
    if not user.is_active:
        return _err("Account is inactive. Contact support.", 403)

    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token, "user": user.to_dict()})


@user_bp.route("/auth/me", methods=["GET"])
@require_auth
def me():
    user = db.session.get(User, int(get_jwt_identity()))
    return jsonify(user.to_dict())


@user_bp.route("/auth/profile", methods=["PUT"])
@require_auth
def update_profile():
    user = db.session.get(User, int(get_jwt_identity()))
    data = request.get_json() or {}

    if "name" in data and data["name"].strip():
        user.name = data["name"].strip()
    if "phone" in data:
        user.phone = data["phone"].strip()
    if "password" in data and data["password"]:
        if len(data["password"]) < 6:
            return _err("Password must be at least 6 characters")
        user.set_password(data["password"])

    db.session.commit()
    return jsonify(user.to_dict())


# ─────────────────────────────────────────────────────
# PRODUCTS (public)
# ─────────────────────────────────────────────────────
@user_bp.route("/products", methods=["GET"])
@cache.cached(timeout=120, query_string=True)
def list_products():
    q        = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    featured = request.args.get("featured")
    page     = int(request.args.get("page", 1))
    per_page = current_app.config["PRODUCTS_PER_PAGE"]

    query = Product.query.filter_by(active=True)
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))
    if category:
        query = query.filter_by(category=category)
    if featured:
        query = query.filter_by(featured=True)

    paginated = query.order_by(Product.order_count.desc(), Product.id.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        "products": [p.to_dict() for p in paginated.items],
        "total":    paginated.total,
        "pages":    paginated.pages,
        "page":     paginated.page,
    })


@user_bp.route("/products/<int:pid>", methods=["GET"])
def get_product(pid):
    p = Product.query.filter_by(id=pid, active=True).first_or_404()
    return jsonify(p.to_dict())


@user_bp.route("/products/categories", methods=["GET"])
@cache.cached(timeout=300)
def product_categories():
    rows = db.session.query(Product.category).filter(
        Product.active == True, Product.category.isnot(None)
    ).distinct().all()
    return jsonify([r[0] for r in rows if r[0]])


# ─────────────────────────────────────────────────────
# ORDERS
# ─────────────────────────────────────────────────────
@user_bp.route("/orders", methods=["POST"])
@optional_auth
def place_order():
    data = request.get_json() or {}
    required = ["customer_name", "phone", "address", "city", "state", "pincode", "items", "total"]
    for f in required:
        if not data.get(f):
            return _err(f"Missing required field: {f}")

    items = data["items"]
    if not items or not isinstance(items, list):
        return _err("Order must contain at least one item")

    # Validate pincode
    if not re.match(r"^\d{6}$", str(data["pincode"])):
        return _err("Invalid PIN code")

    current_user = get_current_user()
    order = Order(
        order_number  = Order.generate_number(),
        user_id       = current_user.id if current_user else None,
        customer_name = data["customer_name"].strip(),
        email         = data.get("email", "").strip(),
        phone         = data["phone"].strip(),
        address       = data["address"].strip(),
        city          = data["city"].strip(),
        state         = data["state"].strip(),
        pincode       = str(data["pincode"]).strip(),
        items         = items,
        subtotal      = float(data.get("subtotal", data["total"])),
        discount_amount = float(data.get("discount_amount", 0.0)),
        shipping_fee  = float(data.get("shipping_fee", 0.0)),
        total         = float(data["total"]),
        notes         = data.get("notes", "").strip(),
    )
    db.session.add(order)

    # Bump order_count on each product
    for item in items:
        p = db.session.get(Product, item.get("id"))
        if p:

            p.order_count = (p.order_count or 0) + item.get("qty", 1)

    db.session.commit()

    # Record initial status in history
    db.session.add(OrderStatusHistory(
        order_id=order.id, status="pending", note="Order placed"
    ))
    db.session.commit()

    # Invalidate product cache
    safe_cache_clear()

    # Send confirmation email (async via thread/Celery)
    try:
        from tasks import send_order_confirmation_task, run_async_task
        run_async_task(send_order_confirmation_task, order.id)
    except Exception:
        pass

    return jsonify({"success": True, "order_number": order.order_number}), 201


@user_bp.route("/orders/my", methods=["GET"])
@require_auth
def my_orders():
    user_id  = int(get_jwt_identity())
    page     = int(request.args.get("page", 1))
    per_page = current_app.config["ORDERS_PER_PAGE"]

    paginated = Order.query.filter_by(user_id=user_id).order_by(
        Order.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "orders": [o.to_dict() for o in paginated.items],
        "total":  paginated.total,
        "pages":  paginated.pages,
        "page":   paginated.page,
    })


@user_bp.route("/orders/<order_number>", methods=["GET"])
@optional_auth
def get_order(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    current_user = get_current_user()
    # Allow owner or admin
    if order.user_id and (not current_user or
            (current_user.id != order.user_id and current_user.role != "admin")):
        return _err("Forbidden", 403)
    return jsonify(order.to_dict(include_history=True))


# ─────────────────────────────────────────────────────
# PUBLIC SITE SETTINGS
# ─────────────────────────────────────────────────────
@user_bp.route("/settings/public", methods=["GET"])
@cache.cached(timeout=300)
def public_settings():
    """Returns only non-sensitive settings the frontend needs."""
    allowed_keys = [
        "site_name", "site_tagline", "site_logo",
        "hero_title", "hero_subtitle",
        "about_title", "about_text",
        "contact_phone", "contact_email", "contact_address", "working_hours",
        "whatsapp_number", "facebook_url", "instagram_url",
        "announcement_text", "announcement_active",
        "manager_lalji_name", "manager_lalji_role", "manager_lalji_bio", "manager_lalji_photo",
        "manager_awadhesh_name", "manager_awadhesh_role", "manager_awadhesh_bio", "manager_awadhesh_photo",
        "manager_arjun_name", "manager_arjun_role", "manager_arjun_bio", "manager_arjun_photo",
        "branches_info",
        "shipping_free_threshold", "shipping_base_fee", "seasonal_discount_percent",
        "testimonial_1_name", "testimonial_1_role", "testimonial_1_text", "testimonial_1_photo",
        "testimonial_2_name", "testimonial_2_role", "testimonial_2_text", "testimonial_2_photo",
        "testimonial_3_name", "testimonial_3_role", "testimonial_3_text", "testimonial_3_photo",
    ]
    all_settings = SiteSetting.all_as_dict()
    return jsonify({k: all_settings.get(k, "") for k in allowed_keys})


# ─────────────────────────────────────────────────────
# SUBMIT CONTACT MESSAGE
# ─────────────────────────────────────────────────────
@user_bp.route("/contact", methods=["POST"])
def submit_contact():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    contact_info = data.get("contact", "").strip()
    message = data.get("message", "").strip()

    if not name or not message:
        return jsonify({"error": "Please provide name and message"}), 400

    msg = ContactMessage(
        name=name,
        contact=contact_info,
        message=message
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({"success": True, "message": "Your query has been recorded. We will contact you soon."}), 201
