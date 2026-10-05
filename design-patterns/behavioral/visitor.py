"""Visitor: add new operations to an object structure without modifying the classes of its elements."""

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def accept(self, visitor: "ShapeVisitor"): ...


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def accept(self, visitor: "ShapeVisitor"):
        return visitor.visit_circle(self)


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width, self.height = width, height

    def accept(self, visitor: "ShapeVisitor"):
        return visitor.visit_rectangle(self)


class ShapeVisitor(ABC):
    @abstractmethod
    def visit_circle(self, circle: Circle): ...

    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle): ...


class AreaVisitor(ShapeVisitor):
    def visit_circle(self, circle: Circle) -> float:
        return math.pi * circle.radius**2

    def visit_rectangle(self, rectangle: Rectangle) -> float:
        return rectangle.width * rectangle.height


class JsonExportVisitor(ShapeVisitor):
    def visit_circle(self, circle: Circle) -> str:
        return f'{{"type": "circle", "radius": {circle.radius}}}'

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        return f'{{"type": "rectangle", "width": {rectangle.width}, "height": {rectangle.height}}}'


def main() -> None:
    shapes: list[Shape] = [Circle(1), Rectangle(3, 4)]
    for shape in shapes:
        print(f"{shape.accept(JsonExportVisitor())}  area={shape.accept(AreaVisitor()):.2f}")


if __name__ == "__main__":
    main()
