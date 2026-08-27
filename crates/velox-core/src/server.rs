use crate::response::{error_response, json_response};
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
                eprintln!("[Velox] Accept error: {}", e);
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
    let uri = req.uri();
    let path = uri.path();
    let query_str = uri.query().unwrap_or("").to_string();

    // 1. Router matching en Rust (Zero GIL)
    let (handler_info, path_params) = match state.router.lookup(method, path) {
        Some(matched) => matched,
        None => {
            return error_response(StatusCode::NOT_FOUND, "Route not found");
        }
    };

    // 2. Extraer body de la petición HTTP
    let body_bytes = match req.into_body().collect().await {
        Ok(collected) => collected.to_bytes(),
        Err(e) => {
            return error_response(
                StatusCode::BAD_REQUEST,
                &format!("Error reading request body: {}", e),
            );
        }
    };

    // 3. Cruzar frontera PyO3 en spawn_blocking para no bloquear Tokio
    let py_result = tokio::task::spawn_blocking(move || {
        execute_python_handler(handler_info, body_bytes, path_params, query_str)
    })
    .await;

    match py_result {
        Ok(Ok((status_code, response_bytes))) => {
            let status = StatusCode::from_u16(status_code).unwrap_or(StatusCode::OK);
            json_response(status, response_bytes)
        }
        Ok(Err(py_err_msg)) => {
            error_response(StatusCode::INTERNAL_SERVER_ERROR, &py_err_msg)
        }
        Err(join_err) => {
            error_response(
                StatusCode::INTERNAL_SERVER_ERROR,
                &format!("Worker thread error: {}", join_err),
            )
        }
    }
}

fn execute_python_handler(
    handler_info: RouteHandler,
    body_bytes: Bytes,
    path_params: Vec<(String, String)>,
    query_str: String,
) -> Result<(u16, Bytes), String> {
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

        if let Ok(raw_bytes) = result.extract::<&[u8]>() {
            Ok((200, Bytes::copy_from_slice(raw_bytes)))
        } else if let Ok(tuple) = result.downcast::<PyTuple>() {
            if tuple.len() == 2 {
                let status: u16 = tuple.get_item(0).and_then(|i| i.extract()).unwrap_or(200);
                let body_item = tuple.get_item(1).map_err(|e| e.to_string())?;
                if let Ok(raw_bytes) = body_item.extract::<&[u8]>() {
                    Ok((status, Bytes::copy_from_slice(raw_bytes)))
                } else if let Ok(s) = body_item.extract::<String>() {
                    Ok((status, Bytes::from(s)))
                } else {
                    Ok((status, Bytes::from(body_item.to_string())))
                }
            } else {
                Err("Invalid handler return tuple length (expected 2: (status, body))".into())
            }
        } else if let Ok(s) = result.extract::<String>() {
            Ok((200, Bytes::from(s)))
        } else {
            Ok((200, Bytes::from(result.to_string())))
        }
    })
}
