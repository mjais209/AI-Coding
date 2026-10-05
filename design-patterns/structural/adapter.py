"""Adapter: convert the interface of a class into another interface clients expect."""

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Target interface our checkout code expects."""

    @abstractmethod
    def pay(self, amount: float) -> str: ...


class LegacyPayGateway:
    """Third-party class with an incompatible interface (amounts in cents)."""

    def make_payment(self, cents: int, currency: str) -> str:
        return f"LegacyPay charged {cents} {currency} cents"


class LegacyPayAdapter(PaymentProcessor):
    def __init__(self, gateway: LegacyPayGateway) -> None:
        self._gateway = gateway

    def pay(self, amount: float) -> str:
        return self._gateway.make_payment(round(amount * 100), "USD")


def checkout(processor: PaymentProcessor, amount: float) -> str:
    return processor.pay(amount)


def main() -> None:
    print(checkout(LegacyPayAdapter(LegacyPayGateway()), 19.99))


if __name__ == "__main__":
    main()
