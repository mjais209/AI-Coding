// Builder: construct a complex object step by step; the same process can create different representations.
#include <iostream>
#include <string>
#include <vector>

#include "check.h"

struct Pizza {
    std::string size = "medium";
    std::string crust = "regular";
    std::vector<std::string> toppings;

    std::string describe() const {
        std::string result = size + " pizza, " + crust + " crust";
        for (const auto& t : toppings) result += ", " + t;
        return result;
    }
};

class PizzaBuilder {
public:
    PizzaBuilder& size(const std::string& s) {
        pizza_.size = s;
        return *this;
    }
    PizzaBuilder& crust(const std::string& c) {
        pizza_.crust = c;
        return *this;
    }
    PizzaBuilder& topping(const std::string& t) {
        pizza_.toppings.push_back(t);
        return *this;
    }
    Pizza build() {
        Pizza result = std::move(pizza_);
        pizza_ = Pizza{};  // reset so the builder can be reused
        return result;
    }

private:
    Pizza pizza_;
};

// Optional director that knows recipes expressed as builder steps.
class PizzaDirector {
public:
    static Pizza margherita(PizzaBuilder& b) {
        return b.size("medium").crust("thin").topping("tomato").topping("mozzarella").topping("basil").build();
    }
};

int main() {
    PizzaBuilder builder;
    Pizza custom = builder.size("large").crust("stuffed").topping("pepperoni").topping("olives").build();
    Pizza margherita = PizzaDirector::margherita(builder);

    std::cout << custom.describe() << "\n" << margherita.describe() << "\n";

    CHECK(custom.toppings.size() == 2);
    CHECK(margherita.crust == "thin" && margherita.toppings.size() == 3);
    CHECK(builder.build().toppings.empty());
}
