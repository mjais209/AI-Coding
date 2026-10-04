using System.Text.Json;
using Azure.Storage.Queues.Models;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace ProducerConsumer.Core;

public sealed class QueueConsumer(
    WorkQueue queue,
    IWorkItemHandler handler,
    IOptions<QueueOptions> options,
    ILogger<QueueConsumer> logger)
{
    private readonly QueueOptions _options = options.Value;

    /// <summary>Receives one batch and processes its messages concurrently. Returns the number received.</summary>
    public async Task<int> ProcessBatchAsync(CancellationToken ct = default)
    {
        QueueMessage[] messages = await queue.Queue.ReceiveMessagesAsync(
            _options.BatchSize,
            TimeSpan.FromSeconds(_options.VisibilityTimeoutSeconds),
            ct);

        await Task.WhenAll(messages.Select(m => ProcessMessageAsync(m, ct)));
        return messages.Length;
    }

    private async Task ProcessMessageAsync(QueueMessage message, CancellationToken ct)
    {
        if (message.DequeueCount > _options.MaxDequeueCount)
        {
            logger.LogError("Moving message {MessageId} to poison queue after {Attempts} attempts",
                message.MessageId, message.DequeueCount);
            await queue.PoisonQueue.SendMessageAsync(message.MessageText, ct);
            await queue.Queue.DeleteMessageAsync(message.MessageId, message.PopReceipt, ct);
            return;
        }

        try
        {
            var item = JsonSerializer.Deserialize<WorkItem>(message.MessageText, Json.Options)
                ?? throw new InvalidDataException("Message body is empty.");
            await handler.HandleAsync(item, ct);
            await queue.Queue.DeleteMessageAsync(message.MessageId, message.PopReceipt, ct);
        }
        catch (Exception ex) when (ex is not OperationCanceledException || !ct.IsCancellationRequested)
        {
            // Leave the message on the queue; it becomes visible again after the visibility timeout.
            logger.LogWarning(ex, "Failed to process message {MessageId} (attempt {Attempt})",
                message.MessageId, message.DequeueCount);
        }
    }
}
