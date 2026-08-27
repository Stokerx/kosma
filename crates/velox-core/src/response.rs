use bytes::Bytes;
use http_body_util::Full;
use hyper::{Response, StatusCode, header::HeaderValue};

pub fn json_response(status: StatusCode, body: Bytes) -> Response<Full<Bytes>> {
    Response::builder()
        .status(status)
        .header("content-type", HeaderValue::from_static("application/json"))
        .header("server", HeaderValue::from_static("Velox/0.1.0"))
        .body(Full::new(body))
        .unwrap()
}

pub fn text_response(status: StatusCode, text: &str) -> Response<Full<Bytes>> {
    Response::builder()
        .status(status)
        .header("content-type", HeaderValue::from_static("text/plain; charset=utf-8"))
        .header("server", HeaderValue::from_static("Velox/0.1.0"))
        .body(Full::new(Bytes::from(text.to_string())))
        .unwrap()
}

pub fn error_response(status: StatusCode, message: &str) -> Response<Full<Bytes>> {
    let err_json = format!("{{\"error\": \"{}\"}}", message);
    Response::builder()
        .status(status)
        .header("content-type", HeaderValue::from_static("application/json"))
        .header("server", HeaderValue::from_static("Velox/0.1.0"))
        .body(Full::new(Bytes::from(err_json)))
        .unwrap()
}
