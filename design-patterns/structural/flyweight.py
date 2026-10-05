"""Flyweight: share common (intrinsic) state between many objects to save memory."""

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class TreeType:
    """Intrinsic, shared state."""

    name: str
    color: str
    texture: str


class TreeTypeFactory:
    _cache: ClassVar[dict[tuple[str, str, str], TreeType]] = {}

    @classmethod
    def get(cls, name: str, color: str, texture: str) -> TreeType:
        key = (name, color, texture)
        if key not in cls._cache:
            cls._cache[key] = TreeType(name, color, texture)
        return cls._cache[key]

    @classmethod
    def count(cls) -> int:
        return len(cls._cache)


@dataclass
class Tree:
    """Extrinsic, per-object state plus a reference to the shared flyweight."""

    x: int
    y: int
    type: TreeType


class Forest:
    def __init__(self) -> None:
        self.trees: list[Tree] = []

    def plant(self, x: int, y: int, name: str, color: str, texture: str) -> None:
        self.trees.append(Tree(x, y, TreeTypeFactory.get(name, color, texture)))


def main() -> None:
    forest = Forest()
    for i in range(1000):
        if i % 2:
            forest.plant(i, i * 2, "Oak", "green", "rough")
        else:
            forest.plant(i, i * 3, "Pine", "dark-green", "needles")
    print(f"Trees planted: {len(forest.trees)}, shared TreeType objects: {TreeTypeFactory.count()}")


if __name__ == "__main__":
    main()
