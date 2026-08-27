from velox.controller import Controller
from velox.routing import get, post
from velox.responses import JsonResponse
from examples.basic_app.services.user_service import UserService
from examples.basic_app.models import CreateUserDTO

class UserController(Controller):
    def __init__(self, service: UserService):
        self.service = service

    @get("/users")
    def index(self):
        """Lista todos los usuarios (Estilo Laravel)."""
        return {"users": self.service.all()}

    @get("/users/{id}")
    def show(self, id: str):
        """Obtiene un usuario por su ID."""
        user = self.service.find(id)
        if not user:
            return (404, {"error": f"User with id {id} not found"})
        return {"user": user}

    @post("/users")
    def store(self, body: CreateUserDTO):
        """Crea un usuario a partir del DTO validado AOT."""
        created = self.service.create(name=body.name, email=body.email, role=body.role)
        return (201, {"status": "created", "user": created})
