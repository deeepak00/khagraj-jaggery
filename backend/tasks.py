"""
Celery tasks.
Runs eagerly (synchronously) when CELERY_TASK_ALWAYS_EAGER=True
(i.e. when Redis is not configured in development).
"""
from extensions import celery, mail
from flask_mail import Message


# ─────────────────────────────────────────────────────
# EMAIL HELPERS
# ─────────────────────────────────────────────────────
STATUS_MESSAGES = {
    "pending":    ("Order Received 🎉",
                   "We have received your order and it is being reviewed."),
    "confirmed":  ("Order Confirmed ✅",
                   "Your order has been confirmed and will be prepared soon."),
    "processing": ("Order Being Prepared ⚙️",
                   "Our team is preparing your order with care."),
    "shipped":    ("Order Shipped 🚚",
                   "Your order is on its way! Estimated delivery in 2–3 days."),
    "delivered":  ("Order Delivered 🎉",
                   "Your order has been delivered. Thank you for shopping with KhagRaj!"),

    "cancelled":  ("Order Cancelled ❌",
                   "Your order has been cancelled. Please contact us if you have questions."),
}


def _build_status_email(order, new_status: str) -> str:
    title, msg = STATUS_MESSAGES.get(new_status, ("Order Update", "Your order status has changed."))
    items_html = "".join(
        f"<tr><td style='padding:6px 10px'>{i['name']}</td>"
        f"<td style='padding:6px 10px;text-align:center'>×{i['qty']}</td>"
        f"<td style='padding:6px 10px;text-align:right'>₹{i['price']*i['qty']:.0f}</td></tr>"
        for i in (order.items or [])
    )
    badge_color = {
        "pending":"#C8882A","confirmed":"#2980b9","processing":"#8e44ad",
        "shipped":"#2c3e50","delivered":"#27ae60","cancelled":"#c0392b",
    }.get(new_status, "#C8882A")

    subtotal = order.subtotal or sum(item['price'] * item['qty'] for item in (order.items or []))
    discount_amount = order.discount_amount or 0.0
    shipping_fee = order.shipping_fee or 0.0

    footer_rows = []
    footer_rows.append(
        f"<tr><td colspan='2' style='padding:6px 10px;text-align:right;color:#5C3317;font-size:.9rem'>Subtotal</td>"
        f"<td style='padding:6px 10px;text-align:right;color:#5C3317;font-size:.9rem'>₹{subtotal:.0f}</td></tr>"
    )
    if discount_amount > 0:
        footer_rows.append(
            f"<tr><td colspan='2' style='padding:6px 10px;text-align:right;color:#c0392b;font-size:.9rem'>Discount</td>"
            f"<td style='padding:6px 10px;text-align:right;color:#c0392b;font-size:.9rem'>−₹{discount_amount:.0f}</td></tr>"
        )
    shipping_text = "Free" if shipping_fee == 0 else f"₹{shipping_fee:.0f}"
    footer_rows.append(
        f"<tr><td colspan='2' style='padding:6px 10px;text-align:right;color:#5C3317;font-size:.9rem'>Delivery Fee</td>"
        f"<td style='padding:6px 10px;text-align:right;color:#5C3317;font-size:.9rem'>{shipping_text}</td></tr>"
    )
    footer_rows.append(
        f"<tr style='border-top:2px solid #F7EDD0'><td colspan='2' style='padding:10px;font-weight:700;color:#2C1810'>Total</td>"
        f"<td style='padding:10px;text-align:right;font-weight:700;color:#C8882A;font-size:1.1rem'>₹{order.total:.0f}</td></tr>"
    )
    footer_html = "".join(footer_rows)

    return f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"></head>
