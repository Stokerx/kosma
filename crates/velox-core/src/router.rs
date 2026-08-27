use matchit::Router as MatchitRouter;
use pyo3::prelude::*;
use std::sync::Arc;

#[derive(Clone)]
pub struct RouteHandler {
    pub handler: Arc<Py<PyAny>>,
    pub is_async: bool,
}

pub struct AppRouter {
    inner: MatchitRouter<RouteHandler>,
}

impl AppRouter {
    pub fn new() -> Self {
        Self {
            inner: MatchitRouter::new(),
        }
    }

    pub fn insert(
        &mut self,
        method: &str,
        path: &str,
        handler: Py<PyAny>,
        is_async: bool,
    ) -> Result<(), String> {
        let route_key = format!("{}:{}", method.to_uppercase(), path);
        self.inner
            .insert(
                route_key,
                RouteHandler {
                    handler: Arc::new(handler),
                    is_async,
                },
            )
            .map_err(|e| format!("Error registering route '{}': {}", path, e))
    }

    pub fn lookup<'a>(
        &'a self,
        method: &str,
        path: &'a str,
    ) -> Option<(RouteHandler, Vec<(String, String)>)> {
        let route_key = format!("{}:{}", method.to_uppercase(), path);
        match self.inner.at(&route_key) {
            Ok(matched) => {
                let params: Vec<(String, String)> = matched
                    .params
                    .iter()
                    .map(|(k, v)| (k.to_string(), v.to_string()))
                    .collect();
                Some((matched.value.clone(), params))
            }
            Err(_) => None,
        }
    }
}
