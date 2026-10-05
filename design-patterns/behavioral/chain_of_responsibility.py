"""Chain of Responsibility: pass a request along a chain of handlers until one handles it."""

from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self) -> None:
        self._next: Handler | None = None

    def set_next(self, handler: "Handler") -> "Handler":
        self._next = handler
        return handler

    def handle(self, amount: float) -> str:
        if self.can_approve(amount):
            return f"{type(self).__name__} approved ${amount:,.0f}"
        if self._next:
            return self._next.handle(amount)
        return f"Nobody can approve ${amount:,.0f}"

    @abstractmethod
    def can_approve(self, amount: float) -> bool: ...


class TeamLead(Handler):
    def can_approve(self, amount: float) -> bool:
        return amount <= 1_000


class Manager(Handler):
    def can_approve(self, amount: float) -> bool:
        return amount <= 10_000


class Director(Handler):
    def can_approve(self, amount: float) -> bool:
        return amount <= 100_000


def build_chain() -> Handler:
    lead = TeamLead()
    lead.set_next(Manager()).set_next(Director())
    return lead


def main() -> None:
    chain = build_chain()
    for amount in (500, 5_000, 50_000, 500_000):
        print(chain.handle(amount))


if __name__ == "__main__":
    main()