<body style="font-family:'Segoe UI',sans-serif;background:#f7f3e9;margin:0;padding:32px">
<div style="max-width:580px;margin:0 auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(44,24,16,.15)">
  <div style="background:#2C1810;padding:32px 40px;text-align:center">
    <h1 style="color:#F5C97A;font-size:2rem;margin:0">KhagRaj</h1>
    <p style="color:rgba(253,246,227,.6);margin:6px 0 0;font-size:.9rem">Pure Jaggery, Ancient Goodness — An Initiative by Lal Ji Foods</p>
  </div>
  <div style="padding:36px 40px">
    <span style="background:{badge_color};color:#fff;padding:5px 16px;border-radius:50px;font-size:.82rem;font-weight:600;text-transform:uppercase">{new_status}</span>
    <h2 style="color:#2C1810;margin:20px 0 8px">{title}</h2>
    <p style="color:#5C3317;line-height:1.6">{msg}</p>
    <div style="background:#FDF6E3;border-radius:12px;padding:16px 20px;margin:24px 0">
      <p style="color:#9B7B5A;font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;margin:0 0 6px">Order Number</p>
      <p style="color:#C8882A;font-size:1.4rem;font-weight:700;margin:0;letter-spacing:2px">{order.order_number}</p>
    </div>
    <table style="width:100%;border-collapse:collapse;margin-bottom:16px">
      <thead><tr style="background:#F7EDD0">
        <th style="padding:8px 10px;text-align:left;font-size:.82rem;color:#5C3317">Item</th>
        <th style="padding:8px 10px;text-align:center;font-size:.82rem;color:#5C3317">Qty</th>
        <th style="padding:8px 10px;text-align:right;font-size:.82rem;color:#5C3317">Amount</th>
      </tr></thead>
      <tbody>{items_html}</tbody>
      <tfoot>{footer_html}</tfoot>
    </table>
    <p style="color:#9B7B5A;font-size:.85rem;margin-top:24px">
      📍 Delivery to: {order.address}, {order.city}, {order.state} – {order.pincode}
    </p>
  </div>
  <div style="background:#F7EDD0;padding:20px 40px;text-align:center">
    <p style="color:#9B7B5A;font-size:.8rem;margin:0">
      © KhagRaj | Pure Jaggery Straight from the Fields<br>
      An Initiative by Lal Ji Foods | For support contact us at khagrajindia2017@gmail.com
    </p>
  </div>

</div>
</body></html>
"""


def _build_confirmation_email(order) -> str:
    return _build_status_email(order, "pending")


# ─────────────────────────────────────────────────────
# TASKS
# ─────────────────────────────────────────────────────
@celery.task(name="tasks.send_order_confirmation")
def send_order_confirmation_task(order_id: int):
    from extensions import db
    from models.models import Order
    order = db.session.get(Order, order_id)
    if not order or not order.email:
        return
    try:
        msg = Message(
            subject=f"Order Confirmed – {order.order_number} | KhagRaj",
            recipients=[order.email],
            html=_build_confirmation_email(order),
        )
        mail.send(msg)
    except Exception as exc:
        print(f"[EMAIL ERROR] confirmation for {order.order_number}: {exc}")


@celery.task(name="tasks.send_status_update")
def send_status_update_task(order_id: int, old_status: str, new_status: str):
    from extensions import db
    from models.models import Order
    order = db.session.get(Order, order_id)
    if not order or not order.email:
        return
    title, _ = STATUS_MESSAGES.get(new_status, ("Order Update", ""))

    try:
        msg = Message(
            subject=f"{title} – {order.order_number} | KhagRaj",

            recipients=[order.email],
            html=_build_status_email(order, new_status),
        )
        mail.send(msg)
    except Exception as exc:
        print(f"[EMAIL ERROR] status update for {order.order_number}: {exc}")


import threading
from flask import current_app

def run_async_task(task_func, *args, **kwargs):
    """
    Runs a task asynchronously. If Celery is running in eager mode (e.g. no Redis),
    it spawns a background thread to execute the task without blocking the main thread.
    Otherwise, it delegates to Celery .delay().
    """
    if current_app.config.get("CELERY_TASK_ALWAYS_EAGER"):
        app = current_app._get_current_object()
        def target():
            with app.app_context():
                try:
                    task_func(*args, **kwargs)
                except Exception as e:
                    app.logger.error(f"Async thread task failed: {e}")
        threading.Thread(target=target, daemon=True).start()
    else:
        task_func.delay(*args, **kwargs)
