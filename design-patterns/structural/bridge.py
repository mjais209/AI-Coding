"""Bridge: decouple an abstraction from its implementation so the two can vary independently."""

from abc import ABC, abstractmethod


class Device(ABC):
    """Implementation side."""

    def __init__(self) -> None:
        self.on = False
        self.volume = 10

    @abstractmethod
    def name(self) -> str: ...


class TV(Device):
    def name(self) -> str:
        return "TV"


class Radio(Device):
    def name(self) -> str:
        return "Radio"


class Remote:
    """Abstraction side; holds a reference to a Device."""

    def __init__(self, device: Device) -> None:
        self.device = device

    def toggle_power(self) -> str:
        self.device.on = not self.device.on
        return f"{self.device.name()} power {'on' if self.device.on else 'off'}"

    def volume_up(self) -> str:
        self.device.volume = min(100, self.device.volume + 10)
        return f"{self.device.name()} volume {self.device.volume}"


class AdvancedRemote(Remote):
    def mute(self) -> str:
        self.device.volume = 0
        return f"{self.device.name()} muted"


def main() -> None:
    for remote in (Remote(TV()), AdvancedRemote(Radio())):
        print(remote.toggle_power())
        print(remote.volume_up())
        if isinstance(remote, AdvancedRemote):
            print(remote.mute())


if __name__ == "__main__":
    main()
