pub mod response;
pub mod router;
pub mod server;

use pyo3::prelude::*;
use router::AppRouter;
use server::{run_server, ServerState};
use std::net::SocketAddr;
use std::sync::Arc;

#[pyclass]
pub struct NativeServer {
    router: Option<AppRouter>,
    routes_count: usize,
}

#[pymethods]
impl NativeServer {
    #[new]
    fn new() -> Self {
        NativeServer {
            router: Some(AppRouter::new()),
            routes_count: 0,
        }
    }

    fn add_route(
        &mut self,
        method: String,
        path: String,
        handler: Py<PyAny>,
        is_async: bool,
    ) -> PyResult<()> {
        if let Some(ref mut router) = self.router {
            router
                .insert(&method, &path, handler, is_async)
                .map_err(|e| pyo3::exceptions::PyValueError::new_err(e))?;
            self.routes_count += 1;
            Ok(())
        } else {
            Err(pyo3::exceptions::PyRuntimeError::new_err(
                "Server is already running",
            ))
        }
    }

    fn routes_len(&self) -> usize {
        self.routes_count
    }

    #[pyo3(signature = (host, port, workers=None))]
    fn serve(
        &mut self,
        py: Python<'_>,
        host: String,
        port: u16,
        workers: Option<usize>,
    ) -> PyResult<()> {
        let router = self.router.take().ok_or_else(|| {
            pyo3::exceptions::PyRuntimeError::new_err("Server is already running or router consumed")
        })?;

        let state = Arc::new(ServerState { router });
        let addr_str = format!("{}:{}", host, port);
        let addr: SocketAddr = addr_str.parse().map_err(|e: std::net::AddrParseError| {
            pyo3::exceptions::PyValueError::new_err(format!("Invalid address: {}", e))
        })?;

        let worker_threads = workers.unwrap_or_else(num_cpus_count);

        // Liberar el GIL para que Tokio asuma el control del socket en paralelo
        py.allow_threads(move || {
            let runtime = match tokio::runtime::Builder::new_multi_thread()
                .worker_threads(worker_threads)
                .enable_all()
                .build()
            {
                Ok(rt) => rt,
                Err(e) => {
                    eprintln!("[Velox] Failed to build Tokio runtime: {}", e);
                    return;
                }
            };

            runtime.block_on(async move {
                println!(
                    "⚡ Velox HTTP Engine (Hyper 1.0 + Tokio) corriendo en http://{}",
                    addr
                );
                if let Err(e) = run_server(state, addr).await {
                    eprintln!("[Velox] Server runtime error: {}", e);
                }
            });
        });

        Ok(())
    }
}

fn num_cpus_count() -> usize {
    std::thread::available_parallelism()
        .map(|n| n.get())
        .unwrap_or(4)
}

#[pymodule]
fn velox_core(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<NativeServer>()?;
    Ok(())
}
