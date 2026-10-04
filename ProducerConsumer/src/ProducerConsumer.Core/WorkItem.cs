using System.Text.Json;

namespace ProducerConsumer.Core;

public sealed record WorkItem(string Id, int Sequence, string Payload, DateTimeOffset CreatedAt);

public static class Json
{
    public static readonly JsonSerializerOptions Options = new(JsonSerializerDefaults.Web)
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
    };
}
