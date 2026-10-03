from app.storage import utcnow

TAX_RATE = 0.08


def build_receipt(order: dict) -> dict:
    """Business logic run by the worker for each order message."""
    lines = []
    for item in order["items"]:
        line_total = round(item["quantity"] * item["unit_price"], 2)
        lines.append({**item, "line_total": line_total})
    subtotal = round(sum(line["line_total"] for line in lines), 2)
    tax = round(subtotal * TAX_RATE, 2)
    return {
        "order_id": order["id"],
        "customer": order["customer"],
        "lines": lines,
        "subtotal": subtotal,
        "tax": tax,
        "total": round(subtotal + tax, 2),
        "processed_at": utcnow(),
    }
