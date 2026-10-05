"""Factory Method: define an interface for creating an object, but let subclasses decide which class to instantiate."""

from abc import ABC, abstractmethod


class Transport(ABC):
    @abstractmethod
    def deliver(self, cargo: str) -> str: ...


class Truck(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Truck delivers {cargo} by road"


class Ship(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Ship delivers {cargo} by sea"


class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> Transport:
        """The factory method."""

    def plan_delivery(self, cargo: str) -> str:
        return self.create_transport().deliver(cargo)


class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()


def main() -> None:
    for logistics in (RoadLogistics(), SeaLogistics()):
        print(logistics.plan_delivery("10 boxes"))


if __name__ == "__main__":
    main()
