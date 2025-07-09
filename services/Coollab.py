from typing import Callable
import websocket
import json
import threading


can_start = False


def on_open(ws):
    global can_start
    can_start = True
    print("Connected")


class Coollab:
    _ws: websocket.WebSocketApp
    _callback: Callable[[], None]

    def __init__(self, host: str = "127.0.0.1", port: int = 12345) -> None:
        global can_start
        can_start = False
        self._ws = websocket.WebSocketApp(
            f"ws://{host}:{port}", on_open=on_open, on_message=self._on_message
        )
        self.thread = threading.Thread(target=self._ws.run_forever)
        self.thread.daemon = True
        self.thread.start()
        while not can_start:  # Wait until websocket connection is created
            pass
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing WebSocket...")
        try:
            self._ws.close()
            self.thread.join(timeout=2)
            if self.thread.is_alive():
                print("⚠️ Thread WebSocket didn'tclose properly")
            else:
                print("✅ Thread WebSocket correctly closed")
        except Exception as e:
            print("Error on shutdown :", e)

    def _send_command(self, command: str, params: dict):
        params["command"] = command
        self._ws.send(json.dumps(params))

    def _on_message(self, ws, message):
        print("Received:", message)
        d = json.loads(message)
        if d["event"] == "ImageExportFinished":
            print("Export finished")
            self._callback()

    def export_image(self, folder: str | None = None, filename: str | None = None, extension: str | None = ".png", width: int | None = None, height: int | None = None) -> None:
        self._send_command(
            "ExportImage",
            {
                "folder": folder,
                "filename": filename,
                "extension": extension,
                "width": width,
                "height": height,
                "project_autosave": False,
                "export_file_overwrite": True
            },
        )

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

    def open_project(self, project_path: str) -> None:
        self._send_command(
            "OpenProject",
            {
                "project_path": project_path,
            },
        )

    def on_image_export_finished(self, callback: Callable[[], None]) -> None:
        self._callback = callback


# coollab = Coollab()

# IMAGE_MAX = 10
# image_count = 0

# has_finished_exporting = False


# def increase_image_count():
#     global image_count
#     global has_finished_exporting
#     image_count += 1
#     print(image_count)
#     if image_count == IMAGE_MAX:
#         coollab.close_app()
#         has_finished_exporting = True


# coollab.on_image_export_finished(increase_image_count)
# for i in range(10):
#     coollab.log(title="Script", content=f"This is {i}")
#     coollab.export_image(2000, 2000)

# # Need to keep the script running to listen to the responses from Coollab
# while not has_finished_exporting:
#     pass

# for i in range(IMAGE_MAX):
#     coollab.export_image(width=500, height=500)
#     coollab.wait_message()
#     # sleep(0.5)
# # for i in range(IMAGE_MAX):
# #     coollab.wait_message()