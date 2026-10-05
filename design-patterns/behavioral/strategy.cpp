// Strategy: define a family of interchangeable algorithms and select one at runtime.
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <memory>
#include <numeric>
#include <vector>

#include "check.h"

class DiscountStrategy {
public:
    virtual ~DiscountStrategy() = default;
    virtual double apply(double total) const = 0;
    virtual const char* name() const = 0;
};

class NoDiscount : public DiscountStrategy {
public:
    double apply(double total) const override { return total; }
    const char* name() const override { return "NoDiscount"; }
};

class PercentageDiscount : public DiscountStrategy {
public:
    explicit PercentageDiscount(double percent) : percent_(percent) {}
    double apply(double total) const override { return total * (1 - percent_ / 100); }
    const char* name() const override { return "PercentageDiscount"; }

private:
    double percent_;
};

class FlatDiscount : public DiscountStrategy {
public:
    explicit FlatDiscount(double amount) : amount_(amount) {}
    double apply(double total) const override { return std::max(0.0, total - amount_); }
    const char* name() const override { return "FlatDiscount"; }

private:
    double amount_;
};

class ShoppingCart {
public:
    void add(double price) { items_.push_back(price); }
    void setStrategy(std::shared_ptr<DiscountStrategy> s) { strategy_ = std::move(s); }
    double total() const { return strategy_->apply(std::accumulate(items_.begin(), items_.end(), 0.0)); }

private:
    std::vector<double> items_;
    std::shared_ptr<DiscountStrategy> strategy_ = std::make_shared<NoDiscount>();
};

int main() {
    ShoppingCart cart;
    cart.add(40);
    cart.add(60);

    std::vector<std::shared_ptr<DiscountStrategy>> strategies{
        std::make_shared<NoDiscount>(), std::make_shared<PercentageDiscount>(15), std::make_shared<FlatDiscount>(25)};
    for (const auto& s : strategies) {
        cart.setStrategy(s);
        std::cout << std::left << std::setw(20) << s->name() << " total = $" << std::fixed << std::setprecision(2)
                  << cart.total() << "\n";
    }

    cart.setStrategy(std::make_shared<PercentageDiscount>(10));
    CHECK(std::abs(cart.total() - 90) < 1e-9);
    cart.setStrategy(std::make_shared<FlatDiscount>(200));
    CHECK(cart.total() == 0);
}
