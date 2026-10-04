using ProducerConsumer.Core;

namespace Consumer;

/// <summary>Simulates a unit of work for each message.</summary>
public sealed class WorkItemHandler(ILogger<WorkItemHandler> logger) : IWorkItemHandler
{
    public async Task HandleAsync(WorkItem item, CancellationToken ct)
    {
        await Task.Delay(TimeSpan.FromMilliseconds(100 + Random.Shared.Next(400)), ct);
        logger.LogInformation("[{Host}] Consumed #{Sequence} \"{Payload}\" ({Id}), queued {Latency:F0} ms ago",
            Environment.MachineName, item.Sequence, item.Payload, item.Id,
            (DateTimeOffset.UtcNow - item.CreatedAt).TotalMilliseconds);
    }
}
