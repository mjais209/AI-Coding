// Memento: capture and restore an object's internal state without violating encapsulation.
#include <iostream>
#include <stack>
#include <string>

#include "check.h"

// Originator.
class Editor {
public:
    // Opaque snapshot: only Editor can read its contents.
    class Memento {
        friend class Editor;
        Memento(std::string content, size_t cursor) : content_(std::move(content)), cursor_(cursor) {}
        std::string content_;
        size_t cursor_;
    };

    void type(const std::string& text) {
        content_.insert(cursor_, text);
        cursor_ += text.size();
    }
    Memento save() const { return Memento(content_, cursor_); }
    void restore(const Memento& m) {
        content_ = m.content_;
        cursor_ = m.cursor_;
    }
    const std::string& content() const { return content_; }

private:
    std::string content_;
    size_t cursor_ = 0;
};

// Caretaker: stores mementos but never looks inside them.
class History {
public:
    void push(Editor::Memento m) { snapshots_.push(std::move(m)); }
    Editor::Memento pop() {
        Editor::Memento m = snapshots_.top();
        snapshots_.pop();
        return m;
    }

private:
    std::stack<Editor::Memento> snapshots_;
};

int main() {
    Editor editor;
    History history;

    editor.type("Design ");
    history.push(editor.save());
    editor.type("patterns ");
    history.push(editor.save());
    editor.type("are tricky!!!");
    std::cout << "Current:  '" << editor.content() << "'\n";

    editor.restore(history.pop());
    std::cout << "Restored: '" << editor.content() << "'\n";
    CHECK(editor.content() == "Design patterns ");

    editor.restore(history.pop());
    std::cout << "Restored: '" << editor.content() << "'\n";
    CHECK(editor.content() == "Design ");
}
