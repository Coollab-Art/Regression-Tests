import flet as ft
from time import sleep
import asyncio
from app.controller import Controller
import threading

dark_color = '#191C20'
light_blue = '#A0CAFD'

class TestPanel(ft.Container):
    def __init__(self, controller: Controller, height: float):
        super().__init__()
        self.controller = controller
        self.height = height
        
        self.version_section = VersionSelection(self.controller)
        self.project_section = TestListSection(self.controller)
        self.counter_section = CounterSection(self.controller)

        self._build()
    
    def _build(self):
        self.content = ft.Column(
            [
                self.version_section,
                ft.Divider(height=1, color=dark_color, thickness=1),
                self.project_section,
                ft.Divider(height=1, color=dark_color, thickness=1),
                self.counter_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
            spacing=5,
        )
        self.padding = ft.padding.symmetric(horizontal=20, vertical=10)
        self.bgcolor = ft.Colors.with_opacity(0.6, dark_color)
        self.col = {"md": 6}
        self.height = self.height

    def start_test(self, pending_number:int):
        self.version_section.disable_controls()
        self.project_section.clear_view()
        self.counter_section.update_size(pending_number)
        self.version_section.update_progress(0)


class VersionSelection(ft.Container):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.browse_button = ft.IconButton(
            icon=ft.Icons.FOLDER_OPEN,
            tooltip="Open file picker",
            on_click=self.open_file_picker,
            # icon_color=light_blue
        )
        self.input_field = ft.TextField(
            label="Coollab version path",
            border_radius=50,
            text_size=12,
            expand=True,
        )
        self.submit_button = ft.ElevatedButton(
            "Launch test",
            icon=ft.Icons.PLAY_ARROW,
            on_click = self.submit_clicked,
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
            # initial_directory="C:\\Program Files",
        )
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            selected_path = e.files[0].path
            self.input_field.value = selected_path
            self.input_field.update()
        else:
            print("File selection canceled")
    
    def submit_clicked(self, e):
        coollab_path = self.input_field.value
        if coollab_path.strip() != "":
            threading.Thread(target=self.controller.launch_test, args=(coollab_path,)).start()

    def disable_controls(self):
        self.input_field.disabled = True
        self.submit_button.disabled = True
        self.browse_button.disabled = True
    def update_progress(self, progress: int):
        self.progress_bar.value = progress
    def enable_controls(self):
        self.input_field.disabled = False
        self.submit_button.disabled = False
        self.browse_button.disabled = False



def create_tile(controller:Controller, test_id:int, score:int, status:bool, on_tile_click, on_redo_click) -> ft.ListTile:
    if not status:
        tile_color = ft.Colors.GREY_500
        tile_icon = ft.Icons.TIMER_SHARP
    else:
        if score <= 200: # Score threshold for success
            tile_color = ft.Colors.GREEN_ACCENT_700
            tile_icon = ft.Icons.CHECK_CIRCLE_OUTLINED
        else :
            tile_color = ft.Colors.RED_ACCENT_400
            tile_icon = ft.Icons.CANCEL_OUTLINED

    subtitle_text = "Processing..." if not status else "Result : " + str(score)

    trailing_button = ft.ElevatedButton(
        content=ft.Icon(ft.Icons.RESTART_ALT_ROUNDED, color=ft.Colors.SECONDARY if status else ft.Colors.GREY_800),
        on_click=lambda e: on_redo_click(test_id),
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            padding=0,
            bgcolor=dark_color,
        ),
        disabled=True if not status else False,
    )
    
    return ft.ListTile(
        leading=ft.Icon(tile_icon, color=tile_color),
        title=ft.Text(f"Test {test_id}", color=tile_color, size=16, weight=ft.FontWeight.W_500,),
        subtitle=ft.Text(subtitle_text, color=tile_color, size=13, weight=ft.FontWeight.W_400, italic=True,),
        trailing=trailing_button,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        on_click=lambda e: on_tile_click(test_id) if status else None,
    )



class TestListSection(ft.Container):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self.lv = ft.ListView(spacing=5, padding=0, auto_scroll=True, expand=True)
        self.tiles_by_id = {}
        self.selected_tile = None
        self._build()
    
    def _build(self):
        self.content=ft.Column([self.lv],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
        self.expand=True

    def clear_view(self):
        self.lv.controls.clear()
        self.tiles_by_id.clear()
        self.selected_tile = None

    def add_processing_tile(self, test_id: int):
        pending_tile = create_tile(self.controller, test_id, 0, False, self.tile_click, self.redo_click)
        self.lv.controls.append(pending_tile)
        self.tiles_by_id[test_id] = pending_tile

    def replace_tile(self, test_id: int, score: int, status: bool):
        result_tile = create_tile(self.controller, test_id, score, status, self.tile_click, self.redo_click)
        if test_id in self.tiles_by_id:
            processing_tile = self.tiles_by_id[test_id]
            try:
                index = self.lv.controls.index(processing_tile)
                self.lv.controls[index] = result_tile
                if self.selected_tile == processing_tile:
                    self.selected_tile = result_tile
                self.tiles_by_id[test_id] = result_tile
            except ValueError:
                print(f"Error: Test ID {test_id} not found in the list for update")
        else:
            print(f"Warning: Attempt to update non-existent Test ID {test_id}... adding non-initialized test")
            self.lv.controls.append(result_tile)
            self.tiles_by_id[test_id] = result_tile

    def tile_click(self, test_id: int):
        clicked_tile = self.tiles_by_id.get(test_id)
        
        if clicked_tile is None:
            print(f"Error: Tile with ID {test_id} not found on click")
            return

        if self.selected_tile is not None and self.selected_tile != clicked_tile:
            self.selected_tile.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            self.selected_tile.update()

        self.selected_tile = clicked_tile
        self.selected_tile.bgcolor = ft.Colors.with_opacity(0.25, light_blue)
        self.selected_tile.update()

        self.controller.update_preview(test_id)

    def redo_click(self, test_id: int):
        print(f"Relaunching test {test_id}...")
        self.controller.relaunch_test(test_id)


class CounterSection(ft.Container):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self.current=ft.Text(value="0", color=ft.Colors.WHITE,  size=12)
        self.total_pending=ft.Text(value="/ ?", color=ft.Colors.WHITE,  size=12)
        self._build()

    def _build(self):
        self.content=ft.Row(
            [
                ft.Text(value="Results :", color=ft.Colors.WHITE, size=12),
                self.current,
                self.total_pending,
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=5,
            expand=True,
        )

    def update_size(self, pending_size: int):
        self.total_pending.value = "/ " + str(pending_size)
        self.current_count = 0
        self.current.value = "0"
    def increment_current(self):
        self.current_count += 1
        self.current.value = str(self.current_count)
    def decrement_current(self):
        self.current_count -= 1
        self.current.value = str(self.current_count)