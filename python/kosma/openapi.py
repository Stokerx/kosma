import orjson
from dataclasses import is_dataclass, fields
from typing import Dict, List, Any, get_type_hints

def type_to_openapi_type(py_type: Any) -> dict:
    if py_type is int:
        return {"type": "integer"}
    elif py_type is float:
        return {"type": "number"}
    elif py_type is bool:
        return {"type": "boolean"}
    elif py_type is str:
        return {"type": "string"}
    elif is_dataclass(py_type):
        hints = get_type_hints(py_type) if hasattr(py_type, "__annotations__") else {}
        props = {}
        required = []
        for f_name, f_type in hints.items():
            props[f_name] = type_to_openapi_type(f_type)
            required.append(f_name)
        return {
            "type": "object",
            "properties": props,
            "required": required
        }
    return {"type": "string"}

def generate_openapi_spec(compiled_routes: list, title: str = "Kosma API", version: str = "1.0.0") -> dict:
    paths: Dict[str, Any] = {}

    for r in compiled_routes:
        if r.path in ("/docs", "/openapi.json"):
            continue

        if r.path not in paths:
            paths[r.path] = {}

        method_key = r.method.lower()
        operation = {
            "summary": f"{r.controller_cls.__name__}.{r.method_name}",
            "responses": {
                str(r.status_code): {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "schema": {"type": "object"}
                        }
                    }
                },
                "422": {
                    "description": "Validation Error",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {"type": "string"},
                                    "errors": {"type": "object"}
                                }
                            }
                        }
                    }
                }
            }
        }

        # Extraer DTO body si existe
        if r.body_param_type:
            operation["requestBody"] = {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": type_to_openapi_type(r.body_param_type)
                    }
                }
            }

        # Extraer path params
        params_spec = []
        for p in r.path_param_names:
            params_spec.append({
                "name": p,
                "in": "path",
                "required": True,
                "schema": {"type": "string"}
            })
        for p, (p_type, default_val) in r.query_params.items():
            params_spec.append({
                "name": p,
                "in": "query",
                "required": default_val is None,
                "schema": type_to_openapi_type(p_type)
            })

        if params_spec:
            operation["parameters"] = params_spec

        paths[r.path][method_key] = operation

    return {
        "openapi": "3.0.0",
        "info": {
            "title": title,
            "version": version,
            "description": "Powered by Kosma Framework (Rust + Python AOT Engine)"
        },
        "paths": paths
    }

def get_swagger_ui_html(openapi_url: str = "/openapi.json", title: str = "Kosma API Docs") -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <style>
        body {{ margin: 0; background: #fafafa; }}
        .topbar {{ display: none !important; }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        SwaggerUIBundle({{
            url: '{openapi_url}',
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
            ],
            layout: "BaseLayout",
            deepLinking: true
        }})
    </script>
</body>
</html>"""
