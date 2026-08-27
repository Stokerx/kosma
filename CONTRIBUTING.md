# Contributing to Kosma ⚡

Thank you for your interest in contributing to **Kosma**!

---

## 🛠️ Development Setup with `uv` (Astral)

Kosma standardizes on **[Astral uv](https://github.com/astral-sh/uv)** for fast Python packaging, environment management, and dependency locking.

### 1. Clone the repository
```bash
git clone git@github.com:Stokerx/Kosma.git
cd Kosma
```

### 2. Install dependencies with `uv`
```bash
# uv creates the virtual environment and installs all dependencies in lockstep
uv sync
```

### 3. Build the native Rust extension
```bash
uv run maturin develop
```

### 4. Run the test suite
```bash
uv run pytest tests/ -v
```

---

## 🏛️ Architectural Guardrails (Must Read Before Submitting PRs)

Please review [`AI_GUARDRAILS.md`](./AI_GUARDRAILS.md) and [`SDD.md`](./SDD.md).
1. **Zero Runtime Introspection:** Do not use `inspect.signature` or `typing.get_type_hints` inside request handlers.
2. **Do Not Block Tokio Worker Threads:** Always run Python execution inside `spawn_blocking` or dedicated worker threads.
3. **Zero-Copy First:** Avoid unnecessary buffer cloning between Rust and Python.
