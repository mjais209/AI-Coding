// State: let an object alter its behavior when its internal state changes; it appears to change its class.
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

#include "check.h"

class Order;

class OrderState {
public:
    virtual ~OrderState() = default;
    virtual std::unique_ptr<OrderState> next() const = 0;
    virtual std::unique_ptr<OrderState> cancel() const;
    virtual std::string name() const = 0;
};

class Cancelled : public OrderState {
public:
    std::unique_ptr<OrderState> next() const override { throw std::runtime_error("Order was cancelled"); }
    std::unique_ptr<OrderState> cancel() const override { return std::make_unique<Cancelled>(); }
    std::string name() const override { return "Cancelled"; }
};

std::unique_ptr<OrderState> OrderState::cancel() const { return std::make_unique<Cancelled>(); }

class Delivered : public OrderState {
public:
    std::unique_ptr<OrderState> next() const override { throw std::runtime_error("Order already delivered"); }
    std::unique_ptr<OrderState> cancel() const override { throw std::runtime_error("Cannot cancel a delivered order"); }
    std::string name() const override { return "Delivered"; }
};

class Shipped : public OrderState {
public:
    std::unique_ptr<OrderState> next() const override { return std::make_unique<Delivered>(); }
    std::unique_ptr<OrderState> cancel() const override { throw std::runtime_error("Cannot cancel a shipped order"); }
    std::string name() const override { return "Shipped"; }
};

class Paid : public OrderState {
public:
    std::unique_ptr<OrderState> next() const override { return std::make_unique<Shipped>(); }
    std::string name() const override { return "Paid"; }
};

class Pending : public OrderState {
public:
    std::unique_ptr<OrderState> next() const override { return std::make_unique<Paid>(); }
    std::string name() const override { return "Pending"; }
};

// Context: delegates behavior to its current state object.
class Order {
public:
    void next() { state_ = state_->next(); }
    void cancel() { state_ = state_->cancel(); }
    std::string status() const { return state_->name(); }

private:
    std::unique_ptr<OrderState> state_ = std::make_unique<Pending>();
};

int main() {
    Order order;
    std::cout << "Start: " << order.status() << "\n";
    for (int i = 0; i < 3; ++i) {
        order.next();
        std::cout << "Next:  " << order.status() << "\n";
    }
    CHECK(order.status() == "Delivered");

    bool threw = false;
    try {
        order.cancel();
    } catch (const std::runtime_error& e) {
        std::cout << "Error: " << e.what() << "\n";
        threw = true;
    }
    CHECK(threw);

    Order early;
    early.cancel();
    std::cout << "Early order cancelled: " << early.status() << "\n";
    CHECK(early.status() == "Cancelled");
}
