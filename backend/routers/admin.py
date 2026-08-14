"""
Admin-only routes (all require admin JWT)
  /api/admin/stats
  /api/admin/products
  /api/admin/orders
  /api/admin/users
  /api/admin/settings
  /api/admin/upload
"""
import os
import uuid
from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import func

from extensions import db, cache, safe_cache_clear
from models.models import (
    User, Product, Order, OrderStatusHistory, SiteSetting, ContactMessage, ORDER_STATUSES
)
from routers import require_admin

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def _err(msg, code=400):
    return jsonify({"error": msg}), code


# ─────────────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────────────
@admin_bp.route("/stats", methods=["GET"])
@require_admin
def stats():
    total_orders   = Order.query.count()
    total_revenue  = db.session.query(func.coalesce(func.sum(Order.total), 0)).filter(
        Order.status != "cancelled"
    ).scalar()
    pending        = Order.query.filter_by(status="pending").count()
    delivered      = Order.query.filter_by(status="delivered").count()
    total_users    = User.query.filter_by(role="user").count()
    total_products = Product.query.filter_by(active=True).count()

    # Status breakdown
    status_counts = {}
    for s in ORDER_STATUSES:
        status_counts[s] = Order.query.filter_by(status=s).count()

    # Revenue last 7 days
    revenue_chart = []
    for i in range(6, -1, -1):
        day_start = datetime.utcnow().replace(hour=0, minute=0, second=0) - timedelta(days=i)
        day_end   = day_start + timedelta(days=1)
        rev = db.session.query(func.coalesce(func.sum(Order.total), 0)).filter(
            Order.created_at >= day_start,
            Order.created_at < day_end,
            Order.status != "cancelled",
        ).scalar()
        revenue_chart.append({
            "date":    day_start.strftime("%d %b"),
            "revenue": round(float(rev), 2),
        })

    # Popular products (top 5)
    popular = Product.query.filter_by(active=True).order_by(
        Product.order_count.desc()
    ).limit(5).all()

    # Recent orders
    recent = Order.query.order_by(Order.created_at.desc()).limit(10).all()

    return jsonify({
        "total_orders":    total_orders,
        "total_revenue":   round(float(total_revenue), 2),
        "pending_orders":  pending,
        "delivered_orders":delivered,
        "total_users":     total_users,
        "total_products":  total_products,
        "status_counts":   status_counts,
        "revenue_chart":   revenue_chart,
        "popular_products":[p.to_dict() for p in popular],
        "recent_orders":   [o.to_dict() for o in recent],
    })


# ─────────────────────────────────────────────────────
# PRODUCTS
# ─────────────────────────────────────────────────────
@admin_bp.route("/products", methods=["GET"])
@require_admin
def list_products():
    q = request.args.get("q", "").strip()
    query = Product.query
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))
    products = query.order_by(Product.id.desc()).all()
    return jsonify([p.to_dict() for p in products])


@admin_bp.route("/products", methods=["POST"])
@require_admin
def add_product():
    data = request.get_json() or {}
    if not data.get("name") or not data.get("price"):
        return _err("Name and price are required")

    image_urls = data.get("image_urls", [])
    image_url  = data.get("image_url", "")
    if image_urls and not image_url:
        image_url = image_urls[0]

    p = Product(
        name        = data["name"].strip(),
        description = data.get("description", "").strip(),
        price       = float(data["price"]),
        unit        = data.get("unit", "kg"),
        category    = data.get("category", "sugarcane"),
        badge       = data.get("badge") or None,
        image_url   = image_url,
        image_urls  = image_urls,
        stock       = int(data.get("stock", 100)),
        active      = bool(data.get("active", True)),
        featured    = bool(data.get("featured", False)),
    )
    db.session.add(p)
    db.session.commit()
    safe_cache_clear()
    return jsonify(p.to_dict()), 201


@admin_bp.route("/products/<int:pid>", methods=["PUT"])
@require_admin
def update_product(pid):
    p    = Product.query.get_or_404(pid)
    data = request.get_json() or {}

    p.name        = data.get("name", p.name).strip()
    p.description = data.get("description", p.description or "").strip()
    p.price       = float(data.get("price", p.price))
    p.unit        = data.get("unit", p.unit)
    p.category    = data.get("category", p.category)
    p.badge       = data.get("badge") or None
    p.stock       = int(data.get("stock", p.stock))
    p.active      = bool(data.get("active", p.active))
    p.featured    = bool(data.get("featured", p.featured))

    if "image_urls" in data:
        p.image_urls = data["image_urls"]
        if p.image_urls and not data.get("image_url"):
            p.image_url = p.image_urls[0]

    if "image_url" in data:
        p.image_url = data["image_url"]

    db.session.commit()
    safe_cache_clear()
    return jsonify(p.to_dict())


@admin_bp.route("/products/<int:pid>", methods=["DELETE"])
@require_admin
def delete_product(pid):
    p = Product.query.get_or_404(pid)
    p.active = False          # soft delete
    db.session.commit()
    safe_cache_clear()
    return jsonify({"success": True})


