import pytest

import run_all
from behavioral import (
    chain_of_responsibility,
    command,
    interpreter,
    iterator,
    mediator,
    memento,
    observer,
    state,
    strategy,
    template_method,
    visitor,
)
from creational import abstract_factory, builder, factory_method, prototype, singleton
from structural import adapter, bridge, composite, decorator, facade, flyweight, proxy


def test_all_23_patterns_present():
    assert len(run_all.pattern_modules()) == 23


@pytest.mark.parametrize("module_name", run_all.pattern_modules())
def test_every_demo_runs(module_name, capsys):
    run_all.main([module_name.split(".")[1]])
    assert capsys.readouterr().out.strip()


# Creational
def test_singleton():
    assert singleton.AppConfig() is singleton.AppConfig()


def test_factory_method():
    assert "Ship" in factory_method.SeaLogistics().plan_delivery("x")


def test_abstract_factory():
    assert abstract_factory.render_form(abstract_factory.DarkThemeFactory()) == "[Dark Button] [Dark Checkbox]"


def test_builder_resets_between_builds():
    b = builder.PizzaBuilder()
    first = b.topping("ham").build()
    second = b.build()
    assert first.toppings == ["ham"] and second.toppings == []


def test_prototype_is_deep_copy():
    original = prototype.Document("t", "b", ["a"])
    clone = original.clone(title="t2")
    clone.tags.append("b")
    assert original.tags == ["a"] and clone.title == "t2"


# Structural
def test_adapter_converts_to_cents():
    assert adapter.LegacyPayAdapter(adapter.LegacyPayGateway()).pay(1.5) == "LegacyPay charged 150 USD cents"


def test_bridge():
    remote = bridge.AdvancedRemote(bridge.TV())
    remote.volume_up()
    assert remote.device.volume == 20
    remote.mute()
    assert remote.device.volume == 0


def test_composite_size():
    root = composite.Folder("r").add(composite.File("a", 1)).add(composite.Folder("s").add(composite.File("b", 2)))
    assert root.size() == 3


def test_decorator():
    coffee = decorator.Caramel(decorator.Milk(decorator.Espresso()))
    assert coffee.cost() == pytest.approx(3.25)
    assert coffee.description() == "Espresso + milk + caramel"


def test_facade():
    assert len(facade.OrderFacade().place_order("s", 1, "a", "e")) == 4


def test_flyweight_shares_instances():
    a = flyweight.TreeTypeFactory.get("Birch", "white", "smooth")
    b = flyweight.TreeTypeFactory.get("Birch", "white", "smooth")
    assert a is b


def test_proxy_lazy_and_protected():
    before = proxy.RealImage.load_count
    image = proxy.ImageProxy("x.png")
    assert proxy.RealImage.load_count == before
    image.display()
    image.display()
    assert proxy.RealImage.load_count == before + 1
    assert "denied" in proxy.ImageProxy("y.png", user_role="guest").display()


# Behavioral
def test_chain_of_responsibility():
    chain = chain_of_responsibility.build_chain()
    assert chain.handle(5_000).startswith("Manager")
    assert chain.handle(1_000_000).startswith("Nobody")


def test_command_undo():
    editor, invoker = command.TextEditor(), command.CommandInvoker()
    invoker.run(command.AppendText(editor, "ab"))
    invoker.run(command.ClearText(editor))
    invoker.undo()
    assert editor.text == "ab"
    invoker.undo()
    assert editor.text == ""


def test_interpreter():
    assert interpreter.parse("+ * x 2 - y 3").interpret({"x": 5, "y": 10}) == 17


def test_iterator_in_order():
    tree = iterator.BinarySearchTree()
    for v in (5, 3, 8, 1, 4):
        tree.insert(v)
    assert list(tree) == [1, 3, 4, 5, 8]


def test_mediator():
    room = mediator.ChatRoom()
    a, b, c = mediator.User("a"), mediator.User("b"), mediator.User("c")
    for u in (a, b, c):
        room.join(u)
    a.send("hi")
    b.send("psst", to="a")
    assert b.inbox == ["a: hi"] and a.inbox == ["b: psst"] and c.inbox == ["a: hi"]


def test_memento():
    editor = memento.Editor()
    editor.type("one")
    snapshot = editor.save()
    editor.type("two")
    editor.restore(snapshot)
    assert editor.content == "one"


def test_observer():
    stock = observer.Stock("X", 1)
    alert = observer.PriceAlert(10)
    stock.subscribe(alert)
    stock.price = 5
    stock.price = 15
    assert len(alert.alerts) == 1


def test_state_transitions():
    order = state.Order()
    order.next()
    order.next()
    assert isinstance(order.state, state.Shipped)
    with pytest.raises(RuntimeError):
        order.cancel()
    pending = state.Order()
    pending.cancel()
    assert isinstance(pending.state, state.Cancelled)


def test_strategy():
    cart = strategy.ShoppingCart(strategy.PercentageDiscount(10))
    cart.add(100)
    assert cart.total() == 90
    cart.strategy = strategy.FlatDiscount(200)
    assert cart.total() == 0


def test_template_method():
    rows = [{"name": "A", "active": True}, {"name": "B", "active": False}]
    assert template_method.CsvExporter().export(rows) == "name,active\nA,True\nB,False\n"
    assert "B" not in template_method.HtmlExporter().export(rows)


def test_visitor():
    assert visitor.Rectangle(3, 4).accept(visitor.AreaVisitor()) == 12
