// Template Method: define the skeleton of an algorithm in a base class, letting subclasses override specific steps.
#include <iostream>
#include <string>
#include <vector>

#include "check.h"

struct Row {
    std::string name;
    bool active;
};

class DataExporter {
public:
    virtual ~DataExporter() = default;

    // The template method: a fixed sequence of steps. Not virtual, so subclasses can't change the order.
    std::string exportRows(const std::vector<Row>& rows) const {
        std::vector<Row> selected = filter(rows);
        return header() + body(selected) + footer();
    }

protected:
    virtual std::vector<Row> filter(const std::vector<Row>& rows) const { return rows; }  // hook with default
    virtual std::string header() const = 0;
    virtual std::string body(const std::vector<Row>& rows) const = 0;
    virtual std::string footer() const { return ""; }  // hook with default
};

class CsvExporter : public DataExporter {
protected:
    std::string header() const override { return "name,active\n"; }
    std::string body(const std::vector<Row>& rows) const override {
        std::string out;
        for (const auto& r : rows) out += r.name + "," + (r.active ? "true" : "false") + "\n";
        return out;
    }
};

class HtmlExporter : public DataExporter {
protected:
    std::vector<Row> filter(const std::vector<Row>& rows) const override {
        std::vector<Row> active;
        for (const auto& r : rows)
            if (r.active) active.push_back(r);
        return active;
    }
    std::string header() const override { return "<table>\n"; }
    std::string body(const std::vector<Row>& rows) const override {
        std::string out;
        for (const auto& r : rows) out += "  <tr><td>" + r.name + "</td></tr>\n";
        return out;
    }
    std::string footer() const override { return "</table>\n"; }
};

int main() {
    std::vector<Row> rows{{"Alice", true}, {"Bob", false}};
    std::string csv = CsvExporter().exportRows(rows);
    std::string html = HtmlExporter().exportRows(rows);
    std::cout << csv << "\n" << html;

    CHECK(csv == "name,active\nAlice,true\nBob,false\n");
    CHECK(html.find("Bob") == std::string::npos);
}
