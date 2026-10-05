"""Facade: provide a simple, unified interface to a complex subsystem."""


class Inventory:
    def reserve(self, sku: str) -> str:
        return f"reserved {sku}"


class Payment:
    def charge(self, amount: float) -> str:
        return f"charged ${amount:.2f}"


class Shipping:
    def schedule(self, address: str) -> str:
        return f"shipping to {address}"


class Notification:
    def email(self, to: str) -> str:
        return f"emailed {to}"


class OrderFacade:
    def __init__(self) -> None:
        self.inventory = Inventory()
        self.payment = Payment()
        self.shipping = Shipping()
        self.notification = Notification()

    def place_order(self, sku: str, amount: float, address: str, email: str) -> list[str]:
        return [
            self.inventory.reserve(sku),
            self.payment.charge(amount),
            self.shipping.schedule(address),
            self.notification.email(email),
        ]


def main() -> None:
    for step in OrderFacade().place_order("SKU-42", 49.90, "221B Baker St", "alice@example.com"):
        print(step)


if __name__ == "__main__":
    main()
