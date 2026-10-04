namespace Orders.Core;

public static class OrderValidator
{
    public static Dictionary<string, string[]> Validate(OrderRequest? order)
    {
        var errors = new Dictionary<string, string[]>();
        if (order is null)
        {
            errors["body"] = ["Request body is required."];
            return errors;
        }
        if (string.IsNullOrWhiteSpace(order.Customer))
            errors["customer"] = ["Customer is required."];
        if (order.Items is null || order.Items.Count == 0)
        {
            errors["items"] = ["At least one item is required."];
            return errors;
        }
        for (var i = 0; i < order.Items.Count; i++)
        {
            var item = order.Items[i];
            if (item is null)
            {
                errors[$"items[{i}]"] = ["Item is required."];
                continue;
            }
            if (string.IsNullOrWhiteSpace(item.Sku))
                errors[$"items[{i}].sku"] = ["SKU is required."];
            if (item.Quantity <= 0)
                errors[$"items[{i}].quantity"] = ["Quantity must be greater than 0."];
            if (item.UnitPrice < 0)
                errors[$"items[{i}].unit_price"] = ["Unit price cannot be negative."];
        }
        return errors;
    }
}
