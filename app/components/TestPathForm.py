import flet as ft
from app.controller import Controller
import threading
from app.theme.AppColors import AppColors


class TestPathForm(ft.Container):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
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
            "Launch all",
            icon=ft.Icons.PLAY_ARROW,
            on_click = self.launch_all_clicked,
            style=ft.ButtonStyle(padding=ft.padding.only(left=10, right=15, top=18, bottom=20)),
        )
        self.progress_bar = ft.ProgressBar(value=0, expand=True)
        self._build()

    def _build(self):
        self.controller.page.overlay.append(self.file_picker)
        self.content=ft.Column(
            [
                ft.Row(
                    [
                        self.input_field,
                        self.browse_button,
                        self.submit_button,
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    height=40,
                ),
                self.progress_bar,
            ],
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
            print("File selection canceled")
    
    def launch_all_clicked(self, e):
        coollab_path = self.input_field.value
        if coollab_path.strip() != "":
            threading.Thread(target=self.controller.launch_all_tests, args=(coollab_path,)).start()

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

    def update_progress(self, progress: int):
        self.progress_bar.value = progress
        self.progress_bar.update()