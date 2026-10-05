"""Builder: construct a complex object step by step; the same process can create different representations."""

from dataclasses import dataclass, field


@dataclass
class Pizza:
    size: str = "medium"
    crust: str = "regular"
    toppings: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        toppings = ", ".join(self.toppings) or "no toppings"
        return f"{self.size} pizza, {self.crust} crust, {toppings}"


class PizzaBuilder:
    def __init__(self) -> None:
        self._pizza = Pizza()

    def size(self, size: str) -> "PizzaBuilder":
        self._pizza.size = size
        return self

    def crust(self, crust: str) -> "PizzaBuilder":
        self._pizza.crust = crust
        return self

    def topping(self, topping: str) -> "PizzaBuilder":
        self._pizza.toppings.append(topping)
        return self

    def build(self) -> Pizza:
        pizza, self._pizza = self._pizza, Pizza()
        return pizza


class PizzaDirector:
    """Optional director that knows recipes built from builder steps."""

    @staticmethod
    def margherita(builder: PizzaBuilder) -> Pizza:
        return builder.size("medium").crust("thin").topping("tomato").topping("mozzarella").topping("basil").build()


def main() -> None:
    builder = PizzaBuilder()
    print(builder.size("large").crust("stuffed").topping("pepperoni").topping("olives").build())
    print(PizzaDirector.margherita(builder))


if __name__ == "__main__":
    main()
