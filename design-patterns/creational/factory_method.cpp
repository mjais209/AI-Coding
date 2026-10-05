// Factory Method: define an interface for creating an object, but let subclasses decide which class to instantiate.
#include <iostream>
#include <memory>
#include <string>
#include <vector>

#include "check.h"

class Transport {
public:
    virtual ~Transport() = default;
    virtual std::string deliver(const std::string& cargo) const = 0;
};

class Truck : public Transport {
public:
    std::string deliver(const std::string& cargo) const override { return "Truck delivers " + cargo + " by road"; }
};

class Ship : public Transport {
public:
    std::string deliver(const std::string& cargo) const override { return "Ship delivers " + cargo + " by sea"; }
};

class Logistics {
public:
    virtual ~Logistics() = default;

    // The factory method.
    virtual std::unique_ptr<Transport> createTransport() const = 0;

    std::string planDelivery(const std::string& cargo) const { return createTransport()->deliver(cargo); }
};

class RoadLogistics : public Logistics {
public:
    std::unique_ptr<Transport> createTransport() const override { return std::make_unique<Truck>(); }
};

class SeaLogistics : public Logistics {
public:
    std::unique_ptr<Transport> createTransport() const override { return std::make_unique<Ship>(); }
};

int main() {
    std::vector<std::unique_ptr<Logistics>> companies;
    companies.push_back(std::make_unique<RoadLogistics>());
    companies.push_back(std::make_unique<SeaLogistics>());

    for (const auto& company : companies) std::cout << company->planDelivery("10 boxes") << "\n";

    CHECK(SeaLogistics().planDelivery("x") == "Ship delivers x by sea");
}
