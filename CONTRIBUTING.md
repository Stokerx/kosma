# Contributing to Kosma ⚡

Thank you for your interest in contributing to **Kosma**! We welcome contributions of all kinds: bug fixes, new features, documentation improvements, and benchmarks.

---

## 🛠️ Development Setup

Kosma requires:
* **Python 3.10+** (Tested on Python 3.10, 3.11, 3.12, 3.13)
* **Rust 1.75+** & Cargo
* **Maturin**

### 1. Clone the repository
```bash
git clone https://github.com/your-org/kosma.git
cd kosma
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -U pip maturin orjson pytest pytest-asyncio
```

### 3. Build the native Rust extension
```bash
maturin develop
```

### 4. Run the test suite
```bash
pytest tests/ -v
```

---

## 🏛️ Architectural Guardrails (Must Read Before Submitting PRs)

Please review [`AI_GUARDRAILS.md`](./AI_GUARDRAILS.md) and [`SDD.md`](./SDD.md).
1. **Zero Runtime Introspection:** Do not use `inspect.signature` or `typing.get_type_hints` inside request handlers.
2. **Do Not Block Tokio Worker Threads:** Always run Python execution inside `spawn_blocking` or dedicated worker threads.
3. **Zero-Copy First:** Avoid unnecessary buffer cloning between Rust and Python.
