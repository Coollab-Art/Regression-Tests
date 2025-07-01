import flet as ft
from app.controller import Controller
from TestsData import TestData

dark_color = '#191C20'
light_blue = '#A0CAFD'

good_score_threshold = 200

def create_tile(controller:Controller, test_data: TestData, on_tile_click, on_redo_click) -> ft.ListTile:
    status = test_data.status
    score = test_data.score
    if not status:
        tile_color = ft.Colors.GREY_500
        tile_icon = ft.Icons.TIMER_SHARP
    else:
        if score <= good_score_threshold:
            tile_color = ft.Colors.GREEN_ACCENT_700
            tile_icon = ft.Icons.CHECK_CIRCLE_OUTLINED
        else :
            tile_color = ft.Colors.RED_ACCENT_400
            tile_icon = ft.Icons.CANCEL_OUTLINED

    subtitle_text = "Processing..." if not status else "Result : " + str(score)

    trailing_button = ft.ElevatedButton(
        content=ft.Icon(ft.Icons.RESTART_ALT_ROUNDED, color=ft.Colors.SECONDARY if status else ft.Colors.GREY_800),
        on_click=lambda e: on_redo_click(test_data.id),
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            padding=0,
            bgcolor=dark_color,
        ),
        disabled=True if not status else False,
    )
    
    return ft.ListTile(
        leading=ft.Icon(tile_icon, color=tile_color),
        title=ft.Text(test_data.test_name, color=tile_color, size=16, weight=ft.FontWeight.W_500,),
        subtitle=ft.Text(subtitle_text, color=tile_color, size=13, weight=ft.FontWeight.W_400, italic=True,),
        trailing=trailing_button,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        on_click=lambda e: on_tile_click(test_data.id) if status else None,
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

    def add_processing_tile(self, test_data: TestData):
        pending_tile = create_tile(self.controller, test_data, self.tile_click, self.redo_click)
        self.lv.controls.append(pending_tile)
        self.tiles_by_id[test_data.id] = pending_tile

    def replace_tile(self, test_data: TestData):
        result_tile = create_tile(self.controller, test_data, self.tile_click, self.redo_click)
        test_id = test_data.id
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

        self.controller.reset_filter_preview()
        self.controller.update_preview(test_id, "threshold")

    def redo_click(self, test_id: int):
        print(f"Relaunching test {test_id}...")
        self.controller.relaunch_test(test_id)