import json
from datetime import datetime, timezone

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.data.tables import TableServiceClient, UpdateMode
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.storage.queue import QueueClient

from app import config

PARTITION_KEY = "order"


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class Storage:
    """Thin wrapper around Azure Queue, Blob and Table Storage clients."""

    def __init__(self, connection_string: str = config.CONNECTION_STRING):
        self.queue = QueueClient.from_connection_string(connection_string, config.QUEUE_NAME)
        self.poison_queue = QueueClient.from_connection_string(connection_string, config.POISON_QUEUE_NAME)
        self.blobs = BlobServiceClient.from_connection_string(connection_string).get_container_client(
            config.BLOB_CONTAINER
        )
        self.table = TableServiceClient.from_connection_string(connection_string).get_table_client(config.TABLE_NAME)

    def ensure_resources(self) -> None:
        for create in (
            self.queue.create_queue,
            self.poison_queue.create_queue,
            self.blobs.create_container,
            self.table.create_table,
        ):
            try:
                create()
            except ResourceExistsError:
                pass

    # Queue
    def enqueue(self, message: dict) -> None:
        self.queue.send_message(json.dumps(message))

    def receive(self, max_messages: int = 16):
        return self.queue.receive_messages(
            messages_per_page=max_messages, visibility_timeout=config.VISIBILITY_TIMEOUT
        )

    def complete(self, msg) -> None:
        self.queue.delete_message(msg)

    def dead_letter(self, msg) -> None:
        self.poison_queue.send_message(msg.content)
        self.queue.delete_message(msg)

    def queue_depth(self) -> int:
        return self.queue.get_queue_properties().approximate_message_count

    # Table
    def upsert_order(self, order_id: str, **fields) -> None:
        entity = {"PartitionKey": PARTITION_KEY, "RowKey": order_id, "updated_at": utcnow(), **fields}
        self.table.upsert_entity(entity, mode=UpdateMode.MERGE)

    def get_order(self, order_id: str) -> dict | None:
        try:
            return _entity_to_dict(self.table.get_entity(PARTITION_KEY, order_id))
        except ResourceNotFoundError:
            return None

    def list_orders(self, limit: int = 50) -> list[dict]:
        entities = self.table.query_entities(f"PartitionKey eq '{PARTITION_KEY}'")
        orders = [_entity_to_dict(e) for e in entities]
        orders.sort(key=lambda o: o.get("created_at", ""), reverse=True)
        return orders[:limit]

    # Blob
    def save_receipt(self, order_id: str, receipt: dict) -> str:
        blob = self.blobs.get_blob_client(f"{order_id}.json")
        blob.upload_blob(
            json.dumps(receipt, indent=2),
            overwrite=True,
            content_settings=ContentSettings(content_type="application/json"),
        )
        return blob.blob_name

    def get_receipt(self, order_id: str) -> dict | None:
        try:
            data = self.blobs.get_blob_client(f"{order_id}.json").download_blob().readall()
        except ResourceNotFoundError:
            return None
        return json.loads(data)


def _entity_to_dict(entity) -> dict:
    data = dict(entity)
    data["id"] = data.pop("RowKey")
    data.pop("PartitionKey", None)
    return data
