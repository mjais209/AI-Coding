# Azure Queue Orders

A small order-processing app built on a message queue and Azure cloud storage.

```
 client ──POST /orders──▶  API (FastAPI)  ──send──▶  Azure Storage Queue "orders"
                              │                              │
                              │ status = queued              │ receive (visibility timeout)
                              ▼                              ▼
                       Azure Table "orders"  ◀──update──  Worker(s)
                                                             │ upload receipt JSON
                                                             ▼
                                                   Azure Blob container "receipts"
```

- **API** (`app/api.py`): validates the order, writes a `queued` row to Table Storage, and puts a message on the queue. It returns `202 Accepted` straight away.
- **Worker** (`app/worker.py`): polls the queue, computes the receipt (`app/processing.py`), uploads it to Blob Storage, marks the order `processed`, and deletes the message. If a message fails, it becomes visible again and is retried. After `MAX_DEQUEUE_COUNT` attempts it is moved to the `orders-poison` queue and the order is marked `failed`. You can run more than one worker in parallel.
- **UI**: a small page at `/` where you can submit orders and watch their status and receipts.

## Run locally (Docker, no Azure account needed)

```bash
docker compose up --build
```

This starts the [Azurite](https://learn.microsoft.com/azure/storage/common/storage-use-azurite) storage emulator, the API on http://localhost:8000 and 2 workers. API docs are at http://localhost:8000/docs.

## Run without Docker

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
docker run -d -p 10000-10002:10000-10002 mcr.microsoft.com/azure-storage/azurite \
  azurite --blobHost 0.0.0.0 --queueHost 0.0.0.0 --tableHost 0.0.0.0 --skipApiVersionCheck --loose
uvicorn app.api:app --reload      # terminal 1
python -m app.worker              # terminal 2
pytest                            # unit + end-to-end tests against Azurite
```

## Use real Azure Storage

```bash
az group create -n orders-rg -l eastus
az storage account create -n <uniquename> -g orders-rg --sku Standard_LRS
export AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string -n <uniquename> -g orders-rg -o tsv)
docker compose up --build api worker
```

The app creates the queue, poison queue, blob container and table on startup if they don't exist yet.

## API

| Method | Path | Description |
| --- | --- | --- |
| POST | `/orders` | `{"customer": "Ada", "items": [{"sku": "A1", "quantity": 2, "unit_price": 9.99}]}` → `202 {"id", "status": "queued"}` |
| GET | `/orders` | Recent orders from Table Storage |
| GET | `/orders/{id}` | One order's status (`queued` / `processing` / `processed` / `failed`) |
| GET | `/orders/{id}/receipt` | Receipt JSON from Blob Storage (`404` until processed) |
| GET | `/health` | Health check plus approximate queue depth |

## Configuration (environment variables)

| Variable | Default |
| --- | --- |
| `AZURE_STORAGE_CONNECTION_STRING` | Azurite on localhost |
| `ORDERS_QUEUE` / `ORDERS_POISON_QUEUE` | `orders` / `orders-poison` |
| `RECEIPTS_CONTAINER` | `receipts` |
| `ORDERS_TABLE` | `orders` |
| `MAX_DEQUEUE_COUNT` | `5` |
| `VISIBILITY_TIMEOUT` (s) | `30` |
| `POLL_INTERVAL` (s) | `1.0` |
