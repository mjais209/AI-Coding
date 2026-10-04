using System.Collections.Concurrent;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.Extensions.Options;
using ProducerConsumer.Core;

namespace ProducerConsumer.Tests;

// Requires Azurite on the default ports (docker compose up azurite).
public sealed class QueueTests : IAsyncLifetime
{
    private readonly QueueOptions _options = new()
    {
        QueueName = $"test-{Guid.NewGuid():N}"[..30],
        PoisonQueueName = $"test-{Guid.NewGuid():N}"[..30] + "-poison",
        MaxDequeueCount = 2,
        VisibilityTimeoutSeconds = 1,
    };

    private WorkQueue _queue = null!;

    public async Task InitializeAsync()
    {
        _queue = new WorkQueue(Options.Create(_options));
        await _queue.EnsureCreatedAsync();
    }

    public async Task DisposeAsync()
    {
        await _queue.Queue.DeleteIfExistsAsync();
        await _queue.PoisonQueue.DeleteIfExistsAsync();
    }

    private QueueConsumer Consumer(IWorkItemHandler handler) =>
        new(_queue, handler, Options.Create(_options), NullLogger<QueueConsumer>.Instance);

    [Fact]
    public async Task Every_produced_item_is_consumed_exactly_once()
    {
        var producer = new QueueProducer(_queue, TimeProvider.System);
        var sent = new List<WorkItem>();
        for (var i = 1; i <= 25; i++)
            sent.Add(await producer.SendAsync(i, $"task #{i}"));

        var handler = new RecordingHandler();
        var consumers = new[] { Consumer(handler), Consumer(handler) };
        await DrainAsync(consumers);

        Assert.Equal(sent.Select(s => s.Id).Order(), handler.Items.Select(i => i.Id).Order());
        Assert.Equal(sent.Single(s => s.Sequence == 7).Payload, handler.Items.Single(i => i.Sequence == 7).Payload);
        Assert.Equal(0, await _queue.GetDepthAsync());
    }

    [Fact]
    public async Task Message_that_keeps_failing_moves_to_poison_queue()
    {
        await new QueueProducer(_queue, TimeProvider.System).SendAsync(1, "boom");
        var handler = new FailingHandler();
        var consumer = Consumer(handler);

        for (var attempt = 0; attempt < 10 && (await _queue.PoisonQueue.PeekMessagesAsync()).Value.Length == 0; attempt++)
        {
            await consumer.ProcessBatchAsync();
            await Task.Delay(1200);
        }

        Assert.Equal(_options.MaxDequeueCount, handler.Calls);
        var poison = (await _queue.PoisonQueue.PeekMessagesAsync()).Value;
        Assert.Single(poison);
        Assert.Contains("\"payload\":\"boom\"", poison[0].MessageText);
        Assert.Equal(0, await _queue.GetDepthAsync());
    }

    [Fact]
    public async Task Malformed_message_is_not_handled_and_ends_in_poison_queue()
    {
        await _queue.Queue.SendMessageAsync("not json");
        var handler = new RecordingHandler();
        var consumer = Consumer(handler);

        for (var attempt = 0; attempt < 10 && (await _queue.PoisonQueue.PeekMessagesAsync()).Value.Length == 0; attempt++)
        {
            await consumer.ProcessBatchAsync();
            await Task.Delay(1200);
        }

        Assert.Empty(handler.Items);
        Assert.Equal("not json", (await _queue.PoisonQueue.PeekMessagesAsync()).Value.Single().MessageText);
    }

    private async Task DrainAsync(QueueConsumer[] consumers)
    {
        var deadline = DateTime.UtcNow.AddSeconds(30);
        while (DateTime.UtcNow < deadline)
        {
            var received = await Task.WhenAll(consumers.Select(c => c.ProcessBatchAsync()));
            if (received.Sum() == 0 && await _queue.GetDepthAsync() == 0)
                return;
        }
        throw new TimeoutException("Queue was not drained.");
    }

    private sealed class RecordingHandler : IWorkItemHandler
    {
        public ConcurrentBag<WorkItem> Items { get; } = [];

        public Task HandleAsync(WorkItem item, CancellationToken ct)
        {
            Items.Add(item);
            return Task.CompletedTask;
        }
    }

    private sealed class FailingHandler : IWorkItemHandler
    {
        private int _calls;
        public int Calls => _calls;

        public Task HandleAsync(WorkItem item, CancellationToken ct)
        {
            Interlocked.Increment(ref _calls);
            throw new InvalidOperationException("simulated failure");
        }
    }
}
