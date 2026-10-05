// Iterator: access elements of a collection sequentially without exposing its underlying representation.
#include <iostream>
#include <iterator>
#include <memory>
#include <stack>
#include <vector>

#include "check.h"

class BinarySearchTree {
    struct Node {
        int value;
        std::unique_ptr<Node> left, right;
    };

public:
    // STL-compatible forward iterator doing an in-order traversal with an explicit stack.
    class iterator {
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = int;
        using difference_type = std::ptrdiff_t;
        using pointer = const int*;
        using reference = const int&;

        iterator() = default;
        explicit iterator(Node* root) { pushLeft(root); }

        reference operator*() const { return stack_.top()->value; }
        iterator& operator++() {
            Node* node = stack_.top();
            stack_.pop();
            pushLeft(node->right.get());
            return *this;
        }
        bool operator==(const iterator& other) const {
            return stack_.empty() ? other.stack_.empty() : !other.stack_.empty() && stack_.top() == other.stack_.top();
        }
        bool operator!=(const iterator& other) const { return !(*this == other); }

    private:
        void pushLeft(Node* node) {
            for (; node; node = node->left.get()) stack_.push(node);
        }
        std::stack<Node*> stack_;
    };

    void insert(int value) {
        std::unique_ptr<Node>* slot = &root_;
        while (*slot) slot = value < (*slot)->value ? &(*slot)->left : &(*slot)->right;
        *slot = std::make_unique<Node>(Node{value, nullptr, nullptr});
    }

    iterator begin() const { return iterator(root_.get()); }
    iterator end() const { return iterator(); }

private:
    std::unique_ptr<Node> root_;
};

int main() {
    BinarySearchTree tree;
    for (int v : {50, 30, 70, 20, 40, 60, 80}) tree.insert(v);

    std::vector<int> visited;
    std::cout << "In-order traversal:";
    for (int v : tree) {  // range-for works because the tree exposes begin()/end()
        std::cout << " " << v;
        visited.push_back(v);
    }
    std::cout << "\n";

    CHECK((visited == std::vector<int>{20, 30, 40, 50, 60, 70, 80}));
}
