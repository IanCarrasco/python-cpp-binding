load("//bazel:build_defs.bzl", "pybind11_extension")

licenses(["notice"])  # Apache 2.0 License

pybind11_extension(
    name = "_example",
    srcs = ["_example.cc"],
    visibility = ["//mylib:__subpackages__"],
    deps = ["//mylib/cc:example"],
)