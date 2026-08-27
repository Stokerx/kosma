# Kosma Framework ⚡

> **Laravel Developer Experience (DX) + Rust Native Performance + Zero-Reflection AOT Engine for Python.**

[![CI](https://github.com/Stokerx/Kosma/actions/workflows/ci.yml/badge.svg)](https://github.com/Stokerx/Kosma/actions)
[![PyPI version](https://img.shields.io/pypi/v/kosma.svg)](https://pypi.org/project/kosma/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by uv](https://img.shields.io/badge/Powered%20by-uv-blueviolet)](https://github.com/astral-sh/uv)

**Kosma** es un framework backend para Python de ultra-alto rendimiento que resuelve las limitaciones históricas de CPython (cold starts, overhead del GIL, fragmentación sync/async e introspección de runtime) delegando la red a un motor nativo en **Rust (Hyper 1.0 + Tokio)** y utilizando compilación **AOT (Ahead-of-Time)** para validar DTOs y generar documentación OpenAPI interactiva.

---

## ⚡ ¿Por qué Kosma?

| Característica | FastAPI + Uvicorn | Django | Litestar | **Kosma** |
| :--- | :--- | :--- | :--- | :--- |
| **Motor de Red** | Python (`asyncio`) | Python (`WSGI/ASGI`) | Python (`asyncio`) | **Rust (`Hyper 1.0` + `Tokio`)** |
| **Introspección** | Runtime (`inspect` en cada req) | Runtime | Runtime (`msgspec`) | **AOT Compilado (Zero-Inspect en req)** |
| **Cold Start** | ~300ms – 1.2s | ~500ms – 2.5s | ~250ms – 600ms | **< 1ms (Instantáneo)** |
| **Ergonomía** | Funciones + `Depends()` | Monolito | Decoradores | **Laravel-like (Controllers, DTOs, DI)** |
| **CORS / Preflight**| Python Middleware | Python Middleware | Python Middleware | **Rust Engine Nativo (Zero GIL)** |
| **Docs Integrados** | Swagger en Runtime | No integrado | Swagger en Runtime | **Swagger UI AOT Zero-CPU** |

---

## 🚀 Inicio Rápido en 30 Segundos

### 1. Instalación con `uv` o `pip`
```bash
# Con uv (Recomendado)
uv add kosma

# O con pip
pip install kosma
```

### 2. Escribe tu primera API (`app.py`)
```python
from dataclasses import dataclass
from kosma import KosmaApp, Controller, get, post

@dataclass
class CreateUserDTO:
    name: str
    email: str
    age: int

class UserController(Controller):
    @get("/users/{id}")
    def show(self, id: str):
        """Devuelve un usuario por su ID."""
        return {"id": id, "name": "Ada Lovelace"}

    @post("/users", status_code=201)
    def store(self, body: CreateUserDTO):
        """Valida el DTO en AOT (422 automático si falla)."""
        return {"status": "created", "user": body}

app = KosmaApp(title="My Store API")
app.enable_cors(allow_origins=["*"])
app.register(UserController)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
```

### 3. Ejecutar
```bash
python app.py
```
Abre en tu navegador `http://127.0.0.1:8000/docs` para ver el **Swagger UI interactivo**.

---

## 🛡️ Validación Automática HTTP 422 (Zero Introspección)

Si un cliente envía datos inválidos o incompletos:
```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob", "age": "invalid_number"}'
```

Kosma responde instantáneamente con un código `422 Unprocessable Entity`:
```json
{
  "message": "Validation failed",
  "errors": {
    "email": "Field is required",
    "age": "Invalid type, expected int"
  }
}
```

---

## 🏛️ Arquitectura & Documentación

* 📘 [Software Design Document (SDD)](./SDD.md)
* 🚫 [AI & Architectural Guardrails](./AI_GUARDRAILS.md)
* 🤝 [Guía de Contribución con uv](./CONTRIBUTING.md)

---

## 📄 Licencia

Licenciado bajo la [Licencia MIT](./LICENSE).
