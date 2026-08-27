import inspect
import sys
from dataclasses import is_dataclass
from typing import get_type_hints, Any, Callable, Dict, List, Type, Tuple, Optional
from pathlib import Path
import orjson
from kosma.responses import Response

class CompiledRoute:
    def __init__(
        self,
        method: str,
        path: str,
        dispatcher: Callable,
        is_async: bool,
        controller_cls: Type,
        method_name: str,
        status_code: int = 200,
        body_param_type: Optional[Type] = None,
        path_param_names: Optional[List[str]] = None,
        query_params: Optional[Dict[str, Tuple[Type, Any]]] = None,
    ):
        self.method = method
        self.path = path
        self.dispatcher = dispatcher
        self.is_async = is_async
        self.controller_cls = controller_cls
        self.method_name = method_name
        self.status_code = status_code
        self.body_param_type = body_param_type
        self.path_param_names = path_param_names or []
        self.query_params = query_params or {}

class AOTCompiler:
    """
    Compilador AOT (Ahead-of-Time).
    Inspecciona controladores y genera funciones despachadoras planas
    optimizadas con validación 422 sin introspección en tiempo de petición.
    """

    @classmethod
    def compile_controller(cls, controller_instance: Any) -> List[CompiledRoute]:
        compiled_routes: List[CompiledRoute] = []
        controller_cls = controller_instance.__class__

        for attr_name in dir(controller_cls):
            if attr_name.startswith("_"):
                continue

            attr = getattr(controller_instance, attr_name)
            if not callable(attr) or not hasattr(attr, "__kosma_route__"):
                continue

            route_meta = getattr(attr, "__kosma_route__")
            is_async = inspect.iscoroutinefunction(attr)
            
            # Análisis estático en tiempo de build
            sig = inspect.signature(attr)
            hints = get_type_hints(attr) if hasattr(attr, "__annotations__") else {}

            dispatcher, body_type, path_names, q_params = cls._generate_flat_dispatcher(
                controller_instance=controller_instance,
                method_name=attr_name,
                parameters=sig.parameters,
                type_hints=hints,
                default_status=route_meta.status_code,
            )

            compiled_routes.append(
                CompiledRoute(
                    method=route_meta.method,
                    path=route_meta.path,
                    dispatcher=dispatcher,
                    is_async=is_async,
                    controller_cls=controller_cls,
                    method_name=attr_name,
                    status_code=route_meta.status_code,
                    body_param_type=body_type,
                    path_param_names=list(path_names),
                    query_params=q_params,
                )
            )

        return compiled_routes

    @classmethod
    def _generate_flat_dispatcher(
        cls,
        controller_instance: Any,
        method_name: str,
        parameters: Dict[str, inspect.Parameter],
        type_hints: Dict[str, Any],
        default_status: int,
    ) -> Tuple[Callable, Optional[Type], List[str], Dict[str, Tuple[Type, Any]]]:
        target_method = getattr(controller_instance, method_name)

        body_param_name = None
        body_param_type = None
        path_param_names = []
        query_param_specs = {}

        for param_name, param in parameters.items():
            if param_name == "self":
                continue
            param_type = type_hints.get(param_name, Any)

            if is_dataclass(param_type) or (hasattr(param_type, "__annotations__") and param_type not in (str, int, float, bool, dict, list, Any)):
                body_param_name = param_name
                body_param_type = param_type
            elif param.default is not inspect.Parameter.empty:
                # Query param con default
                query_param_specs[param_name] = (param_type, param.default)
            else:
                # Path param obligatorio
                path_param_names.append(param_name)

        # DTO field metadata & defaults
        dto_fields: Dict[str, Tuple[Type, bool, Any]] = {}
        if body_param_type:
            dto_hints = get_type_hints(body_param_type) if hasattr(body_param_type, "__annotations__") else {}
            for f_name, f_type in dto_hints.items():
                has_default = hasattr(body_param_type, f_name)
                default_val = getattr(body_param_type, f_name, None) if has_default else None
                dto_fields[f_name] = (f_type, has_default, default_val)

        def flat_dispatcher(raw_body_bytes: bytes, path_params: dict, query_params: dict):
            call_kwargs = {}
            validation_errors = {}

            # 1. Validación y Deserialización AOT de DTOs
            if body_param_name and body_param_type:
                if not raw_body_bytes or len(raw_body_bytes) == 0:
                    data = {}
                else:
                    try:
                        data = orjson.loads(raw_body_bytes)
                    except Exception:
                        return (422, orjson.dumps({"message": "Malformed JSON payload"}))

                if not isinstance(data, dict):
                    return (422, orjson.dumps({"message": "JSON body must be an object"}))

                dto_kwargs = {}
                for f_name, (f_type, has_def, def_val) in dto_fields.items():
                    if f_name not in data:
                        if not has_def:
                            validation_errors[f_name] = "Field is required"
                        else:
                            dto_kwargs[f_name] = def_val
                    else:
                        val = data[f_name]
                        try:
                            if f_type is int:
                                dto_kwargs[f_name] = int(val)
                            elif f_type is float:
                                dto_kwargs[f_name] = float(val)
                            elif f_type is bool:
                                if isinstance(val, bool):
                                    dto_kwargs[f_name] = val
                                elif isinstance(val, str):
                                    dto_kwargs[f_name] = val.lower() in ("true", "1", "yes")
                                else:
                                    dto_kwargs[f_name] = bool(val)
                            elif f_type is str:
                                dto_kwargs[f_name] = str(val)
                            else:
                                dto_kwargs[f_name] = val
                        except (ValueError, TypeError):
                            validation_errors[f_name] = f"Invalid type, expected {getattr(f_type, '__name__', str(f_type))}"

                if validation_errors:
                    return (422, orjson.dumps({
                        "message": "Validation failed",
                        "errors": validation_errors
                    }))

                dto_kwargs_clean = {k: v for k, v in dto_kwargs.items() if k in dto_fields}
                dto_instance = body_param_type(**dto_kwargs_clean)
                call_kwargs[body_param_name] = dto_instance

            # 2. Inyección de Path Params
            for p_name in path_param_names:
                if p_name in path_params:
                    call_kwargs[p_name] = path_params[p_name]
                elif p_name in query_params:
                    call_kwargs[p_name] = query_params[p_name]

            # 3. Inyección de Query Params con casting
            for q_name, (q_type, q_default) in query_param_specs.items():
                if q_name in query_params:
                    raw_val = query_params[q_name]
                    try:
                        if q_type is int:
                            call_kwargs[q_name] = int(raw_val)
                        elif q_type is float:
                            call_kwargs[q_name] = float(raw_val)
                        elif q_type is bool:
                            call_kwargs[q_name] = raw_val.lower() in ("true", "1", "yes")
                        elif q_type is str:
                            call_kwargs[q_name] = str(raw_val)
                        else:
                            call_kwargs[q_name] = raw_val
                    except (ValueError, TypeError):
                        call_kwargs[q_name] = q_default
                else:
                    call_kwargs[q_name] = q_default

            # 4. Invocar método de negocio
            result = target_method(**call_kwargs)

            # 5. Formateo de respuesta
            if isinstance(result, tuple) and len(result) == 3:
                return result
            elif isinstance(result, tuple) and len(result) == 2:
                status, content = result
                if isinstance(content, (dict, list)):
                    return (status, orjson.dumps(content))
                elif isinstance(content, bytes):
                    return (status, content)
                elif isinstance(content, str):
                    return (status, content.encode("utf-8"))
                return (status, str(content).encode("utf-8"))
            elif isinstance(result, Response):
                return result.to_raw()
            elif isinstance(result, (dict, list)):
                return (default_status, orjson.dumps(result))
            elif isinstance(result, bytes):
                return (default_status, result)
            elif isinstance(result, str):
                return (default_status, result.encode("utf-8"))
            else:
                return (default_status, str(result).encode("utf-8"))

        return flat_dispatcher, body_param_type, path_param_names, query_param_specs
