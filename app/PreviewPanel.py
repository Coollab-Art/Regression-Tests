import flet as ft
import numpy as np
import cv2
import base64
from app.controller import Controller
from dataclasses import dataclass
from pynput.mouse import Controller as MouseController
from app.img_handler import (
    get_hex,
    get_color_at_pos,
)

dark_color = '#191C20'
light_blue = '#A0CAFD'
placeholder_path = "/img/logo.png"

class PreviewPanel(ft.Container):
    def __init__(self, controller: Controller, height: float):
        super().__init__()
        self.controller = controller
        self.height = height
        self.filter_section = ImgFilter(self.controller)
        self.image_section = ImgDisplay(self.controller, 'No image preview available yet')
        self._build()

    def _build(self):

        self.content = ft.Column(
            [
                self.filter_section,
                ft.Divider(height=1, color=dark_color, thickness=2),
                self.image_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
            spacing=0,
        )
        self.padding = ft.padding.all(0)
        self.bgcolor = ft.Colors.with_opacity(0.7, dark_color)
        self.col = {"md": 8}
        self.height = self.height

    def start_test(self):
        self.filter_section.reset()
        self.image_section.reset()

    def update_content(self, result: str):
        self.image_section.update_label(result)
        self.image_section.label_container.alignment = ft.alignment.bottom_left
    
@dataclass
class FilterButton:
    name: str
    icon: ft.Icons
    value: str
    control: ft.Control = None
    active: bool = False

class ImgFilter(ft.Container):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self.filter_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0),
            # padding=ft.padding.only(left=10, right=15, top=18, bottom=20),
            padding=ft.padding.symmetric(horizontal=20, vertical=28),
        )
        self.selected_test_id = None
        self.filters = [
            FilterButton(name="Threshold", icon=ft.Icons.GRADIENT_OUTLINED, value="threshold", control=None, active=True),
            FilterButton(name="Exported", icon=ft.Icons.COMPARE_OUTLINED, value="exported", control=None, active=False),
            FilterButton(name="Original", icon=ft.Icons.IMAGE_OUTLINED, value="original", control=None, active=False),
            # FilterButton(name="Outlined", icon=ft.Icons.IMAGE_SEARCH_OUTLINED, value="outlined", control=None, active=False),
        ]
        self._build()

    def _build(self):
        button_list = []
        for filter_data in self.filters:
            button = ft.ElevatedButton(
                filter_data.name,
                icon=filter_data.icon,
                style=self.filter_style,
                expand=True,
                on_click=lambda e, val=filter_data.value: self.change_active_filter(val),
            )
            filter_data.control = button
            button_list.append(button)

        self.content=ft.Row(
            button_list,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )
        self.padding=0
        self.margin=0
        self.update_buttons()
    
    def get_active_filter(self) -> str:
        for filter_data in self.filters:
            if filter_data.active:
                return filter_data.value
        return ""
    
    def reset(self):
        self.selected_test_id = None
        for filter_data in self.filters:
            filter_data.active = False if filter_data.value != "threshold" else True
        self.update_buttons()
    
    def change_active_filter(self, filter_value: str):
        for filter_data in self.filters:
            if filter_data.value == filter_value:
                if filter_data.active:
                    break
                else:
                    filter_data.active = True
                    if self.selected_test_id is not None:
                        self.controller.update_preview(self.selected_test_id, filter_value)
            else:
                filter_data.active = False
        self.update_buttons()
        self.update()

    def update_buttons(self):
        for filter_data in self.filters:
            button = filter_data.control
            if button is not None:
                if filter_data.active:
                    button.bgcolor = light_blue
                    button.color = dark_color
                else:
                    button.bgcolor = dark_color
                    button.color = ft.Colors.with_opacity(.6, light_blue)

class ImgDisplay(ft.Container):
    def __init__(self, controller: Controller,  initial_text: str):
        super().__init__(
            bgcolor=ft.Colors.with_opacity(.3, dark_color),
            padding=0,
            margin=0,
            expand=True,
        )
        self.controller = controller
        self.mouse_inside = False
        self.image_displayed = False

        # Image with label
        self.label = ft.Text(initial_text, color=ft.Colors.with_opacity(.7, ft.Colors.ON_SURFACE))
        self.label_container = ft.Container(
            content=self.label,
            alignment=ft.alignment.center,
            padding=ft.padding.all(10),
        )
        self.displayed_image = ft.Image(
            src=placeholder_path,
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            expand=True,
            error_content=ft.Text("Error while loading image", color=ft.Colors.RED_500),
        )

        # Color picker on hover
        self.mouse_follower_text_content = ft.Text(
            value="No color detected",
            color=light_blue,
            size=20,
            weight=ft.FontWeight.BOLD
        )
        self.mouse_follower_container = ft.Container(
            content=self.mouse_follower_text_content,
            left=0,
            top=0,
            alignment=ft.alignment.center,
            visible=False,
            expand=False,
        )
        self.mouse_ctrl = MouseController()

        # Display components
        self.content=ft.GestureDetector(
            on_hover=lambda e: self.update_color_picker(e),
            on_exit=lambda e: self.hide_color_picker(e),
            content=ft.Stack(
                controls=[
                    ft.Stack(
                        [
                            self.displayed_image,
                            self.label_container,
                        ],
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                    self.mouse_follower_container,
                ],
                expand=True,
            ),
            expand=True,
        )

    def reset(self):
        self.displayed_image.src_base64 = None
        self.displayed_image.src = placeholder_path
        self.displayed_image.fit = ft.ImageFit.COVER
        self.update_label('No image preview available yet')
        self.label_container.alignment = ft.alignment.center
        self.image_displayed = False

    def update_label(self, new_text: str):
        self.label.value = new_text

    def update_img(self, image: str):
        self.displayed_image.src = None
        self.displayed_image.src_base64 = image
        self.displayed_image.fit = ft.ImageFit.CONTAIN
        self.image_displayed = True
    
    def hide_color_picker(self, e: ft.ControlEvent):
        self.mouse_inside = False
        self.mouse_follower_text_content.value="No color detected",
        self.mouse_follower_text_content.color=light_blue,
        if self.mouse_follower_container.visible:
            self.mouse_follower_container.visible = False
            self.mouse_follower_container.update()

    
    def update_color_picker(self, e: ft.ControlEvent):
        if not self.image_displayed:
            return
        self.mouse_inside = True
        if not self.mouse_follower_container.visible:
            self.mouse_follower_container.visible = True

        offset = self.mouse_follower_text_content.size * 0.5
        new_left = e.local_x - offset
        new_top = e.local_y - offset

        pos = self.mouse_ctrl.position
        rgb = get_color_at_pos(pos[0], pos[1])
        # rgb = get_color_at_pos(e.local_x, e.local_y)
        hex_color = get_hex(rgb)

        if (self.mouse_follower_container.left != new_left or self.mouse_follower_container.top != new_top):
            self.mouse_follower_container.left = new_left
            self.mouse_follower_container.top = new_top
            self.mouse_follower_text_content.value = f"RGB: {rgb} | HEX: {hex_color}"
            self.mouse_follower_text_content.color = hex_color
            self.mouse_follower_container.update()

