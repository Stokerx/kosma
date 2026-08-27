use bytes::Bytes;
use http_body_util::Full;
use hyper::{header::HeaderValue, Response, StatusCode};

pub struct CorsConfig {
    pub enabled: bool,
    pub allow_origin: String,
    pub allow_methods: String,
    pub allow_headers: String,
}

impl Default for CorsConfig {
    fn default() -> Self {
        Self {
            enabled: false,
            allow_origin: "*".to_string(),
            allow_methods: "GET, POST, PUT, DELETE, PATCH, OPTIONS".to_string(),
            allow_headers: "Content-Type, Authorization, X-Requested-With".to_string(),
        }
    }
}

pub fn json_response(status: StatusCode, body: Bytes, cors: &CorsConfig) -> Response<Full<Bytes>> {
    let mut builder = Response::builder()
        .status(status)
        .header("content-type", HeaderValue::from_static("application/json"))
        .header("server", HeaderValue::from_static("Kosma/0.1.0"));

    if cors.enabled {
        builder = apply_cors_headers(builder, cors);
    }

    builder.body(Full::new(body)).unwrap()
}

pub fn html_response(status: StatusCode, html: &str, cors: &CorsConfig) -> Response<Full<Bytes>> {
    let mut builder = Response::builder()
        .status(status)
        .header(
            "content-type",
            HeaderValue::from_static("text/html; charset=utf-8"),
        )
        .header("server", HeaderValue::from_static("Kosma/0.1.0"));

    if cors.enabled {
        builder = apply_cors_headers(builder, cors);
    }

    builder.body(Full::new(Bytes::from(html.to_string()))).unwrap()
}

pub fn text_response(status: StatusCode, text: &str, cors: &CorsConfig) -> Response<Full<Bytes>> {
    let mut builder = Response::builder()
        .status(status)
        .header(
            "content-type",
            HeaderValue::from_static("text/plain; charset=utf-8"),
        )
        .header("server", HeaderValue::from_static("Kosma/0.1.0"));

    if cors.enabled {
        builder = apply_cors_headers(builder, cors);
    }

    builder.body(Full::new(Bytes::from(text.to_string()))).unwrap()
}

pub fn preflight_cors_response(cors: &CorsConfig) -> Response<Full<Bytes>> {
    let mut builder = Response::builder()
        .status(StatusCode::NO_CONTENT)
        .header("server", HeaderValue::from_static("Kosma/0.1.0"));

    if cors.enabled {
        builder = apply_cors_headers(builder, cors);
    }

    builder.body(Full::new(Bytes::new())).unwrap()
}

pub fn error_response(status: StatusCode, message: &str, cors: &CorsConfig) -> Response<Full<Bytes>> {
    let err_json = format!("{{\"error\": \"{}\"}}", message);
    json_response(status, Bytes::from(err_json), cors)
}

fn apply_cors_headers(
    builder: hyper::http::response::Builder,
    cors: &CorsConfig,
) -> hyper::http::response::Builder {
    builder
        .header("access-control-allow-origin", &cors.allow_origin)
        .header("access-control-allow-methods", &cors.allow_methods)
        .header("access-control-allow-headers", &cors.allow_headers)
        .header("access-control-max-age", "86400")
}
