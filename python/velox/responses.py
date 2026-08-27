from typing import Any, Optional, Dict
import orjson

class Response:
    def __init__(self, content: Any, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        self.status_code = status_code
        self.headers = headers or {}
        self.content = content

    def to_raw(self) -> tuple[int, bytes]:
        if isinstance(self.content, bytes):
            return self.status_code, self.content
        elif isinstance(self.content, str):
            return self.status_code, self.content.encode("utf-8")
        else:
            return self.status_code, orjson.dumps(self.content)

class JsonResponse(Response):
    def __init__(self, data: Any, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        super().__init__(content=orjson.dumps(data), status_code=status_code, headers=headers)

class TextResponse(Response):
    def __init__(self, text: str, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        super().__init__(content=text.encode("utf-8"), status_code=status_code, headers=headers)
