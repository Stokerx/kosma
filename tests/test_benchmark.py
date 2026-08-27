import threading
import time
import urllib.request
import orjson
from velox import VeloxApp, Controller, get

class BenchController(Controller):
    @get("/ping")
    def ping(self):
        return {"status": "pong", "timestamp": time.time()}

def test_cold_start_and_throughput_benchmark():
    # 1. Medir Cold Start
    start_time = time.perf_counter()
    app = VeloxApp()
    app.register(BenchController)
    app.compile()
    compile_time_ms = (time.perf_counter() - start_time) * 1000

    print(f"\n[⚡ BENCHMARK] Cold Start / AOT Compilation Time: {compile_time_ms:.2f} ms")
    assert compile_time_ms < 50.0  # El arranque y compilación debe ser ultrarrápido

    port = 8999
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=port),
        daemon=True,
    )
    server_thread.start()
    time.sleep(0.15)

    # 2. Medir Throughput con 1,000 peticiones concurrentes
    total_requests = 500
    concurrency = 20
    requests_per_thread = total_requests // concurrency
    errors = []

    def client_worker():
        for _ in range(requests_per_thread):
            try:
                req = urllib.request.Request(f"http://127.0.0.1:{port}/ping")
                with urllib.request.urlopen(req, timeout=5) as resp:
                    assert resp.status == 200
            except Exception as e:
                errors.append(e)

    bench_start = time.perf_counter()
    threads = [threading.Thread(target=client_worker) for _ in range(concurrency)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    bench_duration = time.perf_counter() - bench_start

    rps = total_requests / bench_duration
    print(f"[⚡ BENCHMARK] Procesadas {total_requests} peticiones en {bench_duration:.3f} s ({rps:.1f} req/s)")
    assert len(errors) == 0
