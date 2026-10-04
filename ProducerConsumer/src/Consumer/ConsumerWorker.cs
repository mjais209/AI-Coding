using Microsoft.Extensions.Options;
using ProducerConsumer.Core;

namespace Consumer;

public sealed class ConsumerWorker(
    WorkQueue queue,
    QueueConsumer consumer,
    IOptions<QueueOptions> options,
    ILogger<ConsumerWorker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await queue.EnsureCreatedAsync(stoppingToken);
        logger.LogInformation("Consuming from '{Queue}'", queue.Queue.Name);
        var idleDelay = TimeSpan.FromMilliseconds(options.Value.PollIntervalMilliseconds);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                if (await consumer.ProcessBatchAsync(stoppingToken) == 0)
                    await Task.Delay(idleDelay, stoppingToken);
            }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
            {
                break;
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Error polling queue; retrying");
                await Task.Delay(idleDelay, stoppingToken);
            }
        }
    }
}
