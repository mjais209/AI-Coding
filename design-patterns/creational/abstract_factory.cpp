// Abstract Factory: create families of related objects without specifying their concrete classes.
#include <iostream>
#include <memory>
#include <string>

#include "check.h"

class Button {
public:
    virtual ~Button() = default;
    virtual std::string render() const = 0;
};

class Checkbox {
public:
    virtual ~Checkbox() = default;
    virtual std::string render() const = 0;
};

class LightButton : public Button {
public:
    std::string render() const override { return "[Light Button]"; }
};
class LightCheckbox : public Checkbox {
public:
    std::string render() const override { return "[Light Checkbox]"; }
};
class DarkButton : public Button {
public:
    std::string render() const override { return "[Dark Button]"; }
};
class DarkCheckbox : public Checkbox {
public:
    std::string render() const override { return "[Dark Checkbox]"; }
};

class UIFactory {
public:
    virtual ~UIFactory() = default;
    virtual std::unique_ptr<Button> createButton() const = 0;
    virtual std::unique_ptr<Checkbox> createCheckbox() const = 0;
};

class LightThemeFactory : public UIFactory {
public:
    std::unique_ptr<Button> createButton() const override { return std::make_unique<LightButton>(); }
    std::unique_ptr<Checkbox> createCheckbox() const override { return std::make_unique<LightCheckbox>(); }
};

class DarkThemeFactory : public UIFactory {
public:
    std::unique_ptr<Button> createButton() const override { return std::make_unique<DarkButton>(); }
    std::unique_ptr<Checkbox> createCheckbox() const override { return std::make_unique<DarkCheckbox>(); }
};

// Client code depends only on the abstract interfaces.
std::string renderForm(const UIFactory& factory) {
    return factory.createButton()->render() + " " + factory.createCheckbox()->render();
}

int main() {
    std::cout << "Light: " << renderForm(LightThemeFactory()) << "\n";
    std::cout << "Dark:  " << renderForm(DarkThemeFactory()) << "\n";

    CHECK(renderForm(DarkThemeFactory()) == "[Dark Button] [Dark Checkbox]");
}
