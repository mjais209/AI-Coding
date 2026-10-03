import json
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.models import OrderRequest
from app.storage import Storage, utcnow

storage = Storage()


@asynccontextmanager
async def lifespan(_: FastAPI):
    storage.ensure_resources()
    yield


app = FastAPI(title="Azure Queue Orders", lifespan=lifespan)


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.post("/orders", status_code=202)
def create_order(order: OrderRequest):
    order_id = str(uuid.uuid4())
    payload = {"id": order_id, **order.model_dump()}
    storage.upsert_order(
        order_id,
        customer=order.customer,
        status="queued",
        created_at=utcnow(),
        items=json.dumps(payload["items"]),
    )
    storage.enqueue(payload)
    return {"id": order_id, "status": "queued"}


@app.get("/orders")
def list_orders():
    return storage.list_orders()


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = storage.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/orders/{order_id}/receipt")
def get_receipt(order_id: str):
    receipt = storage.get_receipt(order_id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="Receipt not available yet")
    return receipt


@app.get("/health")
def health():
    return {"status": "ok", "queue_depth": storage.queue_depth()}
