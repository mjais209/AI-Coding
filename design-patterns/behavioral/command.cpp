// Command: encapsulate a request as an object, enabling queuing, logging and undo.
#include <iostream>
#include <memory>
#include <string>
#include <vector>

#include "check.h"

struct TextEditor {
    std::string text;
};

class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
};

class AppendText : public Command {
public:
    AppendText(TextEditor& editor, std::string text) : editor_(editor), text_(std::move(text)) {}
    void execute() override { editor_.text += text_; }
    void undo() override { editor_.text.erase(editor_.text.size() - text_.size()); }

private:
    TextEditor& editor_;
    std::string text_;
};

class ClearText : public Command {
public:
    explicit ClearText(TextEditor& editor) : editor_(editor) {}
    void execute() override {
        backup_ = editor_.text;
        editor_.text.clear();
    }
    void undo() override { editor_.text = backup_; }

private:
    TextEditor& editor_;
    std::string backup_;
};

class CommandInvoker {
public:
    void run(std::unique_ptr<Command> command) {
        command->execute();
        history_.push_back(std::move(command));
    }
    void undo() {
        if (history_.empty()) return;
        history_.back()->undo();
        history_.pop_back();
    }

private:
    std::vector<std::unique_ptr<Command>> history_;
};

int main() {
    TextEditor editor;
    CommandInvoker invoker;

    invoker.run(std::make_unique<AppendText>(editor, "Hello"));
    invoker.run(std::make_unique<AppendText>(editor, ", World"));
    std::cout << "After appends: '" << editor.text << "'\n";
    CHECK(editor.text == "Hello, World");

    invoker.run(std::make_unique<ClearText>(editor));
    std::cout << "After clear:   '" << editor.text << "'\n";
    CHECK(editor.text.empty());

    invoker.undo();
    std::cout << "Undo clear:    '" << editor.text << "'\n";
    CHECK(editor.text == "Hello, World");

    invoker.undo();
    std::cout << "Undo append:   '" << editor.text << "'\n";
    CHECK(editor.text == "Hello");
}
