namespace Orders.Core;

public sealed class StorageOptions
{
    public const string SectionName = "Storage";

    public string ConnectionString { get; set; } = "UseDevelopmentStorage=true";
    public string QueueName { get; set; } = "orders";
    public string PoisonQueueName { get; set; } = "orders-poison";
    public string ReceiptsContainer { get; set; } = "receipts";
    public string OrdersTable { get; set; } = "orders";
    public int MaxDequeueCount { get; set; } = 5;
    public int VisibilityTimeoutSeconds { get; set; } = 30;
    public int PollIntervalMilliseconds { get; set; } = 1000;
}
