using System.Text.Json;

namespace Orders.Core;

public sealed record OrderItem(string Sku, int Quantity, decimal UnitPrice);

public sealed record OrderRequest(string Customer, List<OrderItem> Items);

public sealed record OrderMessage(string Id, string Customer, List<OrderItem> Items);

public sealed record ReceiptLine(string Sku, int Quantity, decimal UnitPrice, decimal LineTotal);

public sealed record Receipt(
    string OrderId,
    string Customer,
    List<ReceiptLine> Lines,
    decimal Subtotal,
    decimal Tax,
    decimal Total,
    DateTimeOffset ProcessedAt);

public sealed record OrderRecord(
    string Id,
    string? Customer,
    string? Status,
    DateTimeOffset? CreatedAt,
    DateTimeOffset? UpdatedAt,
    List<OrderItem>? Items,
    double? Total,
    string? ReceiptBlob,
    string? Error);

public static class OrderStatus
{
    public const string Queued = "queued";
    public const string Processing = "processing";
    public const string Processed = "processed";
    public const string Failed = "failed";
}

public static class Json
{
    public static readonly JsonSerializerOptions Options = new(JsonSerializerDefaults.Web)
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
    };
}
