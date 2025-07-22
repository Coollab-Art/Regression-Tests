import flet as ft
from app.controller import Controller
import asyncio
import inspect
from app.theme.AppColors import AppColors


class TestPathForm(ft.Container):
    def __init__(self, controller: Controller, submit_text: str = "Submit", submit_action = None):
        super().__init__()
        self.controller = controller
        self.submit_action = submit_action
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.browse_button = ft.IconButton(
            icon=ft.Icons.FOLDER_OPEN,
            tooltip="Open file picker",
            on_click=self.open_file_picker,
        )
        self.input_field = ft.TextField(
            label="Coollab version path",
            border_radius=50,
            text_size=12,
            expand=True,
            value=self.controller.get_coollab_path(),
            on_focus=lambda e: self.controller.set_focus_state(True),
            on_blur=lambda e: self.controller.set_focus_state(False),
        )
        self.submit_button = ft.ElevatedButton(
            submit_text,
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.on_submit,
            style=ft.ButtonStyle(padding=ft.padding.only(left=10, right=15, top=18, bottom=20)),
        )
        self._build()

    def _build(self):
        self.controller.page.overlay.append(self.file_picker)
        self.content=ft.Row(
            [
                self.input_field,
                self.browse_button,
                self.submit_button,
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            height=40,
        )

    def open_file_picker(self, e):
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["exe"],
        )
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            selected_path = e.files[0].path
            self.input_field.value = selected_path
            self.input_field.update()
        else:
            print("[INFO] File selection canceled")
    
    async def on_submit(self, e):
        coollab_path = self.input_field.value
        if coollab_path.strip() != "":
            if self.controller.coollab is None or coollab_path != self.controller.get_coollab_path():
                await self.controller.relaunch_coollab(coollab_path)
            self.controller.set_coollab_path(coollab_path)
            if self.submit_action:
                await self.submit_action()
        else:
            print("[Error] Please enter a valid path")

    def disable_controls(self):
        self.input_field.disabled = True
        self.submit_button.disabled = True
        self.browse_button.disabled = True
        self.update()
    def enable_controls(self):
        self.input_field.disabled = False
        self.submit_button.disabled = False
        self.browse_button.disabled = False
        self.update()