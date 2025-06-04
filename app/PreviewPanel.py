import flet as ft
import numpy as np
import cv2
import base64
from PIL import Image
import tempfile
from app.controller import Controller

dark_color = '#191C20'
light_blue = '#A0CAFD'
placeholder_path = "/img/logo.png"

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
        self.selector_section.reset()
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
        self.selected_test_id = None
        self.filters = [
            # {"name": "Outlined", "icon": ft.Icons.IMAGE_SEARCH_OUTLINED, "value": "outlined", "control": None, "is_active": False},
            {"name": "Threshold", "icon": ft.Icons.GRADIENT_OUTLINED, "value": "threshold", "control": None, "is_active": False},
            {"name": "Exported", "icon": ft.Icons.COMPARE_OUTLINED, "value": "exported", "control": None, "is_active": False},
            {"name": "Original", "icon": ft.Icons.IMAGE_OUTLINED, "value": "original", "control": None, "is_active": False},
        ]
        self._build()

    def _build(self):
        button_list = []
        for filter_data in self.filters:
            button = ft.ElevatedButton(
                filter_data["name"],
                icon=filter_data["icon"],
                style=self.selector_style,
                bgcolor=dark_color,
                color=ft.Colors.with_opacity(.6, light_blue),
                expand=True,
                on_click=lambda e, val=filter_data["value"]: self._on_click(e, val)
            )
            filter_data["control"] = button
            button_list.append(button)

        self.content=ft.Row(
            button_list,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )
        self.padding=0
        self.margin=0
    
    def reset(self):
        self.set_selected(None)
        for filter_data in self.filters:
            filter_data["is_active"] = False
            self._update_button(filter_data)

    def _on_click(self, e, clicked_value: str):
        for filter_data in self.filters:
            if filter_data["value"] == clicked_value:
                filter_data["is_active"] = not filter_data["is_active"] # Toggle
                self._update_button(filter_data)
                break

        if self.selected_test_id is not None:
            self.controller.update_preview(self.selected_test_id)

    def _update_button(self, filter_data: dict):
        button = filter_data["control"]
        if button is not None:
            if filter_data["is_active"]:
                button.bgcolor = light_blue
                button.color = dark_color
            else:
                button.bgcolor = dark_color
                button.color = ft.Colors.with_opacity(.6, light_blue)

    def get_filter(self) -> str | None:
        for filter_data in reversed(self.filters):
            if filter_data["is_active"]:
                return filter_data["value"]
        return None
    
    def set_selected(self, test_id: int):
        self.selected_test_id = test_id

class ImgDisplay(ft.Container):
    def __init__(self,  initial_text: str):
        super().__init__(
            bgcolor=ft.Colors.with_opacity(.3, dark_color),
            padding=0,
            margin=0,
            expand=True,
        )
        self.label = ft.Text(initial_text, color=ft.Colors.with_opacity(.7, ft.Colors.ON_SURFACE))
        self.label_container = ft.Container(
            content=self.label,
            alignment=ft.alignment.center,
            padding=ft.padding.all(10),
        )
        self.displayed_image = ft.Image(
            src=placeholder_path,
            fit=ft.ImageFit.COVER,
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
        self.displayed_image.src = placeholder_path
        self.displayed_image.fit = ft.ImageFit.COVER
        self.update_text('No image preview available yet')
        self.label_container.alignment = ft.alignment.center

    def update_text(self, new_text: str):
        self.label.value = new_text

    def update_img(self, image: str):
        self.displayed_image.src = None
        self.displayed_image.src_base64 = image
        self.displayed_image.fit = ft.ImageFit.CONTAIN

class ComparisonSection(ft.Container):
    def __init__(self, controller, height: float):
        super().__init__(
            height = height,
        )
        self.controller = controller
        self.original_image = ft.Image(
            src=placeholder_path,
            fit=ft.ImageFit.COVER,
            repeat=ft.ImageRepeat.NO_REPEAT,
            expand=True,
        )
        self.exported_image = ft.Image(
            src=placeholder_path,
            fit=ft.ImageFit.COVER,
            repeat=ft.ImageRepeat.NO_REPEAT,
            expand=True,
        )
        self.original_stack=ft.Stack(
            [
                self.original_image,
                ft.Container(
                    content=ft.Text("Original", color=ft.Colors.with_opacity(.7, ft.Colors.ON_SURFACE)),
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.symmetric(5, 10),
                )
            ],
            alignment=ft.alignment.center,
            expand=True,
        )
        self.exported_stack=ft.Stack(
            [
                self.exported_image,
                ft.Container(
                    content=ft.Text("Exported", color=ft.Colors.with_opacity(.7, ft.Colors.ON_SURFACE)),
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.symmetric(5, 10),
                )
            ],
            alignment=ft.alignment.center,
            expand=True,
        )
        self._build()

    def _build(self):
        self.content=ft.Row(
            [
                self.original_stack,
                self.exported_stack,
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
        self.original_image.src = placeholder_path
        self.exported_image.src = placeholder_path
        self.original_image.fit = ft.ImageFit.COVER
        self.exported_image.fit = ft.ImageFit.COVER

    def update_img(self, original_image: str, exported_image: str):
        self.original_image.src = None
        self.exported_image.src = None
        self.original_image.src_base64 = original_image
        self.exported_image.src_base64 = exported_image
        self.original_image.fit = ft.ImageFit.CONTAIN
        self.exported_image.fit = ft.ImageFit.CONTAIN