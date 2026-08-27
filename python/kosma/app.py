from typing import List, Type, Optional, Callable, Dict
from kosma.container import Container
from kosma.controller import Controller
from kosma.compiler import AOTCompiler, CompiledRoute
from kosma.openapi import generate_openapi_spec, get_swagger_ui_html
import orjson

try:
    from kosma.kosma_core import NativeServer
except ImportError:
    NativeServer = None

class KosmaApp:
    """
    Aplicación principal de Kosma.
    Orquesta controladores, DI Container, OpenAPI Docs, CORS y el motor en Rust.
    """

    def __init__(
        self,
        title: str = "Kosma API",
        version: str = "1.0.0",
        docs_url: Optional[str] = "/docs",
        openapi_url: Optional[str] = "/openapi.json",
        container: Optional[Container] = None,
    ):
        self.title = title
        self.version = version
        self.docs_url = docs_url
        self.openapi_url = openapi_url
        self.container = container or Container()
        self.controllers: List[Type[Controller]] = []
        self.compiled_routes: List[CompiledRoute] = []
        self._server = None
        self._cors_settings: Optional[Dict[str, list]] = None

    def enable_cors(
        self,
        allow_origins: Optional[List[str]] = None,
        allow_methods: Optional[List[str]] = None,
        allow_headers: Optional[List[str]] = None,
    ):
        """Habilita y configura CORS en el núcleo de Rust."""
        self._cors_settings = {
            "allow_origins": allow_origins or ["*"],
            "allow_methods": allow_methods or ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            "allow_headers": allow_headers or ["Content-Type", "Authorization", "X-Requested-With"],
        }
        return self

    def register(self, controller_cls: Type[Controller]):
        """Registra un controlador en la aplicación."""
        self.controllers.append(controller_cls)
        return self

    def compile(self):
        """
        Paso AOT: Resuelve dependencias, compila despachadores planos
        y genera el esquema OpenAPI estático.
        """
        self.compiled_routes.clear()
        for ctrl_cls in self.controllers:
            instance = self.container.resolve(ctrl_cls)
            routes = AOTCompiler.compile_controller(instance)
            self.compiled_routes.extend(routes)

        # Autogenerar OpenAPI Spec y Swagger UI
        if self.openapi_url:
            spec_dict = generate_openapi_spec(self.compiled_routes, title=self.title, version=self.version)
            spec_bytes = orjson.dumps(spec_dict)
            self.compiled_routes.append(
                CompiledRoute(
                    method="GET",
                    path=self.openapi_url,
                    dispatcher=lambda body, p, q: (200, spec_bytes),
                    is_async=False,
                    controller_cls=self.__class__,
                    method_name="openapi_schema",
                )
            )

        if self.docs_url and self.openapi_url:
            swagger_html = get_swagger_ui_html(openapi_url=self.openapi_url, title=f"{self.title} - Swagger UI")
            self.compiled_routes.append(
                CompiledRoute(
                    method="GET",
                    path=self.docs_url,
                    dispatcher=lambda body, p, q: (200, "text/html", swagger_html.encode("utf-8")),
                    is_async=False,
                    controller_cls=self.__class__,
                    method_name="swagger_ui",
                )
            )

        # Registrar en el servidor nativo de Rust
        if NativeServer is not None:
            self._server = NativeServer()
            if self._cors_settings:
                self._server.set_cors(
                    self._cors_settings["allow_origins"],
                    self._cors_settings["allow_methods"],
                    self._cors_settings["allow_headers"],
                )
            for r in self.compiled_routes:
                self._server.add_route(r.method, r.path, r.dispatcher, r.is_async)
        return self

    def run(self, host: str = "127.0.0.1", port: int = 8000, workers: Optional[int] = None):
        """
        Inicia el servidor HTTP nativo en Rust con Hyper 1.0 y Tokio.
        """
        if self._server is None:
            self.compile()

        if self._server is None:
            raise RuntimeError(
                "No se pudo inicializar kosma_core. Asegúrate de compilar las extensiones con 'maturin develop'."
            )

        print(f"[*] Registradas {len(self.compiled_routes)} rutas compiladas.")
        for r in self.compiled_routes:
            print(f"    -> [{r.method}] {r.path} => {r.controller_cls.__name__}.{r.method_name}")

        if self.docs_url:
            print(f"📚 Documentación interactiva en http://{host}:{port}{self.docs_url}")

        self._server.serve(host, port, workers)
