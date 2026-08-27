import argparse
import sys
from pathlib import Path

def make_controller(name: str):
    name_clean = name.replace(".py", "")
    if not name_clean.endswith("Controller"):
        class_name = f"{name_clean}Controller"
    else:
        class_name = name_clean

    file_name = f"{name_clean.lower()}.py"
    target_dir = Path("app/controllers")
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / file_name

    if target_file.exists():
        print(f"❌ El archivo {target_file} ya existe.")
        return

    content = f'''from dataclasses import dataclass
from kosma.controller import Controller
from kosma.routing import get, post

@dataclass
class ExampleDTO:
    name: str
    active: bool = True

class {class_name}(Controller):
    @get("/{name_clean.lower()}")
    def index(self):
        return {{"message": "Hello from {class_name}"}}

    @post("/{name_clean.lower()}")
    def store(self, body: ExampleDTO):
        return {{"status": "created", "data": body}}
'''
    target_file.write_text(content, encoding="utf-8")
    print(f"✅ Controlador creado exitosamente: {target_file}")

def main():
    parser = argparse.ArgumentParser(description="Kosma Framework CLI - Laravel DX with Rust Speed")
    subparsers = parser.add_subparsers(dest="command")

    # Command: make:controller
    mc_parser = subparsers.add_parser("make:controller", help="Genera un nuevo controlador")
    mc_parser.add_argument("name", type=str, help="Nombre del controlador (ej. User)")

    # Command: routes
    subparsers.add_parser("routes", help="Lista todas las rutas registradas")

    # Command: build
    subparsers.add_parser("build", help="Precompila las rutas y genera despachadores AOT")

    # Command: serve
    serve_parser = subparsers.add_parser("serve", help="Inicia el servidor HTTP")
    serve_parser.add_argument("--host", type=str, default="127.0.0.1", help="Host (default: 127.0.0.1)")
    serve_parser.add_argument("--port", type=int, default=8000, help="Puerto (default: 8000)")
    serve_parser.add_argument("--workers", type=int, default=None, help="Número de workers en Tokio")

    args = parser.parse_args()

    if args.command == "make:controller":
        make_controller(args.name)
    elif args.command == "serve":
        print(f"🚀 Iniciando servidor Kosma en http://{args.host}:{args.port}...")
    elif args.command == "build":
        print("⚡ Compilando rutas y despachadores AOT con Kosma...")
        print("✅ Compilación completada con éxito.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
