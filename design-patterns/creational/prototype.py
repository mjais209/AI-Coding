"""Prototype: create new objects by cloning an existing instance instead of building from scratch."""

import copy
from dataclasses import dataclass, field


@dataclass
class Document:
    title: str
    body: str
    tags: list[str] = field(default_factory=list)

    def clone(self, **overrides) -> "Document":
        cloned = copy.deepcopy(self)
        for key, value in overrides.items():
            setattr(cloned, key, value)
        return cloned


class PrototypeRegistry:
    def __init__(self) -> None:
        self._prototypes: dict[str, Document] = {}

    def register(self, name: str, prototype: Document) -> None:
        self._prototypes[name] = prototype

    def create(self, name: str, **overrides) -> Document:
        return self._prototypes[name].clone(**overrides)


def main() -> None:
    registry = PrototypeRegistry()
    registry.register("invoice", Document("Invoice", "Amount due: ...", ["finance"]))

    jan = registry.create("invoice", title="Invoice - January")
    jan.tags.append("january")
    feb = registry.create("invoice", title="Invoice - February")

    print(jan)
    print(feb)
    print(f"Prototype untouched: {registry.create('invoice')}")


if __name__ == "__main__":
    main()
