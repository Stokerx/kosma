from typing import Callable, Any, Optional

class RouteMeta:
    def __init__(self, method: str, path: str, status_code: int = 200):
        self.method = method.upper()
        self.path = path
        self.status_code = status_code

def route(method: str, path: str, status_code: int = 200):
    def decorator(fn: Callable[..., Any]):
        setattr(fn, "__kosma_route__", RouteMeta(method, path, status_code))
        return fn
    return decorator

def get(path: str, status_code: int = 200):
    return route("GET", path, status_code)

def post(path: str, status_code: int = 201):
    return route("POST", path, status_code)

def put(path: str, status_code: int = 200):
    return route("PUT", path, status_code)

def delete(path: str, status_code: int = 200):
    return route("DELETE", path, status_code)

def patch(path: str, status_code: int = 200):
    return route("PATCH", path, status_code)
