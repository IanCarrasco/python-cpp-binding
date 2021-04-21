#import "pybind11/pybind11.h"
#import "pybind11/pytypes.h"
#import "mylib/cc/example.h"

namespace py = pybind11;

PYBIND11_MODULE(_example, m) {
    m.def("add", &add);
}