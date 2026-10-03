"""End-to-end tests against Azurite (or a real storage account via AZURE_STORAGE_CONNECTION_STRING)."""

import json
import os
import time
import uuid

import pytest

suffix = uuid.uuid4().hex[:8]
os.environ.setdefault("ORDERS_QUEUE", f"orders-{suffix}")
os.environ.setdefault("ORDERS_POISON_QUEUE", f"orders-poison-{suffix}")
os.environ.setdefault("RECEIPTS_CONTAINER", f"receipts-{suffix}")
os.environ.setdefault("ORDERS_TABLE", f"orders{suffix}")
os.environ.setdefault("MAX_DEQUEUE_COUNT", "1")
os.environ.setdefault("VISIBILITY_TIMEOUT", "1")

from fastapi.testclient import TestClient  # noqa: E402

from app import api, worker  # noqa: E402
from app.storage import Storage  # noqa: E402

@pytest.fixture(scope="module")
def storage():
    s = Storage()
    try:
        s.ensure_resources()
    except Exception as exc:
        pytest.skip(f"Azure Storage not reachable: {exc}")
    yield s
    s.queue.delete_queue()
    s.poison_queue.delete_queue()
    s.blobs.delete_container()
    s.table.delete_table()

@pytest.fixture(scope="module")
def client(storage):
    with TestClient(api.app) as c:
        yield c

def test_order_flows_through_queue_to_storage(client, storage):
    res = client.post(
        "/orders",
        json={"customer": "Ada", "items": [{"sku": "A", "quantity": 3, "unit_price": 2.5}]},
    )
    assert res.status_code == 202
    order_id = res.json()["id"]

    assert client.get(f"/orders/{order_id}").json()["status"] == "queued"
    assert client.get(f"/orders/{order_id}/receipt").status_code == 404

    assert worker.process_batch(storage) == 1

    order = client.get(f"/orders/{order_id}").json()
    assert order["status"] == "processed"
    assert order["total"] == 8.1
    receipt = client.get(f"/orders/{order_id}/receipt").json()
    assert receipt["order_id"] == order_id
    assert any(o["id"] == order_id for o in client.get("/orders").json())

def test_invalid_order_rejected(client):
    assert client.post("/orders", json={"customer": "Ada", "items": []}).status_code == 422

def test_poison_message_is_dead_lettered(storage):
    order_id = str(uuid.uuid4())
    storage.upsert_order(order_id, status="queued")
    storage.enqueue({"id": order_id, "customer": "Bad"})  # missing "items" -> processing fails

    assert worker.process_batch(storage) == 1  # first attempt fails, message stays on queue

    time.sleep(1.5)  # wait for visibility timeout
    assert worker.process_batch(storage) == 1  # exceeds MAX_DEQUEUE_COUNT -> poison queue

    poisoned = [json.loads(m.content) for m in storage.poison_queue.receive_messages()]
    assert any(m["id"] == order_id for m in poisoned)
    assert storage.get_order(order_id)["status"] == "failed"
