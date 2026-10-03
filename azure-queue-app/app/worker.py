import json
import logging
import signal
import time

from app import config
from app.processing import build_receipt
from app.storage import Storage

log = logging.getLogger("worker")


def handle_message(storage: Storage, msg) -> None:
    if msg.dequeue_count > config.MAX_DEQUEUE_COUNT:
        log.error("Moving message %s to poison queue after %s attempts", msg.id, msg.dequeue_count)
        try:
            order_id = json.loads(msg.content).get("id")
            if order_id:
                storage.upsert_order(order_id, status="failed", error="exceeded max delivery attempts")
        except (ValueError, AttributeError):
            pass
        storage.dead_letter(msg)
        return

    order = json.loads(msg.content)
    storage.upsert_order(order["id"], status="processing")
    receipt = build_receipt(order)
    blob_name = storage.save_receipt(order["id"], receipt)
    storage.upsert_order(order["id"], status="processed", total=receipt["total"], receipt_blob=blob_name)
    storage.complete(msg)
    log.info("Processed order %s (total %.2f)", order["id"], receipt["total"])


def process_batch(storage: Storage) -> int:
    count = 0
    for msg in storage.receive():
        try:
            handle_message(storage, msg)
        except Exception:
            # Leave the message on the queue; it becomes visible again after the
            # visibility timeout and is retried until MAX_DEQUEUE_COUNT.
            log.exception("Failed to process message %s", msg.id)
        count += 1
    return count


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    logging.getLogger("azure").setLevel(logging.WARNING)
    storage = Storage()
    storage.ensure_resources()
    running = True

    def stop(*_):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    log.info("Worker listening on queue '%s'", config.QUEUE_NAME)
    while running:
        if process_batch(storage) == 0:
            time.sleep(config.POLL_INTERVAL)
    log.info("Worker stopped")


if __name__ == "__main__":
    main()
