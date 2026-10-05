// Adapter: convert the interface of a class into another interface clients expect.
#include <cmath>
#include <iostream>
#include <string>

#include "check.h"

// Target interface our checkout code expects.
class PaymentProcessor {
public:
    virtual ~PaymentProcessor() = default;
    virtual std::string pay(double amount) = 0;
};

// Third-party class with an incompatible interface (amounts in cents).
class LegacyPayGateway {
public:
    std::string makePayment(long cents, const std::string& currency) {
        return "LegacyPay charged " + std::to_string(cents) + " " + currency + " cents";
    }
};

class LegacyPayAdapter : public PaymentProcessor {
public:
    explicit LegacyPayAdapter(LegacyPayGateway& gateway) : gateway_(gateway) {}
    std::string pay(double amount) override { return gateway_.makePayment(std::lround(amount * 100), "USD"); }

private:
    LegacyPayGateway& gateway_;
};

std::string checkout(PaymentProcessor& processor, double amount) { return processor.pay(amount); }

int main() {
    LegacyPayGateway gateway;
    LegacyPayAdapter adapter(gateway);
    std::string result = checkout(adapter, 19.99);
    std::cout << result << "\n";

    CHECK(result == "LegacyPay charged 1999 USD cents");
}
