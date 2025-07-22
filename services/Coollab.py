from time import sleep
from typing import Callable
import websocket
import json
import threading
import asyncio


can_start = False


def on_open(ws):
    global can_start
    can_start = True
    print("[COOLLAB INFO] Connected")


class Coollab:
    _ws: websocket.WebSocketApp
    _callback: Callable[[], None]
    _next_id: int = 0
    _future: asyncio.Future

    def __init__(self, host: str = "127.0.0.1", port: int = 12345) -> None:
        self._ws = websocket.WebSocketApp(
            f"ws://{host}:{port}", on_open=on_open, on_message=self._on_message
        )
        thread = threading.Thread(target=self._ws.run_forever)
        thread.daemon = True
        thread.start()
        while not can_start:  # Wait until websocket connection is created
            pass

    def _send_command(self, command: str, params: dict):
        params["command"] = command
        params["command_id"] = self._next_id
        self._next_id += 1
        self._ws.send(json.dumps(params))

    def _on_message(self, ws, message):
        print("[COOLLAB INFO] Received:", message)
        d = json.loads(message)
        if d["event"] == "ImageExportFinished":
            self._loop.call_soon_threadsafe(
                self._callback, d["path"]
            )
        elif d["event"] == "OpenedProject":
            self._loop.call_soon_threadsafe(
                self._future.set_result, None
            )  # TODO use command_id to know which future to set
        elif d["event"] == "ImageExportStarted":
            self._loop.call_soon_threadsafe(self._future.set_result, None)

    # Starts the export, it only only be finished a lot later, and then the callback on_image_export_finished() will be called
    async def start_image_export(
        self,
        width: int = 500,
        height: int = 500,
        folder: str | None = None,
        filename: str | None = None,
        extension: str | None = None,
        project_autosave: bool = False,
        export_file_overwrite: bool = False,
    ) -> None:
        print(f"Exporting image : {filename}")
        self._send_command(
            "ExportImage",
            {
                "width": width,
                "height": height,
                "folder": folder,
                "filename": filename,
                "extension": extension,
                "project_autosave": project_autosave,
                "export_file_overwrite": export_file_overwrite,
            },
        )
        self._loop = asyncio.get_running_loop()
        self._future = self._loop.create_future()
        await self._future

    def log(self, title: str, content: str) -> None:
        self._send_command(
            "Log",
            {
                "title": title,
                "content": content,
            },
        )

    def close_app(self) -> None:
        self._send_command(
            "CloseApp",
            {
                "force_kill_task_in_progress": False,
            },
        )

    async def open_project(self, path: str) -> None:
        self._send_command(
            "OpenProject",
            {
                "path": path,
            },
        )
        self._loop = asyncio.get_running_loop()
        self._future = self._loop.create_future()
        await self._future

    def on_image_export_finished(self, callback: Callable[[], None]) -> None:
        self._callback = callback