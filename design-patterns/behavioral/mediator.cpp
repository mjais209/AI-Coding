// Mediator: define an object that encapsulates how a set of objects interact, reducing direct coupling.
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "check.h"

class ChatRoom;

class User {
public:
    explicit User(std::string name) : name_(std::move(name)) {}
    const std::string& name() const { return name_; }
    void join(ChatRoom& room);
    void send(const std::string& message, const std::string& to = "");
    void receive(const std::string& from, const std::string& message) { inbox.push_back(from + ": " + message); }

    std::vector<std::string> inbox;

private:
    std::string name_;
    ChatRoom* room_ = nullptr;
};

// Users talk only to the mediator, never directly to each other.
class ChatRoom {
public:
    void join(User& user) { users_[user.name()] = &user; }
    void send(const std::string& from, const std::string& message, const std::string& to) {
        if (!to.empty()) {
            users_.at(to)->receive(from, message);
            return;
        }
        for (auto& [name, user] : users_)
            if (name != from) user->receive(from, message);
    }

private:
    std::map<std::string, User*> users_;
};

void User::join(ChatRoom& room) {
    room_ = &room;
    room.join(*this);
}

void User::send(const std::string& message, const std::string& to) { room_->send(name_, message, to); }

int main() {
    ChatRoom room;
    User alice("Alice"), bob("Bob"), carol("Carol");
    for (User* u : {&alice, &bob, &carol}) u->join(room);

    alice.send("Hi everyone!");
    bob.send("Hey Alice, private hello", "Alice");

    for (User* u : {&alice, &bob, &carol}) {
        std::cout << u->name() << " inbox:";
        for (const auto& m : u->inbox) std::cout << " [" << m << "]";
        std::cout << "\n";
    }

    CHECK(alice.inbox == std::vector<std::string>{"Bob: Hey Alice, private hello"});
    CHECK(bob.inbox == std::vector<std::string>{"Alice: Hi everyone!"});
    CHECK(carol.inbox == std::vector<std::string>{"Alice: Hi everyone!"});
}
