pub mod response;
pub mod router;
pub mod server;

use pyo3::prelude::*;
use response::CorsConfig;
use router::AppRouter;
use server::{run_server, ServerState};
use std::net::SocketAddr;
use std::sync::Arc;

#[pyclass]
pub struct NativeServer {
    router: Option<AppRouter>,
    routes_count: usize,
    cors: CorsConfig,
}

#[pymethods]
impl NativeServer {
    #[new]
    fn new() -> Self {
        NativeServer {
            router: Some(AppRouter::new()),
            routes_count: 0,
            cors: CorsConfig::default(),
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

    #[pyo3(signature = (allow_origins=None, allow_methods=None, allow_headers=None))]
    fn set_cors(
        &mut self,
        allow_origins: Option<Vec<String>>,
        allow_methods: Option<Vec<String>>,
        allow_headers: Option<Vec<String>>,
    ) {
        self.cors.enabled = true;
        if let Some(origins) = allow_origins {
            self.cors.allow_origin = origins.join(", ");
        }
        if let Some(methods) = allow_methods {
            self.cors.allow_methods = methods.join(", ");
        }
        if let Some(headers) = allow_headers {
            self.cors.allow_headers = headers.join(", ");
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

        let state = Arc::new(ServerState {
            router,
            cors: self.cors.clone(),
        });

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
                    eprintln!("[Kosma] Failed to build Tokio runtime: {}", e);
                    return;
                }
            };

            runtime.block_on(async move {
                println!(
                    "⚡ Kosma HTTP Engine (Hyper 1.0 + Tokio) corriendo en http://{}",
                    addr
                );
                if let Err(e) = run_server(state, addr).await {
                    eprintln!("[Kosma] Server runtime error: {}", e);
                }
            });
        });

        Ok(())
    }
}

// Implement Clone for CorsConfig
impl Clone for CorsConfig {
    fn clone(&self) -> Self {
        Self {
            enabled: self.enabled,
            allow_origin: self.allow_origin.clone(),
            allow_methods: self.allow_methods.clone(),
            allow_headers: self.allow_headers.clone(),
        }
    }
}

fn num_cpus_count() -> usize {
    std::thread::available_parallelism()
        .map(|n| n.get())
        .unwrap_or(4)
}

#[pymodule]
fn kosma_core(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<NativeServer>()?;
    Ok(())
}
