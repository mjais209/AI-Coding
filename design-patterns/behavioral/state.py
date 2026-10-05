"""State: let an object alter its behavior when its internal state changes; it appears to change its class."""

from abc import ABC, abstractmethod


class OrderState(ABC):
    @abstractmethod
    def next(self, order: "Order") -> None: ...

    def cancel(self, order: "Order") -> None:
        order.state = Cancelled()

    def __str__(self) -> str:
        return type(self).__name__


class Pending(OrderState):
    def next(self, order: "Order") -> None:
        order.state = Paid()


class Paid(OrderState):
    def next(self, order: "Order") -> None:
        order.state = Shipped()


class Shipped(OrderState):
    def next(self, order: "Order") -> None:
        order.state = Delivered()

    def cancel(self, order: "Order") -> None:
        raise RuntimeError("Cannot cancel an order that has shipped")


class Delivered(OrderState):
    def next(self, order: "Order") -> None:
        raise RuntimeError("Order already delivered")

    def cancel(self, order: "Order") -> None:
        raise RuntimeError("Cannot cancel a delivered order")


class Cancelled(OrderState):
    def next(self, order: "Order") -> None:
        raise RuntimeError("Order was cancelled")

    def cancel(self, order: "Order") -> None:
        pass


class Order:
    def __init__(self) -> None:
        self.state: OrderState = Pending()

    def next(self) -> None:
        self.state.next(self)

    def cancel(self) -> None:
        self.state.cancel(self)


def main() -> None:
    order = Order()
    print(f"Start: {order.state}")
    for _ in range(3):
        order.next()
        print(f"Next:  {order.state}")
    try:
        order.cancel()
    except RuntimeError as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
