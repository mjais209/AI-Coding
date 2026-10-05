// Decorator: attach additional responsibilities to an object dynamically by wrapping it.
#include <cmath>
#include <iomanip>
#include <iostream>
#include <memory>
#include <string>

#include "check.h"

class Coffee {
public:
    virtual ~Coffee() = default;
    virtual double cost() const = 0;
    virtual std::string description() const = 0;
};

class Espresso : public Coffee {
public:
    double cost() const override { return 2.00; }
    std::string description() const override { return "Espresso"; }
};

class CoffeeDecorator : public Coffee {
public:
    explicit CoffeeDecorator(std::unique_ptr<Coffee> inner) : inner_(std::move(inner)) {}

protected:
    std::unique_ptr<Coffee> inner_;
};

class Milk : public CoffeeDecorator {
public:
    using CoffeeDecorator::CoffeeDecorator;
    double cost() const override { return inner_->cost() + 0.50; }
    std::string description() const override { return inner_->description() + " + milk"; }
};

class Caramel : public CoffeeDecorator {
public:
    using CoffeeDecorator::CoffeeDecorator;
    double cost() const override { return inner_->cost() + 0.75; }
    std::string description() const override { return inner_->description() + " + caramel"; }
};

int main() {
    std::unique_ptr<Coffee> order = std::make_unique<Espresso>();
    order = std::make_unique<Milk>(std::move(order));
    order = std::make_unique<Milk>(std::move(order));
    order = std::make_unique<Caramel>(std::move(order));

    std::cout << order->description() << ": $" << std::fixed << std::setprecision(2) << order->cost() << "\n";

    CHECK(order->description() == "Espresso + milk + milk + caramel");
    CHECK(std::abs(order->cost() - 3.75) < 1e-9);
}
