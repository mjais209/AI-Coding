"""Abstract Factory: create families of related objects without specifying their concrete classes."""

from abc import ABC, abstractmethod


class Button(ABC):
    @abstractmethod
    def render(self) -> str: ...


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str: ...


class LightButton(Button):
    def render(self) -> str:
        return "[Light Button]"


class LightCheckbox(Checkbox):
    def render(self) -> str:
        return "[Light Checkbox]"


class DarkButton(Button):
    def render(self) -> str:
        return "[Dark Button]"


class DarkCheckbox(Checkbox):
    def render(self) -> str:
        return "[Dark Checkbox]"


class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox: ...


class LightThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return LightButton()

    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()


class DarkThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return DarkButton()

    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()


def render_form(factory: UIFactory) -> str:
    return f"{factory.create_button().render()} {factory.create_checkbox().render()}"


def main() -> None:
    for factory in (LightThemeFactory(), DarkThemeFactory()):
        print(f"{type(factory).__name__}: {render_form(factory)}")


if __name__ == "__main__":
    main()
