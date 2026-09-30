import sys
import os

# Ensure parent directory is at the front of sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from server import app as fastapi_app

# Vercel ASGI wrapper to normalize incoming rewrite paths
class VercelHandler:
    def __init__(self, asgi_app):
        self.asgi_app = asgi_app

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http":
            path = scope.get("path", "")
            # If Vercel rewrote the path to /api/index.py or /api/index or /api
            if path in ("/api/index.py", "/api/index", "/api", "/api/"):
                headers = dict(scope.get("headers", []))
                matched = headers.get(b"x-matched-path", headers.get(b"x-vercel-matched-path", b"")).decode("utf-8", errors="ignore")
                if matched and matched not in ("/api/index.py", "/api/index"):
                    scope["path"] = matched
                    scope["raw_path"] = matched.encode("utf-8")
                else:
                    scope["path"] = "/"
                    scope["raw_path"] = b"/"
        await self.asgi_app(scope, receive, send)

app = VercelHandler(fastapi_app)
