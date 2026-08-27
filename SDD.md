# Software Design Document (SDD): Velox Framework

**Codename:** Velox  
**Objetivo:** Framework backend para Python de ultra-alto rendimiento con núcleo de red nativo en Rust (PyO3 + Hyper 1.0 + Tokio), compilador AOT de esquemas y ergonomía inspirada en Laravel.

---

## 1. Visión y Objetivos Arquitectónicos

1. **Rendimiento Nativo:** Mover la gestión de sockets TCP, protocolo HTTP, ruteo y bufferización de payloads a Rust sin interacción con el GIL hasta que sea necesario.
2. **Cold Starts < 10ms:** Eliminar la introspección dinámica (`inspect.signature`, `typing.get_type_hints`, Pydantic runtime schema parsing) mediante generación de código estático AOT (`velox build`).
3. **Ergonomía Laravel (DX):** Controladores tipados basados en clases, DTOs declarativos, inyección de dependencias precompilada y CLI potente.
4. **Cero Fragmentación Sync/Async:** Gestión transparente de llamadas asíncronas y síncronas sin congelar el loop de I/O de red.

---

## 2. Diagrama de Arquitectura de Capas

```
┌────────────────────────────────────────────────────────┐
│                   Cliente HTTP / Red                   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                NÚCLEO EN RUST (velox_core)             │
│                                                        │
│   1. Hyper 1.0 + Tokio Runtime (Multi-Threaded)        │
│   2. Router Nativo Radix Trie (matchit)                │
│   3. Extractor Zero-Copy de Body (bytes::Bytes)        │
│   4. Blocking Executor / Worker Pool                   │
└───────────────────────────┬────────────────────────────┘
                            │
               PyO3 Boundary (Python::with_gil)
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│            CAPA DE DESPACHO AOT (Python)               │
│                                                        │
│   1. Dispatchers Planos Autogenerados                  │
│   2. orjson Deserialization directa a DTOs             │
│   3. Contenedor DI Pre-resuelto (Singletons)           │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│           CAPA DE DOMINIO / NEGOCIO (Python)           │
│                                                        │
│   Controladores (@get, @post), DTOs y Servicios        │
└────────────────────────────────────────────────────────┘
```

---

## 3. Especificación de Componentes

### 3.1. Núcleo Rust (`velox_core`)
- **`NativeServer`:** Clase exportada a Python vía PyO3. Gestiona el ciclo de vida del `TcpListener` y el runtime de Tokio.
- **Ruteo:** Utiliza `matchit::Router<RouteHandler>`. Las rutas se registran en Python antes del arranque y se compilan en un árbol Radix de búsqueda $O(k)$ donde $k$ es la longitud del path.
- **Manejo de GIL:** Durante el loop de `accept()` y lectura de paquetes en socket, Tokio corre 100% liberado de GIL (`py.allow_threads`). El GIL se adquiere puntualmente dentro de `spawn_blocking` para ejecutar el despachador Python.

### 3.2. Compilador AOT (`velox.compiler`)
- **CLI:** `velox build`
- **Funcionamiento:**
  1. Escanea las carpetas de controladores.
  2. Parsea el AST y extrae la signatura de métodos y tipos de parámetros (DTOs).
  3. Genera el archivo `_generated_routes.py` que contiene funciones planas de despacho directo.
  4. Elimina la necesidad de inspección dinámica en tiempo de ejecución.

### 3.3. Contenedor de Inyección de Dependencias (`velox.container`)
- Analiza las dependencias de constructores de servicios y controladores en el build.
- Genera el código de cableado (*wiring*) estático para que todas las instancias requeridas estén listas en el inicio de la aplicación.

---

## 4. Especificación de API (Ergonomía Laravel)

### Ejemplo de Controlador y DTO
```python
from dataclasses import dataclass
from velox.controller import Controller
from velox.routing import get, post
from app.services.user_service import UserService

@dataclass
class CreateUserDTO:
    name: str
    email: str
    age: int

class UserController(Controller):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @get("/users/{id}")
    def show(self, id: str):
        return self.user_service.find(id)

    @post("/users")
    def store(self, body: CreateUserDTO):
        user = self.user_service.create(name=body.name, email=body.email, age=body.age)
        return {"status": "created", "user": user}
```

---

## 5. Matriz de Rendimiento y Criterios de Aceptación
1. **Cold Start:** < 10ms en inicio de contenedor.
2. **Latencia p99:** < 2ms para endpoints JSON simples con 100 conexiones concurrentes.
3. **Throughput:** > 40,000 req/sec en máquinas de desarrollo estándar (superando a FastAPI + Uvicorn).
