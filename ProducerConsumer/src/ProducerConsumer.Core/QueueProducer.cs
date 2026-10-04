using System.Text.Json;

namespace ProducerConsumer.Core;

public sealed class QueueProducer(WorkQueue queue, TimeProvider clock)
{
    public async Task<WorkItem> SendAsync(int sequence, string payload, CancellationToken ct = default)
    {
        var item = new WorkItem(Guid.NewGuid().ToString(), sequence, payload, clock.GetUtcNow());
        await queue.Queue.SendMessageAsync(JsonSerializer.Serialize(item, Json.Options), ct);
        return item;
    }
}
