"""Observer: define a one-to-many dependency so that when one object changes state, all dependents are notified."""

from collections.abc import Callable

Listener = Callable[[str, float], None]


class Stock:
    """Subject / publisher."""

    def __init__(self, symbol: str, price: float) -> None:
        self.symbol = symbol
        self._price = price
        self._observers: list[Listener] = []

    def subscribe(self, observer: Listener) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: Listener) -> None:
        self._observers.remove(observer)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        self._price = value
        for observer in list(self._observers):
            observer(self.symbol, value)


class PriceAlert:
    def __init__(self, threshold: float) -> None:
        self.threshold = threshold
        self.alerts: list[str] = []

    def __call__(self, symbol: str, price: float) -> None:
        if price > self.threshold:
            self.alerts.append(f"ALERT: {symbol} above {self.threshold}: {price}")


def main() -> None:
    stock = Stock("ACME", 100.0)
    alert = PriceAlert(threshold=120)
    stock.subscribe(lambda s, p: print(f"[logger] {s} -> {p}"))
    stock.subscribe(alert)
    for price in (110, 125, 130):
        stock.price = price
    print("\n".join(alert.alerts))


if __name__ == "__main__":
    main()
