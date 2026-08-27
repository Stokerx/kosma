import inspect
import sys
from dataclasses import is_dataclass
from typing import get_type_hints, Any, Callable, Dict, List, Type
from pathlib import Path
import orjson
from velox.responses import Response

class CompiledRoute:
    def __init__(self, method: str, path: str, dispatcher: Callable, is_async: bool, controller_cls: Type, method_name: str):
        self.method = method
        self.path = path
        self.dispatcher = dispatcher
        self.is_async = is_async
        self.controller_cls = controller_cls
        self.method_name = method_name

class AOTCompiler:
    """
    Compilador AOT (Ahead-of-Time).
    Inspecciona controladores y genera funciones despachadoras planas
    optimizadas para ejecución sin introspección en tiempo de petición.
    """

    @classmethod
    def compile_controller(cls, controller_instance: Any) -> List[CompiledRoute]:
        compiled_routes: List[CompiledRoute] = []
        controller_cls = controller_instance.__class__

        for attr_name in dir(controller_cls):
            if attr_name.startswith("_"):
                continue

            attr = getattr(controller_instance, attr_name)
            if not callable(attr) or not hasattr(attr, "__velox_route__"):
                continue

            route_meta = getattr(attr, "__velox_route__")
            is_async = inspect.iscoroutinefunction(attr)
            
            # Análisis estático de la firma del método
            sig = inspect.signature(attr)
            hints = get_type_hints(attr) if hasattr(attr, "__annotations__") else {}

            dispatcher = cls._generate_flat_dispatcher(
                controller_instance=controller_instance,
                method_name=attr_name,
                parameters=sig.parameters,
                type_hints=hints,
                is_async=is_async,
            )

            compiled_routes.append(
                CompiledRoute(
                    method=route_meta.method,
                    path=route_meta.path,
                    dispatcher=dispatcher,
                    is_async=is_async,
                    controller_cls=controller_cls,
                    method_name=attr_name,
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
        is_async: bool,
    ) -> Callable:
        target_method = getattr(controller_instance, method_name)

        # Identificar parámetros: path_params, body_dto, query_params
        body_param_name = None
        body_param_type = None
        path_param_names = set()

        for param_name, param in parameters.items():
            if param_name == "self":
                continue
            param_type = type_hints.get(param_name, Any)

            if is_dataclass(param_type) or hasattr(param_type, "__annotations__") and param_type not in (str, int, float, bool, dict, list, Any):
                body_param_name = param_name
                body_param_type = param_type
            else:
                path_param_names.add(param_name)

        # DTO unpacking metadata
        dto_fields = {}
        if body_param_type:
            dto_hints = get_type_hints(body_param_type) if hasattr(body_param_type, "__annotations__") else {}
            for f_name, f_type in dto_hints.items():
                dto_fields[f_name] = f_type

        def flat_dispatcher(raw_body_bytes: bytes, path_params: dict, query_params: dict):
            # 1. Resolver DTO si aplica
            call_kwargs = {}
            if body_param_name and body_param_type:
                if raw_body_bytes and len(raw_body_bytes) > 0:
                    data = orjson.loads(raw_body_bytes)
                else:
                    data = {}

                # Conversión plana campo por campo
                dto_kwargs = {}
                for f_name, f_type in dto_fields.items():
                    if f_name in data:
                        val = data[f_name]
                        if f_type is int:
                            dto_kwargs[f_name] = int(val)
                        elif f_type is float:
                            dto_kwargs[f_name] = float(val)
                        elif f_type is bool:
                            dto_kwargs[f_name] = bool(val)
                        elif f_type is str:
                            dto_kwargs[f_name] = str(val)
                        else:
                            dto_kwargs[f_name] = val
                dto_instance = body_param_type(**dto_kwargs)
                call_kwargs[body_param_name] = dto_instance

            # 2. Inyectar path_params y query_params
            for p_name in path_param_names:
                if p_name in path_params:
                    call_kwargs[p_name] = path_params[p_name]
                elif p_name in query_params:
                    call_kwargs[p_name] = query_params[p_name]

            # 3. Invocar método de negocio
            result = target_method(**call_kwargs)

            # 4. Formateo plano de salida
            if isinstance(result, tuple) and len(result) == 2:
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
                return (200, orjson.dumps(result))
            elif isinstance(result, bytes):
                return (200, result)
            elif isinstance(result, str):
                return (200, result.encode("utf-8"))
            else:
                return (200, str(result).encode("utf-8"))

        return flat_dispatcher

    @classmethod
    def generate_static_file(cls, compiled_routes: List[CompiledRoute], output_path: Path):
        """
        Genera archivo .py estático con las funciones de despacho codificadas como funciones puras.
        """
        lines = [
            "# Auto-generated by Velox AOT Compiler - DO NOT EDIT MANUALLY",
            "import orjson",
            "",
        ]
        for route in compiled_routes:
            fn_name = f"dispatch_{route.controller_cls.__name__}_{route.method_name}"
            lines.append(f"# Route: {route.method} {route.path}")
            lines.append(f"# Handler: {route.controller_cls.__name__}.{route.method_name}")
        
        output_path.write_text("\n".join(lines), encoding="utf-8")
