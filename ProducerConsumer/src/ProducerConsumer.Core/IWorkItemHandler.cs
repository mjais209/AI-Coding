namespace ProducerConsumer.Core;

public interface IWorkItemHandler
{
    Task HandleAsync(WorkItem item, CancellationToken ct);
}
