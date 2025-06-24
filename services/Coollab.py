import socket
import json
from time import sleep
from typing import Optional

class Coollab:
    _host: str
    _port: int
    _s: Optional[socket.socket]

    def __init__(self, host: str = "127.0.0.1", port: int = 12345) -> None:
        self._host = host
        self._port = port
        self._s = None

    def __enter__(self) -> "Coollab":
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((self._host, self._port))
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._s:
            self._s.close()

    def _encode_json(self, dic: dict) -> bytes:
        return json.dumps(dic).encode("utf-8") + b"\0"

    def export_image(self, width: int = 500, height: int = 500) -> None:
        if self._s:
            self._s.sendall(
                self._encode_json(
                    {
                        "command": "ExportImage",
                        "width": width,
                        "height": height,
                        "format": ".png",
                    }
                )
            )

    def log(self, title: str, content: str) -> None:
        if self._s:
            self._s.sendall(
                self._encode_json(
                    {
                        "command": "Log",
                        "title": title,
                        "content": content,
                    }
                )
            )