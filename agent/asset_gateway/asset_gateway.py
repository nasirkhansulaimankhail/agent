"""Serve only public bench assets in the container's filesystem namespace."""
from werkzeug.middleware.shared_data import SharedDataMiddleware


def not_found(environ, start_response):
    start_response("404 Not Found", [("Content-Type", "text/plain"), ("Cache-Control", "no-store")])
    return [b"Not Found\n"]


static = SharedDataMiddleware(
    not_found,
    {"/assets": "/home/frappe/frappe-bench/sites/assets"},
    cache=True,
    cache_timeout=300,
)


def application(environ, start_response):
    if environ.get("REQUEST_METHOD") not in ("GET", "HEAD"):
        start_response("405 Method Not Allowed", [("Allow", "GET, HEAD"), ("Content-Length", "0")])
        return []
    return static(environ, start_response)


if __name__ == "__main__":
    # systemd's docker-exec client cannot signal the in-container Gunicorn itself.
    import os
    import signal
    import time
    from pathlib import Path
    pid_file = Path("/home/frappe/frappe-bench/config/assets.pid")
    if pid_file.exists():
        pid = int(pid_file.read_text().strip())
        command = Path(f"/proc/{pid}/cmdline")
        if command.exists() and b"asset_gateway:application" in command.read_bytes():
            os.kill(pid, signal.SIGTERM)
            for _ in range(100):
                if not command.exists() or not command.read_bytes():
                    break
                time.sleep(0.1)
            else:
                raise RuntimeError("Asset gateway did not stop within 10 seconds")
        # Docker recreation can leave a PID file from a different PID namespace.
        if pid_file.exists() and pid_file.read_text().strip() == str(pid):
            pid_file.unlink()
