cmake_minimum_required(VERSION 3.16)
project(DesignPatterns LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release)
endif()

if(MSVC)
  add_compile_options(/W4 /permissive- /D_USE_MATH_DEFINES)
else()
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

enable_testing()

# One executable (and one CTest test) per pattern file, e.g. behavioral/observer.cpp -> ./observer
foreach(category creational structural behavioral)
  file(GLOB sources CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${category}/*.cpp)
  foreach(source ${sources})
    get_filename_component(name ${source} NAME_WE)
    add_executable(${name} ${source})
    target_include_directories(${name} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
    add_test(NAME ${category}.${name} COMMAND ${name})
  endforeach()
endforeach()
