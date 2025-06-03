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
        self.selector_section = ImgSelector(self.controller)
        self.comparison_section = ComparisonSection(self.controller, self.height * 0.3)
        self._build()

    def _build(self):

        self.content = ft.Column(
            [
                self.selector_section,
                ft.Divider(height=1, color=dark_color, thickness=2),
                self.image_section,
                ft.Divider(height=1, color=dark_color, thickness=2),
                self.comparison_section,
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
        self.image_section.reset()
        self.comparison_section.reset()

    def update_content(self, result: str):
        self.image_section.update_text(result)
        self.image_section.label_container.alignment = ft.alignment.bottom_left

class ImgSelector(ft.Container):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.selector_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0),
            # padding=ft.padding.only(left=10, right=15, top=18, bottom=20),
            padding=ft.padding.symmetric(horizontal=20, vertical=28),
        )
        self._build()

    def _build(self):
        self.content=ft.Row(
            [
                # ft.ElevatedButton(
                #     "Outlined",
                #     icon=ft.Icons.IMAGE_SEARCH_OUTLINED,
                #     style=self.selector_style,
                #     bgcolor=dark_color,
                #     color=ft.Colors.with_opacity(.6, light_blue),
                #     expand=True,
                # ),
                ft.ElevatedButton(
                    "Threshold",
                    icon=ft.Icons.GRADIENT_OUTLINED,
                    style=self.selector_style,
                    bgcolor=dark_color,
                    color=ft.Colors.with_opacity(.6, light_blue),
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Exported",
                    icon=ft.Icons.COMPARE_OUTLINED,
                    style=self.selector_style,
                    bgcolor=dark_color,
                    color=ft.Colors.with_opacity(.6, light_blue),
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Original",
                    icon=ft.Icons.IMAGE_OUTLINED,
                    style=self.selector_style,
                    bgcolor=dark_color,
                    color=ft.Colors.with_opacity(.6, light_blue),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )
        self.padding=0
        self.margin=0

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
        self.displayed_image = ft.Image(
            src="/img/img2-friend.png",
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            expand=True,
        )
        self.content=ft.Stack(
            [
                self.displayed_image,
                self.label_container,
            ],
            alignment=ft.alignment.center,
            expand=True,
        )

    def reset(self):
        self.displayed_image.src_base64 = None
        self.displayed_image.src = "/img/img2-friend.png"
        self.update_text('No image preview available yet')
        self.label_container.alignment = ft.alignment.center

    def update_text(self, new_text: str):
        self.label.value = new_text

    def update_img(self, image: str):
        self.displayed_image.src = None
        self.displayed_image.src_base64 = image

class ComparisonSection(ft.Container):
    def __init__(self, controller, height: float):
        super().__init__(
            height = height,
        )
        self.controller = controller
        self.original_image = ft.Image(
            src="/img/img1.png",
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            expand=True,
        )
        self.exported_image = ft.Image(
            src="/img/img1-small.png",
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            expand=True,
        )
        self._build()

    def _build(self):
        self.content=ft.Row(
            [
                self.original_image,
                self.exported_image,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            expand=True,
        )
        self.bgcolor=ft.Colors.with_opacity(.3, dark_color)
        self.padding=0
        self.margin=0
    
    def reset(self):
        self.original_image.src_base64 = None
        self.exported_image.src_base64 = None
        self.original_image.src = "/img/img1.png"
        self.exported_image.src = "/img/img1-small.png"

    def update_img(self, original_image: str, exported_image: str):
        self.original_image.src = None
        self.exported_image.src = None
        self.original_image.src_base64 = original_image
        self.exported_image.src_base64 = exported_image