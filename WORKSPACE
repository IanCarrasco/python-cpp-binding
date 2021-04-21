workspace(name = "mylib")

""" Load External Dependency to Fetch from Remote Sources """
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

""" General utilities for bazel buildgen files """
http_archive(
    name = "bazel_skylib",
    strip_prefix = "bazel-skylib-0.9.0",
    url = "https://github.com/bazelbuild/bazel-skylib/archive/0.9.0.zip",
    sha256 = "a8677c64e2a58eb113f305784e6af9759cfa3f9a6eacb4d40531fe1bd6356aca",
)

""" C++ Utilities """
http_archive(
    name = "com_google_absl",
    strip_prefix = "abseil-cpp-master",
    urls = ["https://github.com/abseil/abseil-cpp/archive/master.zip"],
)

""" Google testing framework """
http_archive(
    name = "com_google_googletest",
    strip_prefix = "googletest-master",
    urls = ["https://github.com/google/googletest/archive/master.zip"],
)

""" Framework for generating python bindings for C++ code """
http_archive(
    name = "pybind11",
    build_file = "@//bazel:pybind11.BUILD",
    sha256 = "1f844c071d9d98f5bb08458f128baa0aa08a9e5939a6b42276adb1bacd8b483e",
    strip_prefix = "pybind11-2.3.0",
    url = "https://github.com/pybind/pybind11/archive/v2.3.0.zip",
)


new_local_repository(
    name = "python_headers",
    path = "/usr/include/python3.9",  # May be overwritten by setup.py.
    build_file = "@//bazel:python_headers.BUILD"
)

# This is a transitive external dependency of @com_google_absl//absl/strings.
# Bazel doesn't pull in transitive dependencies from external WORKSPACE files.
# (https://docs.bazel.build/versions/master/external.html#transitive-dependencies)
http_archive(
    name = "rules_cc",
    strip_prefix = "rules_cc-master",
    urls = ["https://github.com/bazelbuild/rules_cc/archive/master.zip"],
)

load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")
bazel_skylib_workspace()