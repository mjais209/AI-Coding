// Observer: define a one-to-many dependency so that when one object changes state, all dependents are notified.
#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "check.h"

// Subject / publisher.
class Stock {
public:
    using Listener = std::function<void(const std::string&, double)>;

    explicit Stock(std::string symbol) : symbol_(std::move(symbol)) {}

    int subscribe(Listener listener) {
        listeners_[nextId_] = std::move(listener);
        return nextId_++;
    }
    void unsubscribe(int id) { listeners_.erase(id); }

    void setPrice(double price) {
        price_ = price;
        for (auto& [id, listener] : listeners_) listener(symbol_, price_);
    }

private:
    std::string symbol_;
    double price_ = 0;
    int nextId_ = 0;
    std::map<int, Listener> listeners_;
};

// A concrete observer.
class PriceAlert {
public:
    explicit PriceAlert(double threshold) : threshold_(threshold) {}
    void operator()(const std::string& symbol, double price) {
        if (price > threshold_) alerts.push_back("ALERT: " + symbol + " above threshold: " + std::to_string(price));
    }
    std::vector<std::string> alerts;

private:
    double threshold_;
};

int main() {
    Stock stock("ACME");
    PriceAlert alert(120);

    int loggerId =
        stock.subscribe([](const std::string& s, double p) { std::cout << "[logger] " << s << " -> " << p << "\n"; });
    stock.subscribe([&alert](const std::string& s, double p) { alert(s, p); });

    stock.setPrice(110);
    stock.setPrice(125);
    stock.unsubscribe(loggerId);  // logger stops receiving updates
    stock.setPrice(130);

    for (const auto& a : alert.alerts) std::cout << a << "\n";
    CHECK(alert.alerts.size() == 2);
}
