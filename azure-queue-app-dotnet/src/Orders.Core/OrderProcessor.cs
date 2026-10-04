using System.Text.Json;
using Azure.Storage.Queues.Models;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace Orders.Core;

/// <summary>Pulls order messages off the queue, writes receipts to Blob Storage and status to Table Storage.</summary>
public sealed class OrderProcessor(OrderStorage storage, IOptions<StorageOptions> options, ILogger<OrderProcessor> logger)
{
    private readonly StorageOptions _options = options.Value;

    public async Task<int> ProcessBatchAsync(CancellationToken ct = default)
    {
        var messages = await storage.ReceiveAsync(ct: ct);
        foreach (var message in messages)
        {
            try
            {
                await HandleMessageAsync(message, ct);
            }
            catch (Exception ex) when (ex is not OperationCanceledException)
            {
                // The message stays on the queue, becomes visible again after the
                // visibility timeout and is retried until MaxDequeueCount is exceeded.
                logger.LogError(ex, "Failed to process message {MessageId}", message.MessageId);
            }
        }
        return messages.Length;
    }

    public async Task HandleMessageAsync(QueueMessage message, CancellationToken ct = default)
    {
        if (message.DequeueCount > _options.MaxDequeueCount)
        {
            logger.LogError("Moving message {MessageId} to poison queue after {Attempts} attempts",
                message.MessageId, message.DequeueCount);
            if (TryGetOrderId(message.MessageText) is { } failedId)
            {
                await storage.UpsertOrderAsync(failedId, new Dictionary<string, object?>
                {
                    ["Status"] = OrderStatus.Failed,
                    ["Error"] = "exceeded max delivery attempts",
                }, ct);
            }
            await storage.DeadLetterAsync(message, ct);
            return;
        }

        var order = JsonSerializer.Deserialize<OrderMessage>(message.MessageText, Json.Options)
            ?? throw new InvalidOperationException("Empty order message");
        if (order.Items is null || order.Items.Count == 0)
            throw new InvalidOperationException($"Order {order.Id} has no items");

        await storage.UpsertOrderAsync(order.Id, new Dictionary<string, object?> { ["Status"] = OrderStatus.Processing }, ct);
        var receipt = ReceiptBuilder.Build(order);
        var blobName = await storage.SaveReceiptAsync(receipt, ct);
        await storage.UpsertOrderAsync(order.Id, new Dictionary<string, object?>
        {
            ["Status"] = OrderStatus.Processed,
            ["Total"] = (double)receipt.Total,
            ["ReceiptBlob"] = blobName,
        }, ct);
        await storage.CompleteAsync(message, ct);
        logger.LogInformation("Processed order {OrderId} (total {Total})", order.Id, receipt.Total);
    }

    private static string? TryGetOrderId(string json)
    {
        try
        {
            using var doc = JsonDocument.Parse(json);
            return doc.RootElement.TryGetProperty("id", out var id) ? id.GetString() : null;
        }
        catch (JsonException)
        {
            return null;
        }
    }
}
