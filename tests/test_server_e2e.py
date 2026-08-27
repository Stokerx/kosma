import threading
import time
import urllib.request
import urllib.error
import orjson
from dataclasses import dataclass
from velox import VeloxApp, Controller, get, post

@dataclass
class ItemDTO:
    title: str
    price: float
    in_stock: bool

class ItemController(Controller):
    @get("/items/{id}")
    def get_item(self, id: str):
        return {"id": id, "title": f"Item_{id}", "price": 99.99}

    @post("/items")
    def create_item(self, body: ItemDTO):
        return {
            "status": "created",
            "item": {
                "title": body.title,
                "price": body.price,
                "in_stock": body.in_stock,
            }
        }

def test_server_http_end_to_end():
    app = VeloxApp()
    app.register(ItemController)
    app.compile()

    port = 8765
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=port),
        daemon=True,
    )
    server_thread.start()

    # Esperar a que el servidor de red esté arriba (cold start < 100ms)
    time.sleep(0.15)

    base_url = f"http://127.0.0.1:{port}"

    # 1. Test GET /items/99
    req = urllib.request.Request(f"{base_url}/items/99")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = orjson.loads(resp.read())
        assert data == {"id": "99", "title": "Item_99", "price": 99.99}

    # 2. Test POST /items with DTO
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
        assert resp.status == 200
        data = orjson.loads(resp.read())
        assert data["status"] == "created"
        assert data["item"]["title"] == "Mechanical Keyboard"
        assert data["item"]["price"] == 149.50
        assert data["item"]["in_stock"] is True

    # 3. Test 404 Route Not Found
    try:
        urllib.request.urlopen(f"{base_url}/nonexistent")
        assert False, "Expected HTTP 404"
    except urllib.error.HTTPError as e:
        assert e.code == 404
        err_data = orjson.loads(e.read())
        assert err_data["error"] == "Route not found"

    # 4. Test Concurrency (10 threads simultáneos)
    def worker(i):
        req = urllib.request.Request(f"{base_url}/items/{i}")
        with urllib.request.urlopen(req) as resp:
            assert resp.status == 200

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
