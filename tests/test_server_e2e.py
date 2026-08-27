import threading
import time
import urllib.request
import urllib.error
import orjson
from dataclasses import dataclass
from kosma import KosmaApp, Controller, get, post

@dataclass
class ItemDTO:
    title: str
    price: float
    in_stock: bool

class ItemController(Controller):
    @get("/items/{id}")
    def get_item(self, id: str):
        return {"id": id, "title": f"Item_{id}", "price": 99.99}

    @post("/items", status_code=201)
    def create_item(self, body: ItemDTO):
        return {
            "status": "created",
            "item": {
                "title": body.title,
                "price": body.price,
                "in_stock": body.in_stock,
            }
        }

def test_server_http_end_to_end_and_features():
    app = KosmaApp(title="Test API", version="1.0.0")
    app.enable_cors(allow_origins=["*"])
    app.register(ItemController)
    app.compile()

    port = 8888
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=port),
        daemon=True,
    )
    server_thread.start()
    time.sleep(0.15)

    base_url = f"http://127.0.0.1:{port}"

    # 1. Test GET /items/99
    req = urllib.request.Request(f"{base_url}/items/99")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        assert resp.headers.get("Access-Control-Allow-Origin") == "*"
        data = orjson.loads(resp.read())
        assert data == {"id": "99", "title": "Item_99", "price": 99.99}

    # 2. Test POST /items with valid DTO (201 Created)
    post_payload = orjson.dumps({
        "title": "Mechanical Keyboard",
        "price": 149.50,
        "in_stock": True
    })
    post_req = urllib.request.Request(
        f"{base_url}/items",
        data=post_payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(post_req) as resp:
        assert resp.status == 201
        data = orjson.loads(resp.read())
        assert data["status"] == "created"
        assert data["item"]["title"] == "Mechanical Keyboard"

    # 3. Test POST /items with INVALID DTO (422 Unprocessable Entity)
    invalid_payload = orjson.dumps({
        "title": "Broken Item",
        "price": "not_a_number"
        # in_stock is missing
    })
    bad_req = urllib.request.Request(
        f"{base_url}/items",
        data=invalid_payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        urllib.request.urlopen(bad_req)
        assert False, "Expected 422 Unprocessable Entity"
    except urllib.error.HTTPError as e:
        assert e.code == 422
        err_res = orjson.loads(e.read())
        assert err_res["message"] == "Validation failed"
        assert "price" in err_res["errors"]
        assert "in_stock" in err_res["errors"]

    # 4. Test CORS Preflight (OPTIONS /items)
    options_req = urllib.request.Request(
        f"{base_url}/items",
        method="OPTIONS"
    )
    with urllib.request.urlopen(options_req) as resp:
        assert resp.status == 204
        assert resp.headers.get("Access-Control-Allow-Origin") == "*"
        assert "POST" in resp.headers.get("Access-Control-Allow-Methods", "")

    # 5. Test OpenAPI spec endpoint (/openapi.json)
    openapi_req = urllib.request.Request(f"{base_url}/openapi.json")
    with urllib.request.urlopen(openapi_req) as resp:
        assert resp.status == 200
        spec = orjson.loads(resp.read())
        assert spec["openapi"] == "3.0.0"
        assert "/items" in spec["paths"]
        assert "post" in spec["paths"]["/items"]

    # 6. Test Swagger UI HTML page (/docs)
    docs_req = urllib.request.Request(f"{base_url}/docs")
    with urllib.request.urlopen(docs_req) as resp:
        assert resp.status == 200
        assert "text/html" in resp.headers.get("Content-Type", "")
        html_content = resp.read().decode("utf-8")
        assert "SwaggerUIBundle" in html_content
