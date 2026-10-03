from app.processing import build_receipt


def test_build_receipt_totals():
    receipt = build_receipt(
        {
            "id": "abc",
            "customer": "Ada",
            "items": [
                {"sku": "A", "quantity": 2, "unit_price": 10.0},
                {"sku": "B", "quantity": 1, "unit_price": 5.5},
            ],
        }
    )
    assert receipt["subtotal"] == 25.5
    assert receipt["tax"] == 2.04
    assert receipt["total"] == 27.54
    assert [line["line_total"] for line in receipt["lines"]] == [20.0, 5.5]
