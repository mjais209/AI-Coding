// Visitor: add new operations to an object structure without modifying the classes of its elements.
#include <cmath>
#include <iomanip>
#include <iostream>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

#include "check.h"

class Circle;
class Rectangle;

class ShapeVisitor {
public:
    virtual ~ShapeVisitor() = default;
    virtual void visit(const Circle& c) = 0;
    virtual void visit(const Rectangle& r) = 0;
};

class Shape {
public:
    virtual ~Shape() = default;
    virtual void accept(ShapeVisitor& v) const = 0;  // double dispatch entry point
};

class Circle : public Shape {
public:
    explicit Circle(double r) : radius(r) {}
    void accept(ShapeVisitor& v) const override { v.visit(*this); }
    double radius;
};

class Rectangle : public Shape {
public:
    Rectangle(double w, double h) : width(w), height(h) {}
    void accept(ShapeVisitor& v) const override { v.visit(*this); }
    double width, height;
};

class AreaVisitor : public ShapeVisitor {
public:
    void visit(const Circle& c) override { total += M_PI * c.radius * c.radius; }
    void visit(const Rectangle& r) override { total += r.width * r.height; }
    double total = 0;
};

class JsonExportVisitor : public ShapeVisitor {
public:
    void visit(const Circle& c) override { out << R"({"type": "circle", "radius": )" << c.radius << "}\n"; }
    void visit(const Rectangle& r) override {
        out << R"({"type": "rectangle", "width": )" << r.width << R"(, "height": )" << r.height << "}\n";
    }
    std::ostringstream out;
};

int main() {
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(1));
    shapes.push_back(std::make_unique<Rectangle>(3, 4));

    AreaVisitor area;
    JsonExportVisitor json;
    for (const auto& s : shapes) {
        s->accept(area);
        s->accept(json);
    }

    std::cout << json.out.str() << "Total area: " << std::fixed << std::setprecision(2) << area.total << "\n";
    CHECK(std::abs(area.total - (M_PI + 12)) < 1e-9);
}
