// Proxy: provide a surrogate that controls access to another object (lazy loading, caching, access control).
#include <iostream>
#include <memory>
#include <string>

#include "check.h"

class Image {
public:
    virtual ~Image() = default;
    virtual std::string display() = 0;
};

class RealImage : public Image {
public:
    static inline int loadCount = 0;

    explicit RealImage(std::string filename) : filename_(std::move(filename)) {
        ++loadCount;  // pretend this is an expensive load from disk
    }
    std::string display() override { return "Displaying " + filename_; }

private:
    std::string filename_;
};

// Virtual proxy (lazy loading) + protection proxy (access control).
class ImageProxy : public Image {
public:
    ImageProxy(std::string filename, std::string role = "viewer")
        : filename_(std::move(filename)), role_(std::move(role)) {}

    std::string display() override {
        if (role_ != "viewer" && role_ != "admin") return "Access denied to " + filename_;
        if (!real_) real_ = std::make_unique<RealImage>(filename_);
        return real_->display();
    }

private:
    std::string filename_, role_;
    std::unique_ptr<RealImage> real_;
};

int main() {
    ImageProxy image("photo.png");
    std::cout << "Loads before display: " << RealImage::loadCount << "\n";
    CHECK(RealImage::loadCount == 0);

    std::cout << image.display() << "\n" << image.display() << "\n";
    std::cout << "Loads after two displays: " << RealImage::loadCount << "\n";
    CHECK(RealImage::loadCount == 1);

    ImageProxy secret("secret.png", "guest");
    std::string denied = secret.display();
    std::cout << denied << "\n";
    CHECK(denied == "Access denied to secret.png");
}
