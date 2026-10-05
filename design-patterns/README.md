# Design Patterns in C++

Runnable, self-contained C++17 examples of all 23 classic "Gang of Four" design patterns. Each pattern is one `.cpp` file with its own `main()`. The file opens with a one-line definition and builds a realistic example. Every demo checks its own behavior with `CHECK(...)` (see `include/check.h`) and exits non-zero if a check fails, so CTest doubles as the test suite.

Requires a C++17 compiler (GCC 8+, Clang 7+, MSVC 2019+) and CMake 3.16+. No other dependencies.

## Build and run

```bash
cd design-patterns
./run_all.sh                 # build, then run every demo
./run_all.sh observer        # only demos whose name contains "observer"

# or manually
cmake -S . -B build
cmake --build build -j
./build/strategy             # run a single pattern
(cd build && ctest --output-on-failure)
```

A single file can also be compiled directly: `g++ -std=c++17 -Iinclude behavioral/state.cpp -o state && ./state`.

## Patterns

### Creational: how objects are created

| Pattern | Example | File |
|---|---|---|
| Singleton | One shared `AppConfig` (Meyers singleton, thread-safe) | [creational/singleton.cpp](creational/singleton.cpp) |
| Factory Method | `RoadLogistics` / `SeaLogistics` create a `Truck` / `Ship` | [creational/factory_method.cpp](creational/factory_method.cpp) |
| Abstract Factory | Light/dark theme factories create matching buttons and checkboxes | [creational/abstract_factory.cpp](creational/abstract_factory.cpp) |
| Builder | Fluent `PizzaBuilder` plus a `PizzaDirector` recipe | [creational/builder.cpp](creational/builder.cpp) |
| Prototype | Polymorphic `clone()` of shapes from a registry | [creational/prototype.cpp](creational/prototype.cpp) |

### Structural: how objects are composed

| Pattern | Example | File |
|---|---|---|
| Adapter | Wraps a legacy payment gateway that takes amounts in cents | [structural/adapter.cpp](structural/adapter.cpp) |
| Bridge | `Remote` abstractions over `TV` / `Radio` devices | [structural/bridge.cpp](structural/bridge.cpp) |
| Composite | File/folder tree that computes its size recursively | [structural/composite.cpp](structural/composite.cpp) |
| Decorator | Adds milk/caramel to an espresso | [structural/decorator.cpp](structural/decorator.cpp) |
| Facade | `OrderFacade` hides inventory, payment, shipping and email | [structural/facade.cpp](structural/facade.cpp) |
| Flyweight | 1000 trees share 2 `TreeType` objects | [structural/flyweight.cpp](structural/flyweight.cpp) |
| Proxy | `ImageProxy` that loads lazily and checks access | [structural/proxy.cpp](structural/proxy.cpp) |

### Behavioral: how objects communicate

| Pattern | Example | File |
|---|---|---|
| Chain of Responsibility | Expense approval passes TeamLead → Manager → Director | [behavioral/chain_of_responsibility.cpp](behavioral/chain_of_responsibility.cpp) |
| Command | Text editor commands with undo | [behavioral/command.cpp](behavioral/command.cpp) |
| Interpreter | Evaluates prefix arithmetic expressions with variables | [behavioral/interpreter.cpp](behavioral/interpreter.cpp) |
| Iterator | STL-compatible in-order iterator over a BST (works with range-for) | [behavioral/iterator.cpp](behavioral/iterator.cpp) |
| Mediator | `ChatRoom` routes messages between users | [behavioral/mediator.cpp](behavioral/mediator.cpp) |
| Memento | Editor snapshots that the caretaker can't read inside | [behavioral/memento.cpp](behavioral/memento.cpp) |
| Observer | Stock price subscribers via `std::function` | [behavioral/observer.cpp](behavioral/observer.cpp) |
| State | Order lifecycle: Pending → Paid → Shipped → Delivered | [behavioral/state.cpp](behavioral/state.cpp) |
| Strategy | Swappable shopping-cart discount strategies | [behavioral/strategy.cpp](behavioral/strategy.cpp) |
| Template Method | CSV/HTML exporters share one export skeleton | [behavioral/template_method.cpp](behavioral/template_method.cpp) |
| Visitor | Area and JSON-export visitors over shapes (double dispatch) | [behavioral/visitor.cpp](behavioral/visitor.cpp) |
