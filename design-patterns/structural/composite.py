"""Composite: compose objects into tree structures and treat individual objects and compositions uniformly."""

from abc import ABC, abstractmethod


class FileSystemNode(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def display(self, indent: int = 0) -> str: ...


class File(FileSystemNode):
    def __init__(self, name: str, size: int) -> None:
        super().__init__(name)
        self._size = size

    def size(self) -> int:
        return self._size

    def display(self, indent: int = 0) -> str:
        return f"{'  ' * indent}{self.name} ({self._size} B)"


class Folder(FileSystemNode):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.children: list[FileSystemNode] = []

    def add(self, node: FileSystemNode) -> "Folder":
        self.children.append(node)
        return self

    def size(self) -> int:
        return sum(child.size() for child in self.children)

    def display(self, indent: int = 0) -> str:
        lines = [f"{'  ' * indent}{self.name}/ ({self.size()} B)"]
        lines += [child.display(indent + 1) for child in self.children]
        return "\n".join(lines)


def main() -> None:
    root = (
        Folder("project")
        .add(File("README.md", 120))
        .add(Folder("src").add(File("main.py", 800)).add(File("utils.py", 300)))
    )
    print(root.display())


if __name__ == "__main__":
    main()
