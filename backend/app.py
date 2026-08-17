"""
GurMahima – Flask Application Factory
"""
import os
import logging

from flask import Flask, send_from_directory, jsonify

from config import config_map
from extensions import db, init_extensions


def create_app(env: str = None) -> Flask:
    env = env or os.environ.get("FLASK_ENV", "development")
    cfg = config_map.get(env, config_map["default"])

    app = Flask(__name__, static_folder="static")
    app.config.from_object(cfg)

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Init all extensions
    init_extensions(app)

    # Register blueprints
    from routers.user  import user_bp
    from routers.admin import admin_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    # Serve uploaded files
    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    # Health check (Render uses this)
    @app.route("/health")
    def health():
        from datetime import datetime
        return jsonify({"status": "ok", "ts": datetime.utcnow().isoformat()})

    # Seed database
    with app.app_context():
        _seed(app)

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    return app


# ─────────────────────────────────────────────────────
# DB SEED
# ─────────────────────────────────────────────────────
def _seed(app: Flask):
    db.create_all()

    # Alter tables before importing models or querying them
    # Check and add expected_delivery_date to orders table
    try:
        db.session.execute(db.text("SELECT expected_delivery_date FROM orders LIMIT 1"))
    except Exception:
        db.session.rollback()
        try:
            db.session.execute(db.text("ALTER TABLE orders ADD COLUMN expected_delivery_date VARCHAR(100)"))
            db.session.commit()
            app.logger.info("Added expected_delivery_date column to orders table")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Failed to add expected_delivery_date: {e}")

    # Check and add image_urls to products table
    try:
        db.session.execute(db.text("SELECT image_urls FROM products LIMIT 1"))
    except Exception:
        db.session.rollback()
        try:
            db.session.execute(db.text("ALTER TABLE products ADD COLUMN image_urls TEXT DEFAULT '[]'"))
            db.session.commit()
            app.logger.info("Added image_urls column to products table")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Failed to add image_urls: {e}")

    for col in ["subtotal", "discount_amount", "shipping_fee"]:
        try:
            db.session.execute(db.text(f"SELECT {col} FROM orders LIMIT 1"))
        except Exception:
            db.session.rollback()
            try:
                db.session.execute(db.text(f"ALTER TABLE orders ADD COLUMN {col} FLOAT DEFAULT 0.0"))
                db.session.commit()
                app.logger.info(f"Added {col} column to orders table")
            except Exception as ex:
                db.session.rollback()
                app.logger.error(f"Failed to add {col} column: {ex}")

    from models.models import User, Product, SiteSetting, ContactMessage

    # Admin user
    admin = User.query.filter_by(role="admin").first()
    if not admin:
        admin = User(
            name  = app.config["ADMIN_NAME"],
            email = app.config["ADMIN_EMAIL"],
            phone = "6394050508",
            role  = "admin",
        )
        admin.set_password(app.config["ADMIN_PASSWORD"])
        db.session.add(admin)
        db.session.commit()
        app.logger.info(f"Admin seeded: {admin.email}")
    else:
        admin.email = app.config["ADMIN_EMAIL"]
        admin.phone = "6394050508"
        db.session.commit()

    # Default site settings
    defaults = {
        "site_name":           "KhagRaj",
        "site_tagline":        "Pure Jaggery, Ancient Goodness — An Initiative by Lal Ji Foods",
        "site_logo":           "/uploads/logo.png",
        "hero_title":          "Pure <em>Jaggery</em>,<br>Ancient Goodness.",
        "hero_subtitle":       "Handcrafted in small batches using traditional methods. No chemicals, no additives — just pure, golden sweetness. An initiative by Lal Ji Foods.",
        "about_title":         "Made with Tradition, Served with Pride",
        "about_text":          "KhagRaj was born from a simple belief — that the sweetness of jaggery should never come at the cost of purity. An initiative by Lal Ji Foods, we source fresh sugarcane from local farms and produce jaggery in open iron vessels the old-fashioned way.",
        "contact_phone":       "+91-6394050508, +91-8601982296",
        "contact_email":       "khagrajindia2017@gmail.com",
        "contact_address":     "KhagRaj Production House, Maharashtra, India",
        "working_hours":       "Mon–Sat, 9:00 AM – 6:00 PM",
        "whatsapp_number":     "916394050508",
        "facebook_url":        "",
        "instagram_url":       "",
        "announcement_text":   "",
        "announcement_active": "false",
        "manager_lalji_name":  "Lal Ji",
        "manager_lalji_role":  "Founder & Visionary",
        "manager_lalji_bio":   "Dedicating decades to restoring health through pure sugarcane jaggery methods.",
        "manager_lalji_photo": "",
        "manager_awadhesh_name": "Mr. Awadhesh Maurya",
        "manager_awadhesh_role": "Co-Director (Operations)",
        "manager_awadhesh_bio":  "Overseeing quality control, open iron pan cooking processes, and rural farmer alliances.",
        "manager_awadhesh_photo": "",
        "manager_arjun_name":  "Mr. Arjun Maurya",
        "manager_arjun_role":  "Co-Director (Logistics & Reach)",
        "manager_arjun_bio":   "Managing modern delivery pipelines and introducing traditional wellness to urban households.",
        "manager_arjun_photo": "",
        "branches_info":       "📍 Gorakhpur Highway Branch (Main Production House)\nVaranasi-Gorakhpur Highway, Uttar Pradesh\n\n📍 Lucknow Outlet (Retail & Inquiries)\nLal Ji Foods Plaza, Lucknow, Uttar Pradesh\n\n📍 Noida Hub (Distribution & Support)\nSector 62, Noida, Uttar Pradesh",
        "shipping_free_threshold": "500",
        "shipping_base_fee":      "50",
        "seasonal_discount_percent": "0",
        "testimonial_1_name":  "Meera K.",
        "testimonial_1_role":  "Verified Buyer • Mumbai",
        "testimonial_1_text":  "KhagRaj has completely replaced white sugar in our kitchen. The quality of jaggery blocks is incredible, and you can smell the fresh sugarcane juice aroma the moment you open the box!",
        "testimonial_1_photo": "",
        "testimonial_2_name":  "Rajesh S.",
        "testimonial_2_role":  "Sweet Shop Owner • Delhi",
        "testimonial_2_text":  "We run a high-end sweet shop and sourcing pure Palm Jaggery has always been a pain. Since finding KhagRaj, our customers have noticed a dramatic increase in product consistency and natural flavor!",
        "testimonial_2_photo": "",
        "testimonial_3_name":  "Anjali P.",
        "testimonial_3_role":  "Fitness Blogger • Pune",
        "testimonial_3_text":  "The Ginger Jaggery powder is a lifesaver for winter. I dissolve it in my chai every evening. The taste is authentic and you can feel the warmth of ginger immediately. Excellent product.",
        "testimonial_3_photo": "",
    }

    for key, value in defaults.items():
        row = SiteSetting.query.filter_by(key=key).first()
        if not row:
            db.session.add(SiteSetting(key=key, value=value))

    # Sample products
    if Product.query.count() == 0:
        sample = [
            ("Pure Sugarcane Jaggery Block",
             "Traditional hand-crafted jaggery blocks made from fresh sugarcane juice. Rich in minerals, unrefined and natural.",
             80, "kg", "sugarcane", "Bestseller", "/uploads/default_product.png", 200, True),
            ("Organic Jaggery Powder",
             "Fine-ground organic jaggery powder — easy to dissolve in tea, coffee, or desserts. 100% chemical-free.",
             120, "kg", "sugarcane", "Organic", "/uploads/default_product.png", 150, False),
            ("Palm Jaggery (Karupatti)",
             "Handmade from natural palm sap. Dark, rich and packed with antioxidants.",
             200, "kg", "palm", "Premium", "/uploads/default_product.png", 80, True),
            ("Jaggery Cubes",
             "Perfectly portioned jaggery cubes — convenient for chai, sweets and cooking.",
             100, "kg", "sugarcane", None, "/uploads/default_product.png", 180, False),
            ("Ginger Jaggery",
             "Pure jaggery infused with real ginger extract. Great for immunity and digestion.",
             150, "kg", "flavored", "New", "/uploads/default_product.png", 60, False),
            ("Cardamom Jaggery",
             "Aromatic jaggery blended with premium cardamom. Elevates your desserts and chai.",
             160, "kg", "flavored", "New", "/uploads/default_product.png", 60, False),
            ("Coconut Jaggery",
             "Made from coconut palm nectar — rare, with a distinct caramel-like flavour.",
             220, "kg", "palm", "Rare", "/uploads/default_product.png", 40, True),
            ("Jaggery Syrup (Paagu)",
             "Liquid jaggery syrup — ideal for pancakes, desserts, and direct use.",
             130, "500ml", "sugarcane", None, "/uploads/default_product.png", 90, False),
        ]
        for name, desc, price, unit, cat, badge, img, stock, featured in sample:
            db.session.add(Product(
                name=name, description=desc, price=price, unit=unit,
                category=cat, badge=badge, image_url=img,
                stock=stock, featured=featured, active=True
            ))

    db.session.commit()


# ─────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────
app = create_app()
from extensions import celery

if __name__ == "__main__":
    port  = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
