# Design Patterns in Python

Runnable, self-contained examples of all 23 classic "Gang of Four" design patterns. Each file has a short explanation, a realistic example, and a `main()` demo.

Requires Python 3.10+. No third-party dependencies (pytest only for tests).

## Run

```bash
cd design-patterns
python run_all.py                     # run every demo
python run_all.py observer            # run demos whose name contains "observer"
python -m behavioral.strategy         # run a single pattern
pip install pytest && python -m pytest -q
```

## Patterns

### Creational — how objects are created

| Pattern | Example | File |
|---|---|---|
| Singleton | One shared `AppConfig` (thread-safe metaclass) | [creational/singleton.py](creational/singleton.py) |
| Factory Method | `RoadLogistics` / `SeaLogistics` create `Truck` / `Ship` | [creational/factory_method.py](creational/factory_method.py) |
| Abstract Factory | Light/Dark theme factories create matching buttons and checkboxes | [creational/abstract_factory.py](creational/abstract_factory.py) |
| Builder | Fluent `PizzaBuilder` plus a `PizzaDirector` recipe | [creational/builder.py](creational/builder.py) |
| Prototype | Clone invoice `Document`s from a registry | [creational/prototype.py](creational/prototype.py) |

### Structural — how objects are composed

| Pattern | Example | File |
|---|---|---|
| Adapter | Wrap a legacy cents-based payment gateway | [structural/adapter.py](structural/adapter.py) |
| Bridge | `Remote` abstractions over `TV` / `Radio` devices | [structural/bridge.py](structural/bridge.py) |
| Composite | File/folder tree with recursive size | [structural/composite.py](structural/composite.py) |
| Decorator | Add milk/caramel to an espresso | [structural/decorator.py](structural/decorator.py) |
| Facade | `OrderFacade` hides inventory, payment, shipping, email | [structural/facade.py](structural/facade.py) |
| Flyweight | 1000 trees share 2 `TreeType` objects | [structural/flyweight.py](structural/flyweight.py) |
| Proxy | Lazy-loading, access-controlled `ImageProxy` | [structural/proxy.py](structural/proxy.py) |

### Behavioral — how objects communicate

| Pattern | Example | File |
|---|---|---|
| Chain of Responsibility | TeamLead → Manager → Director expense approval | [behavioral/chain_of_responsibility.py](behavioral/chain_of_responsibility.py) |
| Command | Text editor commands with undo | [behavioral/command.py](behavioral/command.py) |
| Interpreter | Evaluate prefix arithmetic expressions with variables | [behavioral/interpreter.py](behavioral/interpreter.py) |
| Iterator | In-order iterator over a binary search tree | [behavioral/iterator.py](behavioral/iterator.py) |
| Mediator | `ChatRoom` routes messages between users | [behavioral/mediator.py](behavioral/mediator.py) |
| Memento | Editor snapshots and restore | [behavioral/memento.py](behavioral/memento.py) |
| Observer | Stock price subscribers and alerts | [behavioral/observer.py](behavioral/observer.py) |
| State | Order lifecycle: Pending → Paid → Shipped → Delivered | [behavioral/state.py](behavioral/state.py) |
| Strategy | Swappable shopping-cart discount strategies | [behavioral/strategy.py](behavioral/strategy.py) |
| Template Method | CSV/HTML exporters share an export skeleton | [behavioral/template_method.py](behavioral/template_method.py) |
| Visitor | Area and JSON-export visitors over shapes | [behavioral/visitor.py](behavioral/visitor.py) |
