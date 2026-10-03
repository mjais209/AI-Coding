import os

AZURITE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    "QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
    "TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
)

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", AZURITE_CONNECTION_STRING)
QUEUE_NAME = os.getenv("ORDERS_QUEUE", "orders")
POISON_QUEUE_NAME = os.getenv("ORDERS_POISON_QUEUE", "orders-poison")
BLOB_CONTAINER = os.getenv("RECEIPTS_CONTAINER", "receipts")
TABLE_NAME = os.getenv("ORDERS_TABLE", "orders")
MAX_DEQUEUE_COUNT = int(os.getenv("MAX_DEQUEUE_COUNT", "5"))
VISIBILITY_TIMEOUT = int(os.getenv("VISIBILITY_TIMEOUT", "30"))
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "1.0"))
