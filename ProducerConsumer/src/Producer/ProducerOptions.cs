namespace Producer;

public sealed class ProducerOptions
{
    public const string SectionName = "Producer";

    /// <summary>Number of messages to send before exiting. 0 means run until stopped.</summary>
    public int Count { get; set; } = 20;
    public int IntervalMilliseconds { get; set; } = 250;
}
