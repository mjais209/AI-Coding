// Facade: provide a simple, unified interface to a complex subsystem.
#include <iostream>
#include <string>
#include <vector>

#include "check.h"

class Inventory {
public:
    std::string reserve(const std::string& sku) { return "reserved " + sku; }
};

class Payment {
public:
    std::string charge(int cents) { return "charged " + std::to_string(cents) + " cents"; }
};

class Shipping {
public:
    std::string schedule(const std::string& address) { return "shipping to " + address; }
};

class Notification {
public:
    std::string email(const std::string& to) { return "emailed " + to; }
};

class OrderFacade {
public:
    std::vector<std::string> placeOrder(const std::string& sku, int cents, const std::string& address,
                                        const std::string& email) {
        return {inventory_.reserve(sku), payment_.charge(cents), shipping_.schedule(address),
                notification_.email(email)};
    }

private:
    Inventory inventory_;
    Payment payment_;
    Shipping shipping_;
    Notification notification_;
};

int main() {
    OrderFacade shop;
    auto steps = shop.placeOrder("SKU-42", 4990, "221B Baker St", "alice@example.com");
    for (const auto& step : steps) std::cout << step << "\n";

    CHECK(steps.size() == 4);
    CHECK(steps[1] == "charged 4990 cents");
}
