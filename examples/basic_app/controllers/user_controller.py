from kosma.controller import Controller
from kosma.routing import get, post
from kosma.responses import JsonResponse
from examples.basic_app.services.user_service import UserService
from examples.basic_app.models import CreateUserDTO

class UserController(Controller):
    def __init__(self, service: UserService):
        self.service = service

    @get("/users")
    def index(self, page: int = 1, limit: int = 10):
        """Lista todos los usuarios con paginación."""
        return {"users": self.service.all(), "page": page, "limit": limit}

    @get("/users/{id}")
    def show(self, id: str):
        """Obtiene un usuario por su ID."""
        user = self.service.find(id)
        if not user:
            return (404, {"error": f"User with id {id} not found"})
        return {"user": user}

    @post("/users", status_code=201)
    def store(self, body: CreateUserDTO):
        """Crea un usuario a partir del DTO validado AOT."""
        created = self.service.create(name=body.name, email=body.email, role=body.role)
        return {"status": "created", "user": created}
