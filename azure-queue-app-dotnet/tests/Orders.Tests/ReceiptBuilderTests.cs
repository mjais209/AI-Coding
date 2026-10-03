using Orders.Core;

namespace Orders.Tests;

public class ReceiptBuilderTests
{
    [Fact]
    public void Build_ComputesLineTotalsSubtotalTaxAndTotal()
    {
        var order = new OrderMessage("abc", "Ada",
        [
            new OrderItem("A", 2, 10.0m),
            new OrderItem("B", 1, 5.5m),
        ]);

        var receipt = ReceiptBuilder.Build(order);

        Assert.Equal([20.0m, 5.5m], receipt.Lines.Select(l => l.LineTotal));
        Assert.Equal(25.5m, receipt.Subtotal);
        Assert.Equal(2.04m, receipt.Tax);
        Assert.Equal(27.54m, receipt.Total);
    }

    [Fact]
    public void Validate_RejectsEmptyOrderAndBadItems()
    {
        Assert.Contains("items", OrderValidator.Validate(new OrderRequest("Ada", [])).Keys);
        var errors = OrderValidator.Validate(new OrderRequest("", [new OrderItem("", 0, -1m)]));
        string[] expected = ["customer", "items[0].quantity", "items[0].sku", "items[0].unit_price"];
        Assert.Equal(expected, errors.Keys.Order());
        Assert.Empty(OrderValidator.Validate(new OrderRequest("Ada", [new OrderItem("A", 1, 1m)])));
    }
}
