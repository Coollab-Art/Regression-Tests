from time import sleep
from typing import Callable
import websocket
import json
import threading
import asyncio


can_start = False
max_retries = 10
retry_delay = 2


def on_open(ws):
    global can_start
    can_start = True
    print("[COOLLAB INFO] Connected")


class Coollab:
    _ws: websocket.WebSocketApp
    _next_id: int = 0
    _futures: dict[int, asyncio.Future] = {}
    _callbacks: dict[int, Callable[[], None]] = {}

    def __init__(self, host: str = "127.0.0.1", port: int = 12345) -> None:
        global can_start
        can_start = False

        try_nb = 0
        while not can_start and try_nb < max_retries:
            if try_nb != 0:
                print(f"[COOLLAB WARN] Attempt {try_nb} failed, retrying...")
                self._ws.close()
            try_nb += 1
            self.start_websocket(host, port)
            waited = 0
            while not can_start and waited < retry_delay:
                sleep(0.1)
                waited += 0.1

        if not can_start:
            raise ConnectionError("[COOLLAB ERROR] Could not connect to server after multiple attempts.")
        else:
            self._loop = asyncio.get_running_loop()

        
    def start_websocket(self, host: str, port: int):
        try:
            self._ws = websocket.WebSocketApp(
                f"ws://{host}:{port}", on_open=on_open, on_message=self._on_message
            )
            thread = threading.Thread(target=self._ws.run_forever)
            thread.daemon = True
            thread.start()

        except Exception as e:
            print(f"[COOLLAB ERROR] Exception during connection :",e)
    
    def _get_next_id(self) -> int:
        id = self._next_id
        self._next_id += 1
        return id

    def _send_request(self, request: str, params: dict):
        future = self._loop.create_future()
        id = self._get_next_id()

        self._futures[id] = future
        params["request"] = request
        params["request_id"] = id
        # print(f"[COOLLAB INFO] Sending request: {request} with params: {params}")
        self._ws.send(json.dumps(params))

        return future

    def _on_message(self, ws, message):
        print("[COOLLAB INFO] Received:", message)
        d = json.loads(message)
        response_id = d.get("response_id") # TODO c++ return this key in all responses

        if d["event"] == "OpenedProject":
            self._loop.call_soon_threadsafe(self._futures[response_id].set_result, None)
        elif d["event"] == "ImageExportStarted":
            self._loop.call_soon_threadsafe(self._futures[response_id].set_result, None)
        elif d["event"] == "ImageExportFinished":
            self._loop.call_soon_threadsafe(self._callbacks[response_id], d["path"])
        elif d["event"] == "GetVersionName":
            self._loop.call_soon_threadsafe(self._futures[response_id].set_result, d["version_name"])

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
        on_image_export_finished: Callable[[], None] | None = None,
    ) -> None:
        print(f"Exporting image : {filename}")
        if on_image_export_finished:
            self._callbacks[self._next_id] = on_image_export_finished
        future = self._send_request(
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
        await future

    def log(self, title: str, content: str) -> None:
        self._send_request(
            "Log",
            {
                "title": title,
                "content": content,
            },
        )

    def close_app(self) -> None:
        print("[COOLLAB INFO] Closing Coollab")
        self._send_request(
            "CloseApp",
            {
                "force_kill_task_in_progress": False,
            },
        )

    async def get_version_name(self) -> None:
        future = self._send_request(
            "GetVersionName",
            {
                # "param1": False,
            },
        )
        return await future

    async def open_project(self, path: str) -> None:
        future = self._send_request(
            "OpenProject",
            {
                "path": path,
            },
        )
        await future