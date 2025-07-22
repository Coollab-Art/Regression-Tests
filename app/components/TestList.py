import flet as ft
from app.controller import Controller
from TestsData import TestData, TestStatus
from app.theme.AppColors import AppColors
import threading
from services.ImageType import ImageType
from app.components.Tile import create_tile

class TestList(ft.Container):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self.lv = ft.ListView(spacing=5, padding=0, auto_scroll=True, expand=True)
        self.tiles_by_id = {}
        self.selected_tile_id = None
        self._build()
    
    def _build(self):
        self.content=ft.Column([self.lv],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
        self.expand=True

    def clear_test_view(self):
        self.lv.controls.clear()
        self.tiles_by_id.clear()
        self.selected_tile_id = None
        self.lv.update()

    def update_tile(self, test_data: TestData):
        new_tile = create_tile(self.controller, test_data, self.tile_click)
        test_id = test_data.id
        if test_id in self.tiles_by_id:
            existing_tile = self.tiles_by_id[test_id]
            try:
                index = self.lv.controls.index(existing_tile)
                self.lv.controls[index] = new_tile
                self.tiles_by_id[test_id] = new_tile
            except ValueError:
                print(f"[ERROR] Test ID {test_id} not found in the list for update")
        else:
            # print(f"[INFO] Adding new tile for test ID {test_id}")
            self.lv.controls.append(new_tile)
            self.tiles_by_id[test_id] = new_tile
        self.lv.update()

    def tile_click(self, test_id: int):
        clicked_tile = self.tiles_by_id.get(test_id)
        
        if clicked_tile is None:
            print(f"[ERROR] Tile with ID {test_id} not found on click")
            return

        if self.selected_tile_id is not None and self.selected_tile_id != test_id:
            selected_tile = self.tiles_by_id.get(self.selected_tile_id)
            selected_tile.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            selected_tile.update()

        self.selected_tile_id = test_id
        clicked_tile.bgcolor = ft.Colors.with_opacity(0.25, AppColors.LIGHT_BLUE)
        clicked_tile.update()

        self.controller.reset_img_filter()
        self.controller.update_img_display(test_id, ImageType.THRESHOLD)