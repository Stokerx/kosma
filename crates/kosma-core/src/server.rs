use crate::response::{
    error_response, html_response, json_response, preflight_cors_response, CorsConfig,
};
use crate::router::{AppRouter, RouteHandler};
use bytes::Bytes;
use http_body_util::{BodyExt, Full};
use hyper::service::service_fn;
use hyper::{Request, Response, StatusCode};
use hyper_util::rt::{TokioExecutor, TokioIo};
use hyper_util::server::conn::auto;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyTuple};
use std::convert::Infallible;
use std::net::SocketAddr;
use std::sync::Arc;
use tokio::net::TcpListener;

pub struct ServerState {
    pub router: AppRouter,
    pub cors: CorsConfig,
}

pub async fn run_server(
    state: Arc<ServerState>,
    addr: SocketAddr,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let listener = TcpListener::bind(addr).await?;
    let auto_server = auto::Builder::new(TokioExecutor::new());

    loop {
        let (stream, _) = match listener.accept().await {
            Ok(conn) => conn,
            Err(e) => {
                eprintln!("[Kosma] Accept error: {}", e);
                continue;
            }
        };

        let io = TokioIo::new(stream);
        let state = Arc::clone(&state);
        let auto_server = auto_server.clone();

        tokio::spawn(async move {
            let service = service_fn(move |req: Request<hyper::body::Incoming>| {
                let state = Arc::clone(&state);
                async move {
                    Ok::<_, Infallible>(handle_request(req, state).await)
                }
            });

            if let Err(err) = auto_server.serve_connection(io, service).await {
                let _ = err;
            }
        });
    }
}

async fn handle_request(
    req: Request<hyper::body::Incoming>,
    state: Arc<ServerState>,
) -> Response<Full<Bytes>> {
    let method = req.method().as_str();

    // 1. Manejo automático de CORS Preflight (OPTIONS)
    if method == "OPTIONS" && state.cors.enabled {
        return preflight_cors_response(&state.cors);
    }

    let uri = req.uri();
    let path = uri.path();
    let query_str = uri.query().unwrap_or("").to_string();

    // 2. Router matching en Rust (Zero GIL)
    let (handler_info, path_params) = match state.router.lookup(method, path) {
        Some(matched) => matched,
        None => {
            return error_response(StatusCode::NOT_FOUND, "Route not found", &state.cors);
        }
    };

    // 3. Extraer body de la petición HTTP
    let body_bytes = match req.into_body().collect().await {
        Ok(collected) => collected.to_bytes(),
        Err(e) => {
            return error_response(
                StatusCode::BAD_REQUEST,
                &format!("Error reading request body: {}", e),
                &state.cors,
            );
        }
    };

    // 4. Cruzar frontera PyO3 en spawn_blocking para no bloquear Tokio
    let py_result = tokio::task::spawn_blocking(move || {
        execute_python_handler(handler_info, body_bytes, path_params, query_str)
    })
    .await;

    match py_result {
        Ok(Ok((status_code, content_type, response_bytes))) => {
            let status = StatusCode::from_u16(status_code).unwrap_or(StatusCode::OK);
            if content_type == "text/html" {
                let html_str = String::from_utf8_lossy(&response_bytes);
                html_response(status, &html_str, &state.cors)
            } else {
                json_response(status, response_bytes, &state.cors)
            }
        }
        Ok(Err(py_err_msg)) => {
            error_response(StatusCode::INTERNAL_SERVER_ERROR, &py_err_msg, &state.cors)
        }
        Err(join_err) => {
            error_response(
                StatusCode::INTERNAL_SERVER_ERROR,
                &format!("Worker thread error: {}", join_err),
                &state.cors,
            )
        }
    }
}

fn execute_python_handler(
    handler_info: RouteHandler,
    body_bytes: Bytes,
    path_params: Vec<(String, String)>,
    query_str: String,
) -> Result<(u16, String, Bytes), String> {
    Python::with_gil(|py| {
        let py_body = PyBytes::new_bound(py, &body_bytes);

        let py_params = PyDict::new_bound(py);
        for (k, v) in path_params {
            py_params.set_item(k, v).map_err(|e| e.to_string())?;
        }

        let py_query = PyDict::new_bound(py);
        if !query_str.is_empty() {
            for pair in query_str.split('&') {
                if let Some((k, v)) = pair.split_once('=') {
                    py_query.set_item(k, v).map_err(|e| e.to_string())?;
                } else if !pair.is_empty() {
                    py_query.set_item(pair, "").map_err(|e| e.to_string())?;
                }
            }
        }

        let bound_handler = handler_info.handler.bind(py);
        let args = (py_body, py_params, py_query);
        let result = bound_handler
            .call1(args)
            .map_err(|e| format!("Python Exception: {}", e))?;

        // Desempaquetar respuesta de Python:
        // 1. (status, bytes)
        // 2. (status, content_type, bytes)
        // 3. raw bytes o string
        if let Ok(tuple) = result.downcast::<PyTuple>() {
            if tuple.len() == 3 {
                let status: u16 = tuple.get_item(0).and_then(|i| i.extract()).unwrap_or(200);
                let content_type: String = tuple.get_item(1).and_then(|i| i.extract()).unwrap_or_else(|_| "application/json".to_string());
                let body_item = tuple.get_item(2).map_err(|e| e.to_string())?;
                let body_bytes = extract_bytes(body_item)?;
                Ok((status, content_type, body_bytes))
            } else if tuple.len() == 2 {
                let status: u16 = tuple.get_item(0).and_then(|i| i.extract()).unwrap_or(200);
                let body_item = tuple.get_item(1).map_err(|e| e.to_string())?;
                let body_bytes = extract_bytes(body_item)?;
                let content_type = if body_bytes.starts_with(b"<!DOCTYPE") || body_bytes.starts_with(b"<html") {
                    "text/html".to_string()
                } else {
                    "application/json".to_string()
                };
                Ok((status, content_type, body_bytes))
            } else {
                Err("Invalid handler tuple return length".into())
            }
        } else if let Ok(raw_bytes) = result.extract::<&[u8]>() {
            Ok((200, "application/json".to_string(), Bytes::copy_from_slice(raw_bytes)))
        } else if let Ok(s) = result.extract::<String>() {
            let content_type = if s.starts_with("<!DOCTYPE") || s.starts_with("<html") {
                "text/html".to_string()
            } else {
                "application/json".to_string()
            };
            Ok((200, content_type, Bytes::from(s)))
        } else {
            Ok((200, "application/json".to_string(), Bytes::from(result.to_string())))
        }
    })
}

fn extract_bytes(item: pyo3::Bound<'_, PyAny>) -> Result<Bytes, String> {
    if let Ok(raw_bytes) = item.extract::<&[u8]>() {
        Ok(Bytes::copy_from_slice(raw_bytes))
    } else if let Ok(s) = item.extract::<String>() {
        Ok(Bytes::from(s))
    } else {
        Ok(Bytes::from(item.to_string()))
    }
}
