from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class User:
    id: str
    name: str
    email: str
    role: str = "user"

@dataclass
class CreateUserDTO:
    name: str
    email: str
    role: str = "user"
