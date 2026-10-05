// Prototype: create new objects by cloning an existing instance instead of building from scratch.
#include <iostream>
#include <map>
#include <memory>
#include <string>
#include <vector>

#include "check.h"

class Shape {
public:
    virtual ~Shape() = default;
    virtual std::unique_ptr<Shape> clone() const = 0;
    virtual std::string describe() const = 0;

    std::string color = "black";
    std::vector<std::string> tags;
};

class Circle : public Shape {
public:
    explicit Circle(int radius) : radius(radius) {}
    std::unique_ptr<Shape> clone() const override { return std::make_unique<Circle>(*this); }
    std::string describe() const override {
        return color + " circle r=" + std::to_string(radius) + " tags=" + std::to_string(tags.size());
    }
    int radius;
};

class Rectangle : public Shape {
public:
    Rectangle(int w, int h) : width(w), height(h) {}
    std::unique_ptr<Shape> clone() const override { return std::make_unique<Rectangle>(*this); }
    std::string describe() const override {
        return color + " rectangle " + std::to_string(width) + "x" + std::to_string(height) +
               " tags=" + std::to_string(tags.size());
    }
    int width, height;
};

class PrototypeRegistry {
public:
    void add(const std::string& name, std::unique_ptr<Shape> prototype) { prototypes_[name] = std::move(prototype); }
    std::unique_ptr<Shape> create(const std::string& name) const { return prototypes_.at(name)->clone(); }

private:
    std::map<std::string, std::unique_ptr<Shape>> prototypes_;
};

int main() {
    PrototypeRegistry registry;
    auto redCircle = std::make_unique<Circle>(10);
    redCircle->color = "red";
    redCircle->tags = {"logo"};
    registry.add("red-circle", std::move(redCircle));
    registry.add("square", std::make_unique<Rectangle>(5, 5));

    auto a = registry.create("red-circle");
    a->tags.push_back("copy");  // modifying a clone must not affect the prototype
    auto b = registry.create("red-circle");
    auto c = registry.create("square");

    std::cout << a->describe() << "\n" << b->describe() << "\n" << c->describe() << "\n";

    CHECK(a->tags.size() == 2 && b->tags.size() == 1);
    CHECK(a.get() != b.get());
}
