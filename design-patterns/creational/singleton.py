"""Singleton: ensure a class has only one instance and provide a global access point to it."""

import threading
from typing import ClassVar


class SingletonMeta(type):
    _instances: ClassVar[dict] = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AppConfig(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.settings: dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        self.settings[key] = value

    def get(self, key: str) -> str | None:
        return self.settings.get(key)


def main() -> None:
    a = AppConfig()
    b = AppConfig()
    a.set("env", "production")
    print(f"Same instance: {a is b}")
    print(f"b sees value set via a: env={b.get('env')}")


if __name__ == "__main__":
    main()
