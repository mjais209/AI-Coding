"""Run the demo of every design pattern example, or only those matching a name filter.

Usage:
    python run_all.py              # all patterns
    python run_all.py observer     # patterns whose module name contains "observer"
"""

import importlib
import pkgutil
import sys

CATEGORIES = ("creational", "structural", "behavioral")


def pattern_modules() -> list[str]:
    modules = []
    for category in CATEGORIES:
        package = importlib.import_module(category)
        modules += [f"{category}.{m.name}" for m in pkgutil.iter_modules(package.__path__)]
    return modules


def main(argv: list[str]) -> None:
    name_filter = argv[0].lower() if argv else ""
    for module_name in pattern_modules():
        if name_filter not in module_name:
            continue
        module = importlib.import_module(module_name)
        title = module_name.split(".")[1].replace("_", " ").title()
        print(f"\n=== {module_name.split('.')[0].title()}: {title} ===")
        print((module.__doc__ or "").strip().splitlines()[0])
        print("-" * 60)
        module.main()


if __name__ == "__main__":
    main(sys.argv[1:])
