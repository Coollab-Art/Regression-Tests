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

    def export_image(self, path: Optional[str] = None, filename: Optional[str] = None, format: Optional[str] = ".png", width: Optional[int] = None, height: Optional[int] = None) -> None:
        if self._s:
            self._s.sendall(
                self._encode_json(
                    {
                        "command": "ExportImage",
                        "file_path": path,
                        "filename": filename,
                        "format": format,
                        "width": width,
                        "height": height,
                        "autosave": False,
                        "override": True
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

    def close_app(self, force_kill: bool) -> None:
        if self._s:
            self._s.sendall(
                self._encode_json(
                    {
                        "command": "CloseApp",
                        "force_kill_task_in_progress": force_kill,
                    }
                )
            )

    def open_project(self, project_path: str) -> None:
        if self._s:
            self._s.sendall(
                self._encode_json(
                    {
                        "command": "OpenProject",
                        "project_path": project_path,
                    }
                )
            )