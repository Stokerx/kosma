# Software Design Document (SDD): Kosma Framework

**Name:** Kosma  
**Objetivo:** Framework backend para Python de ultra-alto rendimiento con núcleo de red nativo en Rust (PyO3 + Hyper 1.0 + Tokio), compilador AOT de esquemas, soporte CORS integrado, documentación Swagger UI nativa y ergonomía inspirada en Laravel.

---

## 1. Visión y Objetivos Arquitectónicos

1. **Rendimiento Nativo:** Mover la gestión de sockets TCP, protocolo HTTP, ruteo y preflight CORS a Rust sin interacción con el GIL hasta que sea necesario.
2. **Cold Starts < 1ms:** Eliminar la introspección dinámica (`inspect.signature`, `typing.get_type_hints`) mediante generación de código estático AOT.
3. **Ergonomía Laravel (DX):** Controladores tipados basados en clases, DTOs declarativos con validación 422 automática, inyección de dependencias precompilada y CLI potente.
4. **Zero-CPU OpenAPI Documentation:** Autogeneración del esquema OpenAPI y Swagger UI en el build, servido sin cómputo en runtime.

---

## 2. Diagrama de Arquitectura de Capas

```
┌────────────────────────────────────────────────────────┐
│                   Cliente HTTP / Red                   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                NÚCLEO EN RUST (kosma_core)             │
│                                                        │
│   1. Hyper 1.0 + Tokio Runtime (Multi-Threaded)        │
│   2. Router Nativo Radix Trie (matchit)                │
│   3. CORS Engine & Preflight (OPTIONS 204 No Content)  │
│   4. Extractor Zero-Copy de Body (bytes::Bytes)        │
│   5. Blocking Executor / Worker Pool                   │
└───────────────────────────┬────────────────────────────┘
                            │
               PyO3 Boundary (Python::with_gil)
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│            CAPA DE DESPACHO AOT (Python)               │
│                                                        │
│   1. Dispatchers Planos con Validación 422             │
│   2. orjson Deserialization directa a DTOs             │
│   3. Contenedor DI Pre-resuelto (Singletons)           │
│   4. OpenAPI 3.0 & Swagger UI Static Handler           │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│           CAPA DE DOMINIO / NEGOCIO (Python)           │
│                                                        │
│   Controladores (@get, @post), DTOs y Servicios        │
└────────────────────────────────────────────────────────┘
```
