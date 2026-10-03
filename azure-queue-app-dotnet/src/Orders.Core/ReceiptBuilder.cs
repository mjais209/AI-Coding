namespace Orders.Core;

public static class ReceiptBuilder
{
    public const decimal TaxRate = 0.08m;

    public static Receipt Build(OrderMessage order, TimeProvider? clock = null)
    {
        var lines = order.Items
            .Select(i => new ReceiptLine(i.Sku, i.Quantity, i.UnitPrice, Round(i.Quantity * i.UnitPrice)))
            .ToList();
        var subtotal = Round(lines.Sum(l => l.LineTotal));
        var tax = Round(subtotal * TaxRate);
        return new Receipt(
            order.Id,
            order.Customer,
            lines,
            subtotal,
            tax,
            subtotal + tax,
            (clock ?? TimeProvider.System).GetUtcNow());
    }

    private static decimal Round(decimal value) => Math.Round(value, 2, MidpointRounding.AwayFromZero);
}
