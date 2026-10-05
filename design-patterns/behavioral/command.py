"""Command: encapsulate a request as an object, enabling queuing, logging and undo."""

from abc import ABC, abstractmethod


class TextEditor:
    def __init__(self) -> None:
        self.text = ""


class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


class AppendText(Command):
    def __init__(self, editor: TextEditor, text: str) -> None:
        self.editor = editor
        self.text = text

    def execute(self) -> None:
        self.editor.text += self.text

    def undo(self) -> None:
        self.editor.text = self.editor.text[: -len(self.text)]


class ClearText(Command):
    def __init__(self, editor: TextEditor) -> None:
        self.editor = editor
        self._backup = ""

    def execute(self) -> None:
        self._backup = self.editor.text
        self.editor.text = ""

    def undo(self) -> None:
        self.editor.text = self._backup


class CommandInvoker:
    def __init__(self) -> None:
        self._history: list[Command] = []

    def run(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo(self) -> None:
        if self._history:
            self._history.pop().undo()


def main() -> None:
    editor, invoker = TextEditor(), CommandInvoker()
    invoker.run(AppendText(editor, "Hello"))
    invoker.run(AppendText(editor, ", World"))
    print(f"After appends: {editor.text!r}")
    invoker.run(ClearText(editor))
    print(f"After clear:   {editor.text!r}")
    invoker.undo()
    print(f"Undo clear:    {editor.text!r}")
    invoker.undo()
    print(f"Undo append:   {editor.text!r}")


if __name__ == "__main__":
    main()
