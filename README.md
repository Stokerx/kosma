# Velox Framework ⚡

**Velox** es un framework de desarrollo backend para Python que une la ergonomía y productividad de **Laravel** con la velocidad extrema y seguridad de memoria de un núcleo nativo en **Rust** (`Hyper 1.0` + `Tokio` + `PyO3`) y un compilador **AOT (Ahead-of-Time)** de rutas y DTOs.

---

## 🎯 Características Principales

* 🚀 **Núcleo de Red en Rust:** Basado en Hyper 1.0 y Tokio. El I/O de red y el matching de rutas en Radix Tree (`matchit`) se ejecutan sin tocar el GIL de Python.
* ⚡ **Compilador AOT (Zero Introspection):** Genera despachadores planos en tiempo de compilación/build, eliminando `inspect.signature` y metaprogramación lenta en runtime.
* 🛠️ **Ergonomía Laravel (DX):** Controladores limpios, Inyección de Dependencias automática, DTOs declarativos y decorators simples (`@get`, `@post`).
* 📦 **Zero-Copy & orjson:** Deserialización y serialización optimizadas a nivel de bytes.
* ⏱️ **Cold Start Ultrarrápido:** Arranque en menos de 10ms, ideal para arquitecturas Serverless y Cloud Run.

---

## 🏗️ Arquitectura

Consulta el [Documento de Diseño de Software (SDD)](./SDD.md) y las [Restricciones Arquitectónicas e Invariantes](./AI_GUARDRAILS.md).

---

## 🚀 Inicio Rápido

```python
from dataclasses import dataclass
from velox import VeloxApp, Controller, get, post

@dataclass
class CreateUserDTO:
    name: str
    email: str
    age: int

class UserController(Controller):
    @get("/users/{id}")
    def show(self, id: str):
        return {"id": id, "name": "Alice"}

    @post("/users")
    def store(self, body: CreateUserDTO):
        return {"status": "created", "data": body}

app = VeloxApp()
app.register(UserController)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
```

---

## 🧪 Pruebas y Compilación

```bash
# Compilar extensiones nativas
maturin develop

# Ejecutar tests
pytest tests/
```
