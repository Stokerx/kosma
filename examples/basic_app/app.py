import sys
from pathlib import Path

# Añadir raíz al sys.path para desarrollo local
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "python"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from velox import VeloxApp, Container
from examples.basic_app.controllers.user_controller import UserController
from examples.basic_app.services.user_service import UserService

def create_app() -> VeloxApp:
    container = Container()
    # Registrar UserService como Singleton
    container.singleton(UserService)

    app = VeloxApp(container=container)
    app.register(UserController)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=8000)
