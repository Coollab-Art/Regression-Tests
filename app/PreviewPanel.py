import flet as ft
import numpy as np
import cv2
import base64
from PIL import Image
import tempfile
from app.controller import Controller

dark_color = '#191C20'
light_blue = '#A0CAFD'

class PreviewPanel(ft.Container):
    def __init__(self, controller, height: float):
        super().__init__()
        self.controller = controller
        self.height = height
        self.image_section = ImgDisplay('No image preview available yet')
        self._build()

    def _build(self):
        selector_section = imgSelector()
        comparison_section = startEndComparison(self.height * 0.3)

        self.content = ft.Column(
            [
                selector_section,
                ft.Divider(height=1, color=dark_color, thickness=2),
                self.image_section,
                ft.Divider(height=1, color=dark_color, thickness=2),
                comparison_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
            spacing=0,
        )
        self.padding = ft.padding.all(0)
        self.bgcolor = ft.Colors.with_opacity(0.7, dark_color)
        self.col = {"md": 6}
        self.height = self.height

    def start_test(self):
        self.image_section = ImgDisplay('No image preview available yet')

    def update_content(self, result: str):
        self.image_section.update_text(result)

def imgSelector() -> ft.Container:

    selector_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=0),
        # padding=ft.padding.only(left=10, right=15, top=18, bottom=20),
        padding=ft.padding.symmetric(horizontal=20, vertical=28),
    )

    return ft.Container(
        content=ft.Row(
            [
                ft.ElevatedButton(
                    "Outlined",
                    icon=ft.Icons.IMAGE_SEARCH_OUTLINED,
                    style=selector_style,
                    bgcolor=dark_color,
                    color=ft.Colors.with_opacity(.6, light_blue),
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Diff",
                    icon=ft.Icons.GRADIENT_OUTLINED,
                    style=selector_style,
                    bgcolor=dark_color,
                    color=ft.Colors.with_opacity(.6, light_blue),
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Exported",
                    icon=ft.Icons.COMPARE_OUTLINED,
                    style=selector_style,
                    bgcolor=dark_color,
                    color=ft.Colors.with_opacity(.6, light_blue),
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Original",
                    icon=ft.Icons.IMAGE_OUTLINED,
                    style=selector_style,
                    bgcolor=dark_color,
                    color=ft.Colors.with_opacity(.6, light_blue),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            # height=100,
            spacing=0,
        ),
        padding=0,
        margin=0,
    )

class ImgDisplay(ft.Container):
    def __init__(self,  initial_text: str):
        super().__init__(
            bgcolor=ft.Colors.with_opacity(.3, dark_color),
            padding=0,
            margin=0,
            expand=True,
        )
        self.label = ft.Text(initial_text, color=ft.Colors.ON_SURFACE)
        self.label_container = ft.Container(
            content=self.label,
            alignment=ft.alignment.center,
            padding=ft.padding.all(10),
        )
        self.content=ft.Stack(
            [
                ft.Image(
                    src="/img/chess.png",
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    expand=True,
                ),
                self.label_container,
            ],
            alignment=ft.alignment.center,
            expand=True,
        )

    def update_text(self, new_text: str):
        self.label.value = new_text
        self.label_container.alignment = ft.alignment.bottom_left

def startEndComparison(height: float) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Image(
                    src="/img/test.png",
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    expand=True,
                ),
                ft.Image(
                    src="/img/chess-altered-hard.png",
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            expand=True,
        ),
        bgcolor=ft.Colors.with_opacity(.3, dark_color),
        padding=0,
        margin=0,
        height=height,
    )