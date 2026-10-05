// Bridge: decouple an abstraction from its implementation so the two can vary independently.
#include <algorithm>
#include <iostream>
#include <memory>
#include <string>

#include "check.h"

// Implementation hierarchy.
class Device {
public:
    virtual ~Device() = default;
    virtual std::string name() const = 0;
    bool on = false;
    int volume = 10;
};

class TV : public Device {
public:
    std::string name() const override { return "TV"; }
};

class Radio : public Device {
public:
    std::string name() const override { return "Radio"; }
};

// Abstraction hierarchy: holds a reference to an implementation.
class Remote {
public:
    explicit Remote(std::shared_ptr<Device> device) : device_(std::move(device)) {}
    virtual ~Remote() = default;

    std::string togglePower() {
        device_->on = !device_->on;
        return device_->name() + " power " + (device_->on ? "on" : "off");
    }
    std::string volumeUp() {
        device_->volume = std::min(100, device_->volume + 10);
        return device_->name() + " volume " + std::to_string(device_->volume);
    }

protected:
    std::shared_ptr<Device> device_;
};

class AdvancedRemote : public Remote {
public:
    using Remote::Remote;
    std::string mute() {
        device_->volume = 0;
        return device_->name() + " muted";
    }
};

int main() {
    auto tv = std::make_shared<TV>();
    auto radio = std::make_shared<Radio>();

    Remote basic(tv);
    std::cout << basic.togglePower() << "\n" << basic.volumeUp() << "\n";

    AdvancedRemote advanced(radio);
    std::cout << advanced.togglePower() << "\n" << advanced.volumeUp() << "\n" << advanced.mute() << "\n";

    CHECK(tv->on && tv->volume == 20);
    CHECK(radio->volume == 0);
}
