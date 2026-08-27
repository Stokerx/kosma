from dataclasses import dataclass
from velox.controller import Controller
from velox.routing import get, post
from velox.compiler import AOTCompiler
from velox.container import Container
from velox.app import VeloxApp
import orjson

@dataclass
class UserDTO:
    name: str
    email: str
    age: int

class UserService:
    def get_user(self, user_id: str):
        return {"id": user_id, "name": f"User_{user_id}"}

    def create_user(self, name: str, email: str, age: int):
        return {"id": "123", "name": name, "email": email, "age": age}

class UserController(Controller):
    def __init__(self, service: UserService):
        self.service = service

    @get("/users/{id}")
    def show(self, id: str):
        return self.service.get_user(id)

    @post("/users")
    def store(self, body: UserDTO):
        return {"status": "created", "user": self.service.create_user(body.name, body.email, body.age)}

def test_aot_compiler_dispatches_cleanly():
    container = Container()
    controller = container.resolve(UserController)
    routes = AOTCompiler.compile_controller(controller)

    assert len(routes) == 2
    
    # 1. Test GET /users/{id}
    get_route = next(r for r in routes if r.method == "GET")
    status, payload = get_route.dispatcher(
        raw_body_bytes=b"",
        path_params={"id": "42"},
        query_params={}
    )
    assert status == 200
    data = orjson.loads(payload)
    assert data == {"id": "42", "name": "User_42"}

    # 2. Test POST /users with DTO
    post_route = next(r for r in routes if r.method == "POST")
    req_body = orjson.dumps({"name": "Bob", "email": "bob@example.com", "age": 30})
    status, payload = post_route.dispatcher(
        raw_body_bytes=req_body,
        path_params={},
        query_params={}
    )
    assert status == 200
    res_data = orjson.loads(payload)
    assert res_data["status"] == "created"
    assert res_data["user"]["name"] == "Bob"
    assert res_data["user"]["age"] == 30

def test_container_dependency_injection():
    container = Container()
    controller = container.resolve(UserController)
    assert isinstance(controller, UserController)
    assert isinstance(controller.service, UserService)
