use waypoint_host_python::CallOptions;
use pyo3::prelude::*;

pub(crate) fn binding(py: Python<'_>) -> PyResult<Bound<'_, PyModule>> {
    py.import("waypoint.rust_bridge.streams")
}

pub(crate) fn call_options(asynchronous: bool) -> CallOptions {
    CallOptions::new(asynchronous, binding)
}
