using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using Orders.Core;

namespace Orders.Tests;

/// <summary>
/// End-to-end tests against Azurite (or a real account via Storage__ConnectionString).
/// Each run uses uniquely named queues, container and table, deleted afterwards.
/// </summary>
[Trait("Category", "Integration")]
public sealed class IntegrationTests : IAsyncLifetime
{
    private readonly WebApplicationFactory<Program> _factory;
    private HttpClient _client = null!;

    public IntegrationTests()
    {
        var suffix = Guid.NewGuid().ToString("N")[..8];
        _factory = new WebApplicationFactory<Program>().WithWebHostBuilder(b =>
        {
            b.UseSetting("Storage:QueueName", $"orders-{suffix}");
            b.UseSetting("Storage:PoisonQueueName", $"orders-poison-{suffix}");
            b.UseSetting("Storage:ReceiptsContainer", $"receipts-{suffix}");
            b.UseSetting("Storage:OrdersTable", $"orders{suffix}");
            b.UseSetting("Storage:MaxDequeueCount", "1");
            b.UseSetting("Storage:VisibilityTimeoutSeconds", "1");
        });
    }

    private OrderStorage Storage => _factory.Services.GetRequiredService<OrderStorage>();
    private OrderProcessor Processor => _factory.Services.GetRequiredService<OrderProcessor>();

    public Task InitializeAsync()
    {
        _client = _factory.CreateClient();
        return Task.CompletedTask;
    }

    public async Task DisposeAsync()
    {
        await Storage.Queue.DeleteIfExistsAsync();
        await Storage.PoisonQueue.DeleteIfExistsAsync();
        await Storage.Receipts.DeleteIfExistsAsync();
        await Storage.Orders.DeleteAsync();
        await _factory.DisposeAsync();
    }

    [Fact]
    public async Task Order_FlowsThroughQueue_ToBlobAndTableStorage()
    {
        var response = await _client.PostAsJsonAsync("/api/orders", new
        {
            customer = "Ada",
            items = new[] { new { sku = "A", quantity = 3, unit_price = 2.5 } },
        });
        Assert.Equal(HttpStatusCode.Accepted, response.StatusCode);
        var orderId = (await response.Content.ReadFromJsonAsync<JsonElement>()).GetProperty("id").GetString();

        Assert.Equal("queued", (await GetJson($"/api/orders/{orderId}")).GetProperty("status").GetString());
        Assert.Equal(HttpStatusCode.NotFound, (await _client.GetAsync($"/api/orders/{orderId}/receipt")).StatusCode);
        Assert.Equal(1, (await GetJson("/api/health")).GetProperty("queue_depth").GetInt32());

        Assert.Equal(1, await Processor.ProcessBatchAsync());

        var order = await GetJson($"/api/orders/{orderId}");
        Assert.Equal("processed", order.GetProperty("status").GetString());
        Assert.Equal(8.1, order.GetProperty("total").GetDouble());
        var receipt = await GetJson($"/api/orders/{orderId}/receipt");
        Assert.Equal(orderId, receipt.GetProperty("order_id").GetString());
        Assert.Equal(8.1m, receipt.GetProperty("total").GetDecimal());
        var orders = await GetJson("/api/orders");
        Assert.Contains(orders.EnumerateArray(), o => o.GetProperty("id").GetString() == orderId);
    }

    [Fact]
    public async Task InvalidOrder_IsRejected()
    {
        var response = await _client.PostAsJsonAsync("/api/orders", new { customer = "Ada", items = Array.Empty<object>() });
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }

    [Fact]
    public async Task PoisonMessage_IsMovedToPoisonQueue()
    {
        _ = _client; // ensure host (and storage resources) are initialized
        var orderId = Guid.NewGuid().ToString();
        await Storage.UpsertOrderAsync(orderId, new Dictionary<string, object?> { ["Status"] = OrderStatus.Queued });
        await Storage.Queue.SendMessageAsync(JsonSerializer.Serialize(new { id = orderId, customer = "Bad" }));

        Assert.Equal(1, await Processor.ProcessBatchAsync()); // fails: no items, stays on queue
        await Task.Delay(TimeSpan.FromSeconds(1.5));          // wait for visibility timeout
        Assert.Equal(1, await Processor.ProcessBatchAsync()); // exceeds MaxDequeueCount -> poison queue

        var poisoned = (await Storage.PoisonQueue.ReceiveMessagesAsync(32)).Value;
        Assert.Contains(poisoned, m => m.MessageText.Contains(orderId));
        Assert.Equal("failed", (await Storage.GetOrderAsync(orderId))!.Status);
    }

    private async Task<JsonElement> GetJson(string url) =>
        await _client.GetFromJsonAsync<JsonElement>(url);
}
