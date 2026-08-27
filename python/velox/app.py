from typing import List, Type, Optional, Callable
from velox.container import Container
from velox.controller import Controller
from velox.compiler import AOTCompiler, CompiledRoute

try:
    from velox.velox_core import NativeServer
except ImportError:
    # Fallback si el binario nativo no está compilado aún
    NativeServer = None

class VeloxApp:
    """
    Aplicación principal de Velox.
    Orquesta los controladores, inyección de dependencias y el motor en Rust.
    """

    def __init__(self, container: Optional[Container] = None):
        self.container = container or Container()
        self.controllers: List[Type[Controller]] = []
        self.compiled_routes: List[CompiledRoute] = []
        self._server = None

    def register(self, controller_cls: Type[Controller]):
        """Registra un controlador en la aplicación."""
        self.controllers.append(controller_cls)
        return self

    def compile(self):
        """
        Paso AOT: Resuelve dependencias y compila todos los despachadores planos.
        """
        self.compiled_routes.clear()
        for ctrl_cls in self.controllers:
            # 1. Resolver instancia usando el contenedor DI
            instance = self.container.resolve(ctrl_cls)
            # 2. Compilar rutas a despachadores planos
            routes = AOTCompiler.compile_controller(instance)
            self.compiled_routes.extend(routes)

        # 3. Registrar rutas en el servidor nativo de Rust
        if NativeServer is not None:
            self._server = NativeServer()
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
                "No se pudo inicializar velox_core. Asegúrate de compilar las extensiones con 'maturin develop'."
            )

        print(f"[*] Registradas {len(self.compiled_routes)} rutas compiladas.")
        for r in self.compiled_routes:
            print(f"    -> [{r.method}] {r.path} => {r.controller_cls.__name__}.{r.method_name}")

        self._server.serve(host, port, workers)
