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

    def add_pending_project(self, test_id: int):
        self.project_section.add_processing_tile(test_id)

    def update_result(self, progress: int, test_id: int, score: int, status: bool):
        self.version_section.update_progress(progress)
        self.project_section.replace_tile(test_id, score, status)
        self.counter_section.increment_current()

    def end_test(self):
        self.version_section.enable_controls()
        self.version_section.update_progress(1)



class VersionSelection(ft.Container):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
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
        self.content=ft.Column(
            [
                ft.Row(
                    [
                        self.input_field,
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
    
    def submit_clicked(self, e):
        coollab_path = self.input_field.value
        if coollab_path.strip() != "":
            threading.Thread(target=self.controller.launch_test, args=(coollab_path,)).start()

    def disable_controls(self):
        self.input_field.disabled = True
        self.submit_button.disabled = True
    def update_progress(self, progress: int):
        self.progress_bar.value = progress
    def enable_controls(self):
        self.input_field.disabled = False
        self.submit_button.disabled = False



def create_tile(controller:Controller, test_id:int, score:int, status:bool, on_tile_click) -> ft.ListTile:
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
        content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY if status else ft.Colors.GREY_800),
        # on_click=controller.relaunch_test(test_id),
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
        # trailing=trailing_button,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        on_click=lambda e: on_tile_click(e, test_id),
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
        pending_tile = create_tile(self.controller, test_id, 0, False, self._tile_click)
        self.lv.controls.append(pending_tile)
        self.tiles_by_id[test_id] = pending_tile

    def replace_tile(self, test_id: int, score: int, status: bool):
        result_tile = create_tile(self.controller, test_id, score, status, self._tile_click)
        if test_id in self.tiles_by_id:
            processing_tile = self.tiles_by_id[test_id]
            try:
                index = self.lv.controls.index(processing_tile)
                self.lv.controls[index] = result_tile
                self.tiles_by_id[test_id] = result_tile
            except ValueError:
                print(f"Erreur: Le Test ID {test_id} n'a pas été trouvée dans la liste pour la mise à jour.")
        else:
            print(f"Avertissement: Tentative de mise à jour du Test ID {test_id} non existant... ajout d'un test non initialisé'")
            self.lv.controls.append(result_tile)
            self.tiles_by_id[test_id] = result_tile

    def _tile_click(self, e, test_id: int):
        clicked_tile = self.tiles_by_id.get(test_id)
        
        if clicked_tile is None:
            print(f"Erreur: Tuile avec ID {test_id} non trouvée lors du clic.")
            return
        
        if self.selected_tile and self.selected_tile != clicked_tile:
            self.selected_tile.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            # self.selected_tile.trailing.content.name = ft.Icons.REMOVE_RED_EYE_OUTLINED
            # self.selected_tile.trailing.content.color = ft.Colors.SECONDARY
            self.selected_tile.update()

        self.selected_tile = clicked_tile
        self.selected_tile.bgcolor = ft.Colors.with_opacity(0.25, light_blue)
        # self.selected_tile.trailing.content.name = ft.Icons.REMOVE_RED_EYE
        # self.selected_tile.trailing.content.color = light_blue
        self.selected_tile.update()

        self.controller.update_preview(test_id)


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