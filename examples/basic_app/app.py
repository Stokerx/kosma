import sys
from pathlib import Path

# Añadir raíz al sys.path para desarrollo local
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "python"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from kosma import KosmaApp, Container
from examples.basic_app.controllers.user_controller import UserController
from examples.basic_app.services.user_service import UserService

def create_app() -> KosmaApp:
    container = Container()
    container.singleton(UserService)

    app = KosmaApp(
        title="Kosma Demo Store API",
        version="1.0.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
        container=container,
    )
    app.enable_cors(allow_origins=["*"])
    app.register(UserController)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=8000)
