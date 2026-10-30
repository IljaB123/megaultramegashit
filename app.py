
import json

APP_VERSION = "0.1.0"

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")

    if path == "/":
        status = "200 OK"
        data = {
            "application": "ica0022",
            "version": APP_VERSION,
            "message": "Hello from Docker v2!"
        }
    elif path == "/healthz":
        status = "200 OK"
        data = {"status": "alive"}
    else:
        status = "404 Not Found"
        data = {"error": "Not found"}

    body = json.dumps(data).encode("utf-8")

    start_response(status, [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(body)))
    ])

    return [body]

