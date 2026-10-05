// Chain of Responsibility: pass a request along a chain of handlers until one handles it.
#include <iostream>
#include <memory>
#include <string>

#include "check.h"

class Approver {
public:
    virtual ~Approver() = default;

    Approver& setNext(std::unique_ptr<Approver> next) {
        next_ = std::move(next);
        return *next_;
    }

    std::string handle(long amount) const {
        if (canApprove(amount)) return name() + " approved $" + std::to_string(amount);
        if (next_) return next_->handle(amount);
        return "Nobody can approve $" + std::to_string(amount);
    }

protected:
    virtual bool canApprove(long amount) const = 0;
    virtual std::string name() const = 0;

private:
    std::unique_ptr<Approver> next_;
};

class TeamLead : public Approver {
protected:
    bool canApprove(long amount) const override { return amount <= 1'000; }
    std::string name() const override { return "TeamLead"; }
};

class Manager : public Approver {
protected:
    bool canApprove(long amount) const override { return amount <= 10'000; }
    std::string name() const override { return "Manager"; }
};

class Director : public Approver {
protected:
    bool canApprove(long amount) const override { return amount <= 100'000; }
    std::string name() const override { return "Director"; }
};

int main() {
    TeamLead chain;
    chain.setNext(std::make_unique<Manager>()).setNext(std::make_unique<Director>());

    for (long amount : {500L, 5'000L, 50'000L, 500'000L}) std::cout << chain.handle(amount) << "\n";

    CHECK(chain.handle(5'000) == "Manager approved $5000");
    CHECK(chain.handle(1'000'000) == "Nobody can approve $1000000");
}
