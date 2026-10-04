using Microsoft.Extensions.Options;
using ProducerConsumer.Core;

namespace Producer;

public sealed class ProducerWorker(
    WorkQueue queue,
    QueueProducer producer,
    IOptions<ProducerOptions> options,
    IHostApplicationLifetime lifetime,
    ILogger<ProducerWorker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var opts = options.Value;
        await queue.EnsureCreatedAsync(stoppingToken);
        logger.LogInformation("Producing {Count} messages to '{Queue}'",
            opts.Count == 0 ? "unlimited" : opts.Count, queue.Queue.Name);

        try
        {
            for (var i = 1; opts.Count == 0 || i <= opts.Count; i++)
            {
                var item = await producer.SendAsync(i, $"task #{i}", stoppingToken);
                logger.LogInformation("Produced #{Sequence} ({Id})", item.Sequence, item.Id);
                await Task.Delay(opts.IntervalMilliseconds, stoppingToken);
            }
            logger.LogInformation("Done. Queue depth is now ~{Depth}", await queue.GetDepthAsync(stoppingToken));
        }
        catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
        {
        }
        finally
        {
            lifetime.StopApplication();
        }
    }
}
