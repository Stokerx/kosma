from typing import Dict, List, Optional
from examples.basic_app.models import User

class UserService:
    def __init__(self):
        self._users: Dict[str, User] = {
            "1": User(id="1", name="Taylor Otwell", email="taylor@laravel.com", role="admin"),
            "2": User(id="2", name="Guido van Rossum", email="guido@python.org", role="core"),
        }

    def all(self) -> List[dict]:
        return [u.__dict__ for u in self._users.values()]

    def find(self, user_id: str) -> Optional[dict]:
        user = self._users.get(user_id)
        return user.__dict__ if user else None

    def create(self, name: str, email: str, role: str = "user") -> dict:
        new_id = str(len(self._users) + 1)
        user = User(id=new_id, name=name, email=email, role=role)
        self._users[new_id] = user
        return user.__dict__
