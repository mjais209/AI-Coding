// Interpreter: define a grammar and an interpreter that evaluates sentences in that language.
//
// Grammar (prefix / Polish notation):  expr := number | variable | ('+' | '-' | '*') expr expr
#include <cctype>
#include <iostream>
#include <map>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>

#include "check.h"

using Context = std::map<std::string, int>;

class Expression {
public:
    virtual ~Expression() = default;
    virtual int interpret(const Context& ctx) const = 0;
};

class Number : public Expression {
public:
    explicit Number(int value) : value_(value) {}
    int interpret(const Context&) const override { return value_; }

private:
    int value_;
};

class Variable : public Expression {
public:
    explicit Variable(std::string name) : name_(std::move(name)) {}
    int interpret(const Context& ctx) const override { return ctx.at(name_); }

private:
    std::string name_;
};

class BinaryOp : public Expression {
public:
    BinaryOp(char op, std::unique_ptr<Expression> l, std::unique_ptr<Expression> r)
        : op_(op), left_(std::move(l)), right_(std::move(r)) {}

    int interpret(const Context& ctx) const override {
        int a = left_->interpret(ctx), b = right_->interpret(ctx);
        switch (op_) {
            case '+':
                return a + b;
            case '-':
                return a - b;
            case '*':
                return a * b;
        }
        throw std::logic_error("unknown operator");
    }

private:
    char op_;
    std::unique_ptr<Expression> left_, right_;
};

std::unique_ptr<Expression> parse(std::istringstream& tokens) {
    std::string token;
    if (!(tokens >> token)) throw std::invalid_argument("unexpected end of input");
    if (token == "+" || token == "-" || token == "*") {
        auto left = parse(tokens);
        auto right = parse(tokens);
        return std::make_unique<BinaryOp>(token[0], std::move(left), std::move(right));
    }
    if (std::isdigit(static_cast<unsigned char>(token[0]))) return std::make_unique<Number>(std::stoi(token));
    return std::make_unique<Variable>(token);
}

std::unique_ptr<Expression> parse(const std::string& source) {
    std::istringstream tokens(source);
    return parse(tokens);
}

int main() {
    const std::string source = "+ * x 2 - y 3";  // (x * 2) + (y - 3)
    Context ctx{{"x", 5}, {"y", 10}};
    int result = parse(source)->interpret(ctx);

    std::cout << source << "  with x=5, y=10  =  " << result << "\n";
    CHECK(result == 17);
}
