// Composite: compose objects into tree structures and treat individual objects and compositions uniformly.
#include <iostream>
#include <memory>
#include <string>
#include <vector>

#include "check.h"

class FileSystemNode {
public:
    explicit FileSystemNode(std::string name) : name_(std::move(name)) {}
    virtual ~FileSystemNode() = default;
    virtual long size() const = 0;
    virtual void print(std::ostream& out, int indent = 0) const = 0;

protected:
    std::string name_;
};

class File : public FileSystemNode {
public:
    File(std::string name, long size) : FileSystemNode(std::move(name)), size_(size) {}
    long size() const override { return size_; }
    void print(std::ostream& out, int indent) const override {
        out << std::string(indent * 2, ' ') << name_ << " (" << size_ << " B)\n";
    }

private:
    long size_;
};

class Folder : public FileSystemNode {
public:
    using FileSystemNode::FileSystemNode;

    Folder& add(std::unique_ptr<FileSystemNode> child) {
        children_.push_back(std::move(child));
        return *this;
    }
    long size() const override {
        long total = 0;
        for (const auto& child : children_) total += child->size();
        return total;
    }
    void print(std::ostream& out, int indent) const override {
        out << std::string(indent * 2, ' ') << name_ << "/ (" << size() << " B)\n";
        for (const auto& child : children_) child->print(out, indent + 1);
    }

private:
    std::vector<std::unique_ptr<FileSystemNode>> children_;
};

int main() {
    auto src = std::make_unique<Folder>("src");
    src->add(std::make_unique<File>("main.cpp", 800)).add(std::make_unique<File>("utils.cpp", 300));

    Folder root("project");
    root.add(std::make_unique<File>("README.md", 120)).add(std::move(src));
    root.print(std::cout, 0);

    CHECK(root.size() == 1220);
}
