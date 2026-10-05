// Singleton: ensure a class has only one instance and provide a global access point to it.
#include <iostream>
#include <map>
#include <mutex>
#include <string>

#include "check.h"

class AppConfig {
public:
    static AppConfig& instance() {
        static AppConfig config;  // thread-safe lazy initialization since C++11
        return config;
    }

    AppConfig(const AppConfig&) = delete;
    AppConfig& operator=(const AppConfig&) = delete;

    void set(const std::string& key, const std::string& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        settings_[key] = value;
    }

    std::string get(const std::string& key) const {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = settings_.find(key);
        return it == settings_.end() ? "" : it->second;
    }

private:
    AppConfig() = default;
    mutable std::mutex mutex_;
    std::map<std::string, std::string> settings_;
};

int main() {
    AppConfig& a = AppConfig::instance();
    AppConfig& b = AppConfig::instance();
    a.set("env", "production");

    std::cout << "Same instance: " << std::boolalpha << (&a == &b) << "\n";
    std::cout << "b sees value set via a: env=" << b.get("env") << "\n";

    CHECK(&a == &b);
    CHECK(b.get("env") == "production");
}
