from typing import Callable, Any

class RouteMeta:
    def __init__(self, method: str, path: str):
        self.method = method.upper()
        self.path = path

def route(method: str, path: str):
    def decorator(fn: Callable[..., Any]):
        setattr(fn, "__velox_route__", RouteMeta(method, path))
        return fn
    return decorator

def get(path: str):
    return route("GET", path)

def post(path: str):
    return route("POST", path)

def put(path: str):
    return route("PUT", path)

def delete(path: str):
    return route("DELETE", path)

def patch(path: str):
    return route("PATCH", path)
