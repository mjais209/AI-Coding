"""Template Method: define the skeleton of an algorithm in a base class, letting subclasses override specific steps."""

from abc import ABC, abstractmethod


class DataExporter(ABC):
    def export(self, rows: list[dict]) -> str:
        """The template method: fixed sequence of steps."""
        rows = self.filter(rows)
        return self.header(rows) + self.body(rows) + self.footer()

    def filter(self, rows: list[dict]) -> list[dict]:
        return rows  # hook with default behavior

    @abstractmethod
    def header(self, rows: list[dict]) -> str: ...

    @abstractmethod
    def body(self, rows: list[dict]) -> str: ...

    def footer(self) -> str:
        return ""


class CsvExporter(DataExporter):
    def header(self, rows: list[dict]) -> str:
        return ",".join(rows[0].keys()) + "\n" if rows else ""

    def body(self, rows: list[dict]) -> str:
        return "".join(",".join(str(v) for v in row.values()) + "\n" for row in rows)


class HtmlExporter(DataExporter):
    def filter(self, rows: list[dict]) -> list[dict]:
        return [r for r in rows if r.get("active")]

    def header(self, rows: list[dict]) -> str:
        return "<table>\n"

    def body(self, rows: list[dict]) -> str:
        return "".join(f"  <tr><td>{r['name']}</td></tr>\n" for r in rows)

    def footer(self) -> str:
        return "</table>\n"


def main() -> None:
    rows = [{"name": "Alice", "active": True}, {"name": "Bob", "active": False}]
    print(CsvExporter().export(rows))
    print(HtmlExporter().export(rows))


if __name__ == "__main__":
    main()
