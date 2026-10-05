"""Strategy: define a family of interchangeable algorithms and select one at runtime."""

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float: ...


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float) -> None:
        self.percent = percent

    def apply(self, total: float) -> float:
        return total * (1 - self.percent / 100)


class FlatDiscount(DiscountStrategy):
    def __init__(self, amount: float) -> None:
        self.amount = amount

    def apply(self, total: float) -> float:
        return max(0.0, total - self.amount)


class ShoppingCart:
    def __init__(self, strategy: DiscountStrategy | None = None) -> None:
        self.items: list[float] = []
        self.strategy = strategy or NoDiscount()

    def add(self, price: float) -> None:
        self.items.append(price)

    def total(self) -> float:
        return round(self.strategy.apply(sum(self.items)), 2)


def main() -> None:
    cart = ShoppingCart()
    for price in (40.0, 60.0):
        cart.add(price)
    for strategy in (NoDiscount(), PercentageDiscount(15), FlatDiscount(25)):
        cart.strategy = strategy
        print(f"{type(strategy).__name__:<20} total = ${cart.total():.2f}")


if __name__ == "__main__":
    main()
