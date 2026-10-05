"""Interpreter: define a grammar and an interpreter that evaluates sentences in that language.

Grammar (prefix/Polish notation):  expr := number | variable | (+|-|*) expr expr
"""

from abc import ABC, abstractmethod
from typing import ClassVar


class Expression(ABC):
    @abstractmethod
    def interpret(self, context: dict[str, int]) -> int: ...


class Number(Expression):
    def __init__(self, value: int) -> None:
        self.value = value

    def interpret(self, context: dict[str, int]) -> int:
        return self.value


class Variable(Expression):
    def __init__(self, name: str) -> None:
        self.name = name

    def interpret(self, context: dict[str, int]) -> int:
        return context[self.name]


class BinaryOp(Expression):
    OPS: ClassVar[dict] = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}

    def __init__(self, op: str, left: Expression, right: Expression) -> None:
        self.op, self.left, self.right = op, left, right

    def interpret(self, context: dict[str, int]) -> int:
        return self.OPS[self.op](self.left.interpret(context), self.right.interpret(context))


def parse(source: str) -> Expression:
    tokens = source.split()

    def parse_next() -> Expression:
        token = tokens.pop(0)
        if token in BinaryOp.OPS:
            return BinaryOp(token, parse_next(), parse_next())
        if token.lstrip("-").isdigit():
            return Number(int(token))
        return Variable(token)

    expr = parse_next()
    if tokens:
        raise ValueError(f"Unexpected tokens: {tokens}")
    return expr


def main() -> None:
    source = "+ * x 2 - y 3"  # (x * 2) + (y - 3)
    context = {"x": 5, "y": 10}
    print(f"{source}  with {context}  =  {parse(source).interpret(context)}")


if __name__ == "__main__":
    main()
