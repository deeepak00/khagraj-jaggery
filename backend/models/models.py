import json
import secrets
from datetime import datetime

from sqlalchemy import event
from sqlalchemy.types import TypeDecorator, Text
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


# ─────────────────────────────────────────────────────
# JSON column type (works with SQLite & PostgreSQL)
# ─────────────────────────────────────────────────────
class JSONType(TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return json.dumps(value) if value is not None else "[]"

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return []


# ─────────────────────────────────────────────────────
# USER
# ─────────────────────────────────────────────────────
class User(db.Model):
    __tablename__ = "users"

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    email        = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone        = db.Column(db.String(20))
    password_hash = db.Column(db.String(256), nullable=False)
    role         = db.Column(db.String(20), default="user")   # "user" | "admin"
    avatar_url   = db.Column(db.String(500))
    is_active    = db.Column(db.Boolean, default=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    orders       = db.relationship("Order", backref="user", lazy="dynamic")

    # ── Password helpers ──
    def set_password(self, raw: str):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password_hash, raw)

    def to_dict(self, include_private=False):
        d = {
            "id":         self.id,
            "name":       self.name,
            "email":      self.email,
            "phone":      self.phone or "",
            "role":       self.role,
            "avatar_url": self.avatar_url or "",
            "is_active":  self.is_active,
            "created_at": self.created_at.isoformat(),
        }
        return d

    def __repr__(self):
        return f"<User {self.email}>"


# ─────────────────────────────────────────────────────
# PRODUCT
# ─────────────────────────────────────────────────────
class Product(db.Model):
    __tablename__ = "products"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price       = db.Column(db.Float, nullable=False)
    unit        = db.Column(db.String(20), default="kg")
    category    = db.Column(db.String(50), index=True)
    badge       = db.Column(db.String(50))          # "Bestseller", "New", "Organic", …
    image_url   = db.Column(db.String(500))          # relative path or full URL
    stock       = db.Column(db.Integer, default=100)
    active      = db.Column(db.Boolean, default=True, index=True)
    featured    = db.Column(db.Boolean, default=False)
    order_count = db.Column(db.Integer, default=0)  # bumped on every order
    image_urls  = db.Column(JSONType, nullable=False, default=list) # up to 5 images
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        urls = self.image_urls
        if not urls and self.image_url:
            urls = [self.image_url]
        return {
            "id":          self.id,
            "name":        self.name,
            "description": self.description or "",
            "price":       self.price,
            "unit":        self.unit,
            "category":    self.category or "",
            "badge":       self.badge or "",
            "image_url":   self.image_url or "",
            "image_urls":  urls or [],
            "stock":       self.stock,
            "active":      self.active,
            "featured":    self.featured,
            "order_count": self.order_count,
            "created_at":  self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Product {self.name}>"


# ─────────────────────────────────────────────────────
# ORDER
# ─────────────────────────────────────────────────────
ORDER_STATUSES = ["pending", "confirmed", "processing", "shipped", "delivered", "cancelled"]


class Order(db.Model):
    __tablename__ = "orders"

    id            = db.Column(db.Integer, primary_key=True)
    order_number  = db.Column(db.String(30), unique=True, nullable=False, index=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    customer_name = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120))
    phone         = db.Column(db.String(20), nullable=False)
    address       = db.Column(db.Text, nullable=False)
    city          = db.Column(db.String(60), nullable=False)
    state         = db.Column(db.String(60), nullable=False)
    pincode       = db.Column(db.String(10), nullable=False)
    items         = db.Column(JSONType, nullable=False, default=list)
    # items schema: [{"id":1,"name":"...","qty":2,"price":80,"unit":"kg"}]
    subtotal      = db.Column(db.Float, nullable=False, default=0.0)
    discount_amount = db.Column(db.Float, nullable=False, default=0.0)
    shipping_fee  = db.Column(db.Float, nullable=False, default=0.0)
    total         = db.Column(db.Float, nullable=False)
    status                 = db.Column(db.String(20), default="pending", index=True)
    notes                  = db.Column(db.Text)
    expected_delivery_date = db.Column(db.String(100), nullable=True)
    created_at             = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    history       = db.relationship(
        "OrderStatusHistory", backref="order",
        lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self, include_history=False):
        d = {
            "id":                     self.id,
            "order_number":           self.order_number,
            "user_id":                self.user_id,
            "customer_name":          self.customer_name,
            "email":                  self.email or "",
            "phone":                  self.phone,
            "address":                self.address,
            "city":                   self.city,
            "state":                  self.state,
            "pincode":                self.pincode,
            "items":                  self.items,
            "subtotal":               self.subtotal,
            "discount_amount":        self.discount_amount,
            "shipping_fee":           self.shipping_fee,
            "total":                  self.total,
            "status":                 self.status,
            "notes":                  self.notes or "",
            "expected_delivery_date": self.expected_delivery_date or "",
            "created_at":             self.created_at.isoformat(),
        }
        if include_history:
            d["history"] = [h.to_dict() for h in self.history.order_by(
                OrderStatusHistory.created_at.asc()
            )]
        return d

    @staticmethod
    def generate_number():
        ts  = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        rnd = secrets.token_hex(2).upper()
        return f"JGR{ts}{rnd}"

    def __repr__(self):
        return f"<Order {self.order_number} [{self.status}]>"


# ─────────────────────────────────────────────────────
# ORDER STATUS HISTORY
# ─────────────────────────────────────────────────────
class OrderStatusHistory(db.Model):
    __tablename__ = "order_status_history"

    id           = db.Column(db.Integer, primary_key=True)
    order_id     = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    status       = db.Column(db.String(20), nullable=False)
    changed_by   = db.Column(db.Integer, db.ForeignKey("users.id"))
    note         = db.Column(db.Text)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "status":     self.status,
            "changed_by": self.changed_by,
            "note":       self.note or "",
            "created_at": self.created_at.isoformat(),
        }


# ─────────────────────────────────────────────────────
# SITE SETTINGS (key-value store)
# ─────────────────────────────────────────────────────
class SiteSetting(db.Model):
    __tablename__ = "site_settings"

    id         = db.Column(db.Integer, primary_key=True)
    key        = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value      = db.Column(db.Text, default="")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get(cls, key: str, default: str = "") -> str:
        row = cls.query.filter_by(key=key).first()
        return row.value if row else default

    @classmethod
    def set(cls, key: str, value: str):
        row = cls.query.filter_by(key=key).first()
        if row:
            row.value = value
            row.updated_at = datetime.utcnow()
        else:
            db.session.add(cls(key=key, value=str(value)))
        db.session.commit()

    @classmethod
    def set_many(cls, data: dict):
        for key, value in data.items():
            row = cls.query.filter_by(key=key).first()
            if row:
                row.value = str(value)
                row.updated_at = datetime.utcnow()
            else:
                db.session.add(cls(key=key, value=str(value)))
        db.session.commit()

    @classmethod
    def all_as_dict(cls) -> dict:
        return {r.key: r.value for r in cls.query.all()}

    def __repr__(self):
        return f"<SiteSetting {self.key}>"


# ─────────────────────────────────────────────────────
# CONTACT MESSAGES
# ─────────────────────────────────────────────────────
class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    contact    = db.Column(db.String(100), nullable=False)
    message    = db.Column(db.Text, nullable=False)
    is_read    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id":         self.id,
            "name":       self.name,
            "contact":    self.contact,
            "message":    self.message,
            "is_read":    self.is_read,
            "created_at": self.created_at.isoformat() if self.created_at else ""
        }

    def __repr__(self):
        return f"<ContactMessage {self.name}>"
