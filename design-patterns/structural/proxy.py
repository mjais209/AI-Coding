"""Proxy: provide a surrogate that controls access to another object (lazy loading, caching, access control)."""

from abc import ABC, abstractmethod


class Image(ABC):
    @abstractmethod
    def display(self) -> str: ...


class RealImage(Image):
    load_count = 0

    def __init__(self, filename: str) -> None:
        self.filename = filename
        RealImage.load_count += 1  # expensive load from disk

    def display(self) -> str:
        return f"Displaying {self.filename}"


class ImageProxy(Image):
    """Virtual + protection proxy: loads lazily and only for authorized users."""

    def __init__(self, filename: str, user_role: str = "viewer") -> None:
        self.filename = filename
        self.user_role = user_role
        self._real: RealImage | None = None

    def display(self) -> str:
        if self.user_role not in ("viewer", "admin"):
            return f"Access denied to {self.filename}"
        if self._real is None:
            self._real = RealImage(self.filename)
        return self._real.display()


def main() -> None:
    image = ImageProxy("photo.png")
    print(f"Loads before display: {RealImage.load_count}")
    print(image.display())
    print(image.display())
    print(f"Loads after two displays: {RealImage.load_count}")
    print(ImageProxy("secret.png", user_role="guest").display())


if __name__ == "__main__":
    main()
