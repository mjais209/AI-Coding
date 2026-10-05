#pragma once

#include <cstdlib>
#include <iostream>

// Like assert(), but stays enabled in Release builds so every demo self-verifies.
#define CHECK(cond)                                                                    \
    do {                                                                               \
        if (!(cond)) {                                                                 \
            std::cerr << __FILE__ << ":" << __LINE__ << ": CHECK failed: " #cond "\n"; \
            std::exit(1);                                                              \
        }                                                                              \
    } while (0)
