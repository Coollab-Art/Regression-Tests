import flet as ft
from app.controller import Controller
from services.utils import (
    get_hex,
    get_color_at_pos,
)
from app.theme.AppColors import AppColors
import asyncio


placeholder_path = "/img/logo.png"

class ImgDisplay(ft.Container):
    def __init__(self, controller: Controller,  initial_text: str):
        super().__init__()
        self.controller = controller
        self.mouse_inside = False
        self.image_displayed = False
        self.running_color_tracker = False

        # Image with label
        self.label = ft.Text(initial_text, color=ft.Colors.with_opacity(.7, ft.Colors.ON_SURFACE))
        self.label_container = ft.Container(
            content=self.label,
            alignment=ft.alignment.center,
            padding=ft.padding.all(10),
            visible=True,
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
            color=AppColors.LIGHT_BLUE,
            size=14,
            weight=ft.FontWeight.BOLD
        )
        self.mouse_follower_color_block = ft.Container(
            width=10,
            height=10,
            bgcolor=AppColors.LIGHT_BLUE,
        )
        self.mouse_follower_container = ft.Container(
            content=ft.Row([self.mouse_follower_color_block,self.mouse_follower_text_content]),
            left=0,
            top=0,
            bgcolor=ft.Colors.with_opacity(.8, AppColors.DARK),
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            border_radius=ft.border_radius.all(5),
            blur=5,
            alignment=ft.alignment.center,
            visible=False,
            expand=False,
        )
        self._build()

    def _build(self):
        self.content=ft.GestureDetector(
            on_enter=lambda e: self.enter(e),
            on_hover=lambda e: self.update_color_picker_pos(e),
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
        self.bgcolor=ft.Colors.with_opacity(.3, AppColors.DARK)
        self.padding=0
        self.margin=0
        self.expand=True

    def reset(self):
        self.displayed_image.src_base64 = None
        self.displayed_image.src = placeholder_path
        self.displayed_image.fit = ft.ImageFit.COVER
        self.label.visible = True
        self.image_displayed = False
        self.mouse_inside = False
        self.update()

    def update_img(self, image: str):
        self.displayed_image.src = None
        self.displayed_image.src_base64 = image
        self.displayed_image.fit = ft.ImageFit.CONTAIN
        self.image_displayed = True
        self.displayed_image.update()
        if self.label.visible:
            self.label.visible = False
            self.label.update()
    
    def enter(self, e: ft.ControlEvent = None):
        self.mouse_inside = True
        if self.image_displayed:
            if not self.running_color_tracker:
                self.page.run_task(self.run_color_tracker)
            if not self.mouse_follower_container.visible:
                self.mouse_follower_container.visible = True
            self.update_color_picker_color()
    
    async def run_color_tracker(self):
        self.running_color_tracker = True
        while self.mouse_inside and self.image_displayed:
            self.update_color_picker_color()
            self.mouse_follower_container.update()
            await asyncio.sleep(0.05)
        self.running_color_tracker = False
    
    def hide_color_picker(self, e: ft.ControlEvent = None):
        self.mouse_inside = False
        self.mouse_follower_container.visible = False
        self.mouse_follower_text_content.value="No color detected",
        self.mouse_follower_text_content.color=AppColors.LIGHT_BLUE,
        self.mouse_follower_container.update()
    
    def update_color_picker_pos(self, e: ft.ControlEvent):
        if not self.image_displayed:
            return
        if not self.mouse_follower_container.visible:
            self.mouse_follower_container.visible = True

        offset = self.mouse_follower_text_content.size * 0.5
        new_left = e.local_x + 10
        new_top = e.local_y - offset

        if (self.mouse_follower_container.left != new_left or self.mouse_follower_container.top != new_top):
            self.mouse_follower_container.left = new_left
            self.mouse_follower_container.top = new_top
            self.mouse_follower_container.update()
        
    def update_color_picker_color(self):
        pos = self.controller.mouse.position
        rgb = get_color_at_pos(pos[0], pos[1])
        hex_color = get_hex(rgb)

        self.mouse_follower_text_content.value = f"RGB: {rgb}"
        self.mouse_follower_color_block.bgcolor = hex_color
        self.mouse_follower_container.update()