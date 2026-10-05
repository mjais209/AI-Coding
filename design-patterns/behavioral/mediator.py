"""Mediator: define an object that encapsulates how a set of objects interact, reducing direct coupling."""


class ChatRoom:
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def join(self, user: "User") -> None:
        self._users[user.name] = user
        user.room = self

    def send(self, sender: str, message: str, to: str | None = None) -> None:
        recipients = [self._users[to]] if to else [u for n, u in self._users.items() if n != sender]
        for user in recipients:
            user.receive(sender, message)


class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.room: ChatRoom | None = None
        self.inbox: list[str] = []

    def send(self, message: str, to: str | None = None) -> None:
        assert self.room, "join a room first"
        self.room.send(self.name, message, to)

    def receive(self, sender: str, message: str) -> None:
        self.inbox.append(f"{sender}: {message}")


def main() -> None:
    room = ChatRoom()
    alice, bob, carol = User("Alice"), User("Bob"), User("Carol")
    for user in (alice, bob, carol):
        room.join(user)
    alice.send("Hi everyone!")
    bob.send("Hey Alice, private hello", to="Alice")
    for user in (alice, bob, carol):
        print(f"{user.name} inbox: {user.inbox}")


if __name__ == "__main__":
    main()