# ─────────────────────────────────────────────────────
# IMAGE UPLOAD
# ─────────────────────────────────────────────────────
def _allowed(filename: str) -> bool:
    allowed = current_app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


@admin_bp.route("/upload", methods=["POST"])
@require_admin
def upload_image():
    if "file" not in request.files:
        return _err("No file provided")
    f = request.files["file"]
    if not f.filename or not _allowed(f.filename):
        return _err("Invalid file type. Allowed: png, jpg, jpeg, webp, gif")

    ext      = f.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    folder   = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    f.save(os.path.join(folder, filename))

    url = f"/uploads/{filename}"
    return jsonify({"url": url, "filename": filename}), 201


# ─────────────────────────────────────────────────────
# ORDERS
# ─────────────────────────────────────────────────────
@admin_bp.route("/orders", methods=["GET"])
@require_admin
def list_orders():
    status   = request.args.get("status")
    page     = int(request.args.get("page", 1))
    per_page = current_app.config["ORDERS_PER_PAGE"]
    q        = request.args.get("q", "").strip()

    query = Order.query
    if status and status != "all":
        query = query.filter_by(status=status)
    if q:
        query = query.filter(
            Order.order_number.ilike(f"%{q}%") |
            Order.customer_name.ilike(f"%{q}%") |
            Order.phone.ilike(f"%{q}%")
        )

    paginated = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        "orders": [o.to_dict() for o in paginated.items],
        "total":  paginated.total,
        "pages":  paginated.pages,
        "page":   paginated.page,
    })


@admin_bp.route("/orders/<int:oid>/status", methods=["PUT"])
@require_admin
def update_order_status(oid):
    order  = Order.query.get_or_404(oid)
    data   = request.get_json() or {}
    status = data.get("status")
    note   = data.get("note", "")

    if status not in ORDER_STATUSES:
        return _err(f"Invalid status. Must be one of: {ORDER_STATUSES}")

    old_status    = order.status
    order.status  = status
    expected_date = data.get("expected_delivery_date")
    if expected_date is not None:
        order.expected_delivery_date = expected_date.strip()

    admin_id      = int(get_jwt_identity())

    history = OrderStatusHistory(
        order_id   = order.id,
        status     = status,
        changed_by = admin_id,
        note       = note,
    )
    db.session.add(history)
    db.session.commit()

    # Send status-update email (async)
    if order.email:
        try:
            from tasks import send_status_update_task
            send_status_update_task.delay(order.id, old_status, status)
        except Exception as exc:
            current_app.logger.warning(f"Email task failed: {exc}")

    return jsonify(order.to_dict(include_history=True))


# ─────────────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────────────
@admin_bp.route("/users", methods=["GET"])
@require_admin
def list_users():
    q     = request.args.get("q", "").strip()
    query = User.query
    if q:
        query = query.filter(
            User.name.ilike(f"%{q}%") | User.email.ilike(f"%{q}%")
        )
    users = query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict() for u in users])


@admin_bp.route("/users/<int:uid>", methods=["PUT"])
@require_admin
def update_user(uid):
    user = User.query.get_or_404(uid)
    data = request.get_json() or {}
    if "is_active" in data:
        user.is_active = bool(data["is_active"])
    if "role" in data and data["role"] in ("user", "admin"):
        user.role = data["role"]
    db.session.commit()
    return jsonify(user.to_dict())


# ─────────────────────────────────────────────────────
# SITE SETTINGS
# ─────────────────────────────────────────────────────
@admin_bp.route("/settings", methods=["GET"])
@require_admin
def get_settings():
    return jsonify(SiteSetting.all_as_dict())


@admin_bp.route("/settings", methods=["PUT"])
@require_admin
def update_settings():
    data = request.get_json() or {}
    SiteSetting.set_many(data)
    safe_cache_clear()
    return jsonify({"success": True, "settings": SiteSetting.all_as_dict()})


@admin_bp.route("/settings/logo", methods=["POST"])
@require_admin
def upload_logo():
    if "file" not in request.files:
        return _err("No file provided")
    f = request.files["file"]
    if not f.filename or not _allowed(f.filename):
        return _err("Invalid file type")

    ext      = f.filename.rsplit(".", 1)[1].lower()
    filename = f"logo_{uuid.uuid4().hex}.{ext}"
    folder   = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    f.save(os.path.join(folder, filename))

    url = f"/uploads/{filename}"
    SiteSetting.set("site_logo", url)
    safe_cache_clear()
    return jsonify({"url": url})


# ─────────────────────────────────────────────────────
# CONTACT MESSAGES MANAGEMENT
# ─────────────────────────────────────────────────────
@admin_bp.route("/messages", methods=["GET"])
@require_admin
def get_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify([m.to_dict() for m in messages])


@admin_bp.route("/messages/<int:msg_id>/read", methods=["PUT"])
@require_admin
def mark_message_read(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.is_read = True
    db.session.commit()
    return jsonify({"success": True, "message": "Message marked as read"})


@admin_bp.route("/messages/<int:msg_id>", methods=["DELETE"])
@require_admin
def delete_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({"success": True, "message": "Message deleted"})
