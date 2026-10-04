using Microsoft.Extensions.Options;
using Orders.Core;

namespace Orders.Worker;

public sealed class OrderWorker(
    OrderStorage storage,
    OrderProcessor processor,
    IOptions<StorageOptions> options,
    ILogger<OrderWorker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await storage.EnsureResourcesAsync(stoppingToken);
        logger.LogInformation("Worker listening on queue '{Queue}'", options.Value.QueueName);
        var idleDelay = TimeSpan.FromMilliseconds(options.Value.PollIntervalMilliseconds);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                if (await processor.ProcessBatchAsync(stoppingToken) == 0)
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
