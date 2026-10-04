namespace ProducerConsumer.Core;

public sealed class QueueOptions
{
    public const string SectionName = "Queue";

    public string ConnectionString { get; set; } = "UseDevelopmentStorage=true";
    public string QueueName { get; set; } = "work-items";
    public string PoisonQueueName { get; set; } = "work-items-poison";
    public int MaxDequeueCount { get; set; } = 5;
    public int BatchSize { get; set; } = 16;
    public int VisibilityTimeoutSeconds { get; set; } = 30;
    public int PollIntervalMilliseconds { get; set; } = 1000;
}
