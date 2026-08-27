# AI Guardrails & Architectural Invariants: Kosma Framework

Este documento establece las reglas estrictas de desarrollo y límites técnicos inviolables para cualquier modificación, extensión o generación de código en este repositorio.

---

## 🚫 Lo que la IA / Desarrollador NO DEBE HACER (Reglas Inviolables)

### 1. Prohibido el uso de `inspect` o `typing.get_type_hints` en Runtime
* **Por qué:** La introspección dinámica es la principal causa de la degradación de rendimiento y cold starts lentos en frameworks como FastAPI o Pydantic v1.
* **Regla:** Ningún endpoint, middleware o deserializador debe invocar `inspect.signature()`, `inspect.getmembers()` o `typing.get_type_hints()` durante el ciclo de vida de una petición (`handle_request`).
* **Solución requerida:** Toda extracción de metadatos debe ocurrir exclusivamente durante la fase de compilación AOT (`kosma build` o `app.compile()`), generando funciones despachadoras planas.

### 2. Prohibido envolver la arquitectura ASGI tradicional
* **Por qué:** ASGI introduce múltiples capas de coroutines intermediarias, tuplas de scope en memoria y overhead de serialización en el event loop de CPython.
* **Regla:** El servidor de red debe residir 100% en Rust sobre **Hyper 1.0** y **Tokio**.
* **Solución requerida:** El paso a Python se realiza únicamente cuando la ruta coincide, pasando punteros de memoria (`Bytes`/`PyBytes`) de manera directa al despachador compilado.

### 3. Prohibido bloquear los Workers de Tokio con el GIL
* **Por qué:** Si un hilo de Tokio adquiere el GIL para ejecutar código Python bloqueante o síncrono, se detiene el procesamiento de paquetes de red de todas las demás conexiones en ese hilo.
* **Regla:** Nunca ejecutar llamadas Python bloqueantes directamente en las tareas principales de Tokio.
* **Solución requerida:** Usar `tokio::task::spawn_blocking` o un threadpool dedicado para interactuar con Python mediante `Python::with_gil`.

### 4. Prohibido clonar buffers de red innecesariamente (Zero-Copy)
* **Por qué:** La copia de memoria en peticiones grandes (JSON, subida de archivos) satura el ancho de banda del bus de memoria y dispara el Garbage Collector de Python.
* **Regla:** Mantener los buffers del socket como `bytes::Bytes` en Rust y exponerlos a Python como vistas de memoria (`PyBytes` o slices) solo cuando el handler lo requiere.

### 5. Prohibido exponer fontanería de bajo nivel a los Controladores (DX First)
* **Por qué:** La complejidad innecesaria (exponer sockets, raw scopes, headers crudos) arruina la experiencia de desarrollo (DX).
* **Regla:** El usuario final no debe ver `request.scope` ni lidiar con streams asíncronos para tareas CRUD cotidianas.
* **Solución requerida:** Controladores estilo Laravel: clases limpias, métodos decorados (`@post("/users")`), DTOs basados en `@dataclass` o tipos nativos, e inyección de servicios limpia.

### 6. Prohibido dependencias pesadas en tiempo de ejecución
* **Por qué:** Paquetes gigantescos aumentan el tamaño de imagen de Docker y el tiempo de arranque.
* **Regla:** El framework en tiempo de ejecución solo depende del binario nativo (`kosma_core`), `orjson` para serialización de alta velocidad y la librería estándar de Python.
