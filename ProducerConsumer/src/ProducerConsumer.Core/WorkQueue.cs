using Azure.Storage.Queues;
using Microsoft.Extensions.Options;

namespace ProducerConsumer.Core;

public sealed class WorkQueue(IOptions<QueueOptions> options)
{
    public QueueClient Queue { get; } = new(options.Value.ConnectionString, options.Value.QueueName);
    public QueueClient PoisonQueue { get; } = new(options.Value.ConnectionString, options.Value.PoisonQueueName);

    public async Task EnsureCreatedAsync(CancellationToken ct = default)
    {
        await Queue.CreateIfNotExistsAsync(cancellationToken: ct);
        await PoisonQueue.CreateIfNotExistsAsync(cancellationToken: ct);
    }

    public async Task<int> GetDepthAsync(CancellationToken ct = default) =>
        (await Queue.GetPropertiesAsync(ct)).Value.ApproximateMessagesCount;
}
