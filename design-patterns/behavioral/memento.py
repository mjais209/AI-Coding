"""Memento: capture and restore an object's internal state without violating encapsulation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EditorMemento:
    content: str
    cursor: int


class Editor:
    """Originator."""

    def __init__(self) -> None:
        self._content = ""
        self._cursor = 0

    def type(self, text: str) -> None:
        self._content = self._content[: self._cursor] + text + self._content[self._cursor :]
        self._cursor += len(text)

    def save(self) -> EditorMemento:
        return EditorMemento(self._content, self._cursor)

    def restore(self, memento: EditorMemento) -> None:
        self._content, self._cursor = memento.content, memento.cursor

    @property
    def content(self) -> str:
        return self._content


class History:
    """Caretaker: stores mementos but never inspects them."""

    def __init__(self) -> None:
        self._snapshots: list[EditorMemento] = []

    def push(self, memento: EditorMemento) -> None:
        self._snapshots.append(memento)

    def pop(self) -> EditorMemento:
        return self._snapshots.pop()


def main() -> None:
    editor, history = Editor(), History()
    editor.type("Design ")
    history.push(editor.save())
    editor.type("patterns ")
    history.push(editor.save())
    editor.type("are tricky!!!")
    print(f"Current:  {editor.content!r}")
    editor.restore(history.pop())
    print(f"Restored: {editor.content!r}")
    editor.restore(history.pop())
    print(f"Restored: {editor.content!r}")


if __name__ == "__main__":
    main()
