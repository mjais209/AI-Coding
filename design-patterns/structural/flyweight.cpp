// Flyweight: share common (intrinsic) state between many objects to save memory.
#include <iostream>
#include <map>
#include <memory>
#include <string>
#include <tuple>
#include <vector>

#include "check.h"

// Intrinsic, shared, immutable state.
struct TreeType {
    const std::string name, color, texture;
};

class TreeTypeFactory {
public:
    std::shared_ptr<const TreeType> get(const std::string& name, const std::string& color, const std::string& texture) {
        auto key = std::make_tuple(name, color, texture);
        auto it = cache_.find(key);
        if (it != cache_.end()) return it->second;
        auto type = std::make_shared<const TreeType>(TreeType{name, color, texture});
        cache_.emplace(key, type);
        return type;
    }
    size_t count() const { return cache_.size(); }

private:
    std::map<std::tuple<std::string, std::string, std::string>, std::shared_ptr<const TreeType>> cache_;
};

// Extrinsic, per-object state plus a pointer to the shared flyweight.
struct Tree {
    int x, y;
    std::shared_ptr<const TreeType> type;
};

int main() {
    TreeTypeFactory factory;
    std::vector<Tree> forest;
    for (int i = 0; i < 1000; ++i) {
        if (i % 2)
            forest.push_back({i, i * 2, factory.get("Oak", "green", "rough")});
        else
            forest.push_back({i, i * 3, factory.get("Pine", "dark-green", "needles")});
    }

    std::cout << "Trees planted: " << forest.size() << ", shared TreeType objects: " << factory.count() << "\n";

    CHECK(forest.size() == 1000 && factory.count() == 2);
    CHECK(forest[1].type == forest[3].type);
}
