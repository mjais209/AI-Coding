# ProducerConsumer (C# / .NET 8 + Azure Storage Queue)

A producer/consumer example: a **Producer** app writes work items to an
**Azure Storage Queue**, and one or more **Consumer** apps read and process them
in parallel. Failed messages are retried, and after too many attempts they are
moved to a poison queue.

```
Producer ──SendMessage──▶ queue "work-items" ──Receive (batch)──▶ Consumer ×N
                                   │                                  │
                                   │  failed > MaxDequeueCount times  │
                                   └──────▶ queue "work-items-poison" ◀┘
```

| Project | What it does |
|---|---|
| `src/ProducerConsumer.Core` | `WorkQueue` (wraps `QueueClient`), `QueueProducer`, `QueueConsumer`, `WorkItem`, `QueueOptions` |
| `src/Producer` | Worker app that sends `Producer:Count` messages (0 = send until stopped), one every `Producer:IntervalMilliseconds`, then exits |
| `src/Consumer` | Worker app (`BackgroundService`) that polls the queue, processes each batch concurrently and deletes messages that succeed |
| `tests/ProducerConsumer.Tests` | xUnit tests against Azurite: each message consumed exactly once by two consumers, poison queue, malformed messages |

## How a message is handled

1. `QueueProducer.SendAsync` serializes a `WorkItem` (`id`, `sequence`, `payload`, `created_at`) as JSON and sends it.
2. `QueueConsumer.ProcessBatchAsync` receives up to `BatchSize` messages. Each message stays invisible to other consumers for `VisibilityTimeoutSeconds`.
3. The message is passed to an `IWorkItemHandler`. The Consumer app's `WorkItemHandler` simulates work and logs it; put your own logic there.
4. On success the message is deleted. On an exception it is left on the queue and is retried when the visibility timeout ends.
5. If a message has been received more than `MaxDequeueCount` times, it is copied to the poison queue and deleted from the main queue.

## Run locally with Docker (no Azure account needed)

```bash
docker compose up --build                     # Azurite + 1 producer + 2 consumers
PRODUCER_COUNT=100 docker compose up --build  # send more messages
docker compose run --rm producer              # send another batch while the consumers keep running
```

The two consumer replicas share the queue, so each message shows up in the logs of only one of them.

## Run without Docker

```bash
docker run -d -p 10001:10001 mcr.microsoft.com/azure-storage/azurite azurite-queue --queueHost 0.0.0.0
dotnet run --project src/Consumer    # in one terminal (start more than one if you like)
dotnet run --project src/Producer    # in another
dotnet test                          # needs Azurite running
```

## Use a real Azure Storage account

```bash
az group create -n producer-consumer-rg -l eastus
az storage account create -n <uniquename> -g producer-consumer-rg --sku Standard_LRS
export AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string -n <uniquename> -g producer-consumer-rg -o tsv)
docker compose up --build producer consumer
# or, without Docker: export Queue__ConnectionString="$AZURE_STORAGE_CONNECTION_STRING"
```

Both apps create their queues on startup if they don't exist.

## Configuration

Set these in `appsettings.json` or as environment variables (`Queue__QueueName`, `Producer__Count`, ...).

| Setting | Default | Meaning |
|---|---|---|
| `Queue:ConnectionString` | `UseDevelopmentStorage=true` | Storage connection string (Azurite by default) |
| `Queue:QueueName` | `work-items` | Main queue |
| `Queue:PoisonQueueName` | `work-items-poison` | Where messages go after too many failures |
| `Queue:MaxDequeueCount` | `5` | Attempts allowed before a message goes to the poison queue |
| `Queue:BatchSize` | `16` | Messages per receive (max 32) |
| `Queue:VisibilityTimeoutSeconds` | `30` | How long a received message stays hidden before it is retried |
| `Queue:PollIntervalMilliseconds` | `1000` | Wait time when the queue is empty |
| `Producer:Count` | `20` | Messages to send (0 = send until stopped) |
| `Producer:IntervalMilliseconds` | `250` | Delay between messages |
