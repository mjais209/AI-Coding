# Azure Queue Orders (.NET 8)

A small order-processing app built on a message queue and Azure cloud storage, written in C# / .NET 8.

```
 client ──POST /api/orders──▶  Orders.Api (ASP.NET Core) ──send──▶  Azure Storage Queue "orders"
                                   │                                        │
                                   │ Status = queued                        │ receive (visibility timeout)
                                   ▼                                        ▼
                            Azure Table "orders"  ◀──update──  Orders.Worker (BackgroundService) ×N
                                                                            │ upload receipt JSON
                                                                            ▼
                                                                 Azure Blob container "receipts"
```

| Project | Purpose |
| --- | --- |
| `src/Orders.Core` | Shared code: `OrderStorage` (wraps the `Azure.Storage.Queues`, `Azure.Storage.Blobs` and `Azure.Data.Tables` clients), `OrderProcessor` (message handling, retries, poison queue), `ReceiptBuilder`, models and validation |
| `src/Orders.Api` | ASP.NET Core minimal API plus a small web UI (`wwwroot/index.html`) |
| `src/Orders.Worker` | .NET Worker Service that polls the queue and processes orders. You can run more than one copy in parallel. |
| `tests/Orders.Tests` | xUnit unit tests, plus end-to-end tests against Azurite using `WebApplicationFactory` |

**Retries and the poison queue:** a message that fails to process stays on the queue and becomes visible again after `VisibilityTimeoutSeconds`. After `MaxDequeueCount` attempts it is moved to the `orders-poison` queue and the order is marked `failed`.

## Run locally (Docker, no Azure account needed)

```bash
docker compose up --build
```

This starts the [Azurite](https://learn.microsoft.com/azure/storage/common/storage-use-azurite) storage emulator, the API + UI on http://localhost:8080 and 2 workers.

## Run without Docker

Requires the [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0).

```bash
docker run -d -p 10000-10002:10000-10002 mcr.microsoft.com/azure-storage/azurite \
  azurite --blobHost 0.0.0.0 --queueHost 0.0.0.0 --tableHost 0.0.0.0 --skipApiVersionCheck --loose

dotnet run --project src/Orders.Api       # terminal 1 -> http://localhost:5000
dotnet run --project src/Orders.Worker    # terminal 2
dotnet test                               # all tests (integration tests need Azurite)
dotnet test --filter "Category!=Integration"   # unit tests only
```

The default connection string is `UseDevelopmentStorage=true`, which points at Azurite on localhost.

## Use real Azure Storage

```bash
az group create -n orders-rg -l eastus
az storage account create -n <uniquename> -g orders-rg --sku Standard_LRS
export AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string -n <uniquename> -g orders-rg -o tsv)
docker compose up --build api worker
```

When you run without Docker, set `Storage__ConnectionString` instead, either as an environment variable or with `dotnet user-secrets`. The app creates the queues, blob container and table on startup if they don't exist yet.

## API

| Method | Path | Description |
| --- | --- | --- |
| POST | `/api/orders` | `{"customer": "Ada", "items": [{"sku": "A1", "quantity": 2, "unit_price": 9.99}]}` → `202 {"id", "status": "queued"}`, or `400` with validation errors |
| GET | `/api/orders` | Recent orders from Table Storage |
| GET | `/api/orders/{id}` | One order's status (`queued` / `processing` / `processed` / `failed`) |
| GET | `/api/orders/{id}/receipt` | Receipt JSON from Blob Storage (`404` until processed) |
| GET | `/api/health` | Health check plus approximate queue depth |

## Configuration (`Storage` section in `appsettings.json`, or `Storage__*` environment variables)

| Setting | Default |
| --- | --- |
| `ConnectionString` | `UseDevelopmentStorage=true` |
| `QueueName` / `PoisonQueueName` | `orders` / `orders-poison` |
| `ReceiptsContainer` | `receipts` |
| `OrdersTable` | `orders` |
| `MaxDequeueCount` | `5` |
| `VisibilityTimeoutSeconds` | `30` |
| `PollIntervalMilliseconds` | `1000` |
