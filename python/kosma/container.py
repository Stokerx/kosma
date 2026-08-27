import inspect
from typing import Any, Dict, Type, TypeVar, get_type_hints

T = TypeVar("T")

class Container:
    """
    Contenedor de Inyección de Dependencias (DI) estilo Laravel.
    Pre-resuelve el grafo de dependencias en el arranque o build time.
    """

    def __init__(self):
        self._instances: Dict[Type, Any] = {}
        self._bindings: Dict[Type, Type] = {}
        self._singletons: set[Type] = set()

    def bind(self, abstract: Type[T], concrete: Type[T]):
        """Vincula una interfaz/tipo abstracto a una implementación concreta."""
        self._bindings[abstract] = concrete

    def singleton(self, abstract: Type[T], concrete: Type[T] = None):
        """Registra un singleton en el contenedor."""
        target = concrete or abstract
        self._bindings[abstract] = target
        self._singletons.add(abstract)

    def instance(self, abstract: Type[T], instance_obj: T):
        """Registra una instancia existente en el contenedor."""
        self._instances[abstract] = instance_obj

    def resolve(self, target_type: Type[T]) -> T:
        """
        Resuelve una clase instanciando recursivamente sus dependencias de constructor.
        """
        # Si ya existe como instancia registrada/singleton resuelto
        if target_type in self._instances:
            return self._instances[target_type]

        # Verificar si hay binding registrado
        concrete = self._bindings.get(target_type, target_type)

        # Inspeccionar parámetros del constructor __init__
        if not hasattr(concrete, "__init__"):
            inst = concrete()
            if target_type in self._singletons:
                self._instances[target_type] = inst
            return inst

        init_sig = inspect.signature(concrete.__init__)
        hints = get_type_hints(concrete.__init__) if hasattr(concrete.__init__, "__annotations__") else {}

        kwargs = {}
        for param_name, param in init_sig.parameters.items():
            if param_name == "self":
                continue
            param_type = hints.get(param_name)
            if param_type and param_type != Any:
                # Recursión para resolver sub-dependencias
                kwargs[param_name] = self.resolve(param_type)
            elif param.default is not inspect.Parameter.empty:
                kwargs[param_name] = param.default

        inst = concrete(**kwargs)
        if target_type in self._singletons:
            self._instances[target_type] = inst

        return inst
