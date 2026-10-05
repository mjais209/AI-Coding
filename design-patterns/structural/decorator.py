"""Decorator: attach additional responsibilities to an object dynamically by wrapping it."""

from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float: ...

    @abstractmethod
    def description(self) -> str: ...


class Espresso(Coffee):
    def cost(self) -> float:
        return 2.00

    def description(self) -> str:
        return "Espresso"


class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee) -> None:
        self._coffee = coffee


class Milk(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.50

    def description(self) -> str:
        return self._coffee.description() + " + milk"


class Caramel(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.75

    def description(self) -> str:
        return self._coffee.description() + " + caramel"


def main() -> None:
    order = Caramel(Milk(Milk(Espresso())))
    print(f"{order.description()}: ${order.cost():.2f}")


if __name__ == "__main__":
    main()
