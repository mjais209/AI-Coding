using System.Text.Json;
using Orders.Core;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOrderStorage(builder.Configuration);
builder.Services.ConfigureHttpJsonOptions(o =>
    o.SerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower);

var app = builder.Build();

await app.Services.GetRequiredService<OrderStorage>().EnsureResourcesAsync();

app.UseDefaultFiles();
app.UseStaticFiles();

var api = app.MapGroup("/api");

api.MapPost("/orders", async (OrderRequest order, OrderStorage storage, CancellationToken ct) =>
{
    var errors = OrderValidator.Validate(order);
    if (errors.Count > 0)
        return Results.ValidationProblem(errors);

    var message = new OrderMessage(Guid.NewGuid().ToString(), order.Customer.Trim(), order.Items);
    await storage.UpsertOrderAsync(message.Id, new Dictionary<string, object?>
    {
        ["Customer"] = message.Customer,
        ["Status"] = OrderStatus.Queued,
        ["CreatedAt"] = DateTimeOffset.UtcNow,
        ["Items"] = JsonSerializer.Serialize(message.Items, Json.Options),
    }, ct);
    await storage.EnqueueAsync(message, ct);
    return Results.Accepted($"/api/orders/{message.Id}", new { id = message.Id, status = OrderStatus.Queued });
});

api.MapGet("/orders", (OrderStorage storage, CancellationToken ct) => storage.ListOrdersAsync(ct: ct));

api.MapGet("/orders/{id}", async (string id, OrderStorage storage, CancellationToken ct) =>
    await storage.GetOrderAsync(id, ct) is { } order
        ? Results.Ok(order)
        : Results.NotFound(new { detail = "Order not found" }));

api.MapGet("/orders/{id}/receipt", async (string id, OrderStorage storage, CancellationToken ct) =>
    await storage.GetReceiptAsync(id, ct) is { } receipt
        ? Results.Ok(receipt)
        : Results.NotFound(new { detail = "Receipt not available yet" }));

api.MapGet("/health", async (OrderStorage storage, CancellationToken ct) =>
    new { status = "ok", queue_depth = await storage.GetQueueDepthAsync(ct) });

app.Run();

public partial class Program;
