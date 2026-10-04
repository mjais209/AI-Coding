using System.Text.Json;
using Azure;
using Azure.Data.Tables;
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;
using Azure.Storage.Queues;
using Azure.Storage.Queues.Models;
using Microsoft.Extensions.Options;

namespace Orders.Core;

/// <summary>Wraps the Azure Queue, Blob and Table Storage clients used by the API and worker.</summary>
public sealed class OrderStorage
{
    public const string PartitionKey = "order";

    private readonly StorageOptions _options;

    public OrderStorage(IOptions<StorageOptions> options)
    {
        _options = options.Value;
        Queue = new QueueClient(_options.ConnectionString, _options.QueueName);
        PoisonQueue = new QueueClient(_options.ConnectionString, _options.PoisonQueueName);
        Receipts = new BlobContainerClient(_options.ConnectionString, _options.ReceiptsContainer);
        Orders = new TableClient(_options.ConnectionString, _options.OrdersTable);
    }

    public QueueClient Queue { get; }
    public QueueClient PoisonQueue { get; }
    public BlobContainerClient Receipts { get; }
    public TableClient Orders { get; }

    public async Task EnsureResourcesAsync(CancellationToken ct = default)
    {
        await Queue.CreateIfNotExistsAsync(cancellationToken: ct);
        await PoisonQueue.CreateIfNotExistsAsync(cancellationToken: ct);
        await Receipts.CreateIfNotExistsAsync(cancellationToken: ct);
        await Orders.CreateIfNotExistsAsync(ct);
    }

    // Queue
    public Task EnqueueAsync(OrderMessage message, CancellationToken ct = default) =>
        Queue.SendMessageAsync(JsonSerializer.Serialize(message, Json.Options), ct);

    public async Task<QueueMessage[]> ReceiveAsync(int maxMessages = 16, CancellationToken ct = default)
    {
        var response = await Queue.ReceiveMessagesAsync(
            maxMessages, TimeSpan.FromSeconds(_options.VisibilityTimeoutSeconds), ct);
        return response.Value;
    }

    public Task CompleteAsync(QueueMessage message, CancellationToken ct = default) =>
        Queue.DeleteMessageAsync(message.MessageId, message.PopReceipt, ct);

    public async Task DeadLetterAsync(QueueMessage message, CancellationToken ct = default)
    {
        await PoisonQueue.SendMessageAsync(message.MessageText, ct);
        await CompleteAsync(message, ct);
    }

    public async Task<int> GetQueueDepthAsync(CancellationToken ct = default) =>
        (await Queue.GetPropertiesAsync(ct)).Value.ApproximateMessagesCount;

    // Table
    public Task UpsertOrderAsync(string orderId, IDictionary<string, object?> fields, CancellationToken ct = default)
    {
        var entity = new TableEntity(PartitionKey, orderId) { ["UpdatedAt"] = DateTimeOffset.UtcNow };
        foreach (var (key, value) in fields)
            entity[key] = value;
        return Orders.UpsertEntityAsync(entity, TableUpdateMode.Merge, ct);
    }

    public async Task<OrderRecord?> GetOrderAsync(string orderId, CancellationToken ct = default)
    {
        var response = await Orders.GetEntityIfExistsAsync<TableEntity>(PartitionKey, orderId, cancellationToken: ct);
        return response.HasValue ? ToRecord(response.Value!) : null;
    }

    public async Task<List<OrderRecord>> ListOrdersAsync(int limit = 50, CancellationToken ct = default)
    {
        var orders = new List<OrderRecord>();
        await foreach (var entity in Orders.QueryAsync<TableEntity>($"PartitionKey eq '{PartitionKey}'", cancellationToken: ct))
            orders.Add(ToRecord(entity));
        return orders.OrderByDescending(o => o.CreatedAt).Take(limit).ToList();
    }

    // Blob
    public async Task<string> SaveReceiptAsync(Receipt receipt, CancellationToken ct = default)
    {
        var blob = Receipts.GetBlobClient($"{receipt.OrderId}.json");
        var content = BinaryData.FromObjectAsJson(receipt, Json.Options);
        await blob.UploadAsync(content, new BlobUploadOptions
        {
            HttpHeaders = new BlobHttpHeaders { ContentType = "application/json" },
        }, ct);
        return blob.Name;
    }

    public async Task<Receipt?> GetReceiptAsync(string orderId, CancellationToken ct = default)
    {
        try
        {
            var result = await Receipts.GetBlobClient($"{orderId}.json").DownloadContentAsync(ct);
            return result.Value.Content.ToObjectFromJson<Receipt>(Json.Options);
        }
        catch (RequestFailedException ex) when (ex.Status == 404)
        {
            return null;
        }
    }

    private static OrderRecord ToRecord(TableEntity e)
    {
        var items = e.GetString("Items") is { } json
            ? JsonSerializer.Deserialize<List<OrderItem>>(json, Json.Options)
            : null;
        return new OrderRecord(
            e.RowKey,
            e.GetString("Customer"),
            e.GetString("Status"),
            e.GetDateTimeOffset("CreatedAt"),
            e.GetDateTimeOffset("UpdatedAt"),
            items,
            e.GetDouble("Total"),
            e.GetString("ReceiptBlob"),
            e.GetString("Error"));
    }
}
