# app/ui/layout.py
import flet as ft
from services.ImageType import ImageType
from app.pages.TestSection import TestPanel
from app.pages.ImageSection import ImagePanel

def display_app(page: ft.Page, controller):
    left_container = TestPanel(controller, page.height)
    right_container = ImagePanel(controller, page.height)
    controller.set_test_panel(left_container)
    controller.set_image_panel(right_container)

    def resize_handler(e):
        left_container.height = page.height
        right_container.height = page.height
        left_container.update()
        right_container.update()

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == " " and not controller.is_focused:
            current_filter = right_container.filter_section.get_active_filter()
            if current_filter != ImageType.ORIGINAL:
                right_container.filter_section.change_active_filter(ImageType.ORIGINAL)
            else:
                right_container.filter_section.change_active_filter(ImageType.EXPORTED)
        if e.key == "E" and not controller.is_focused:
            right_container.filter_section.change_active_filter(ImageType.EXPORTED)
        if e.key == "R" and not controller.is_focused:
            right_container.filter_section.change_active_filter(ImageType.ORIGINAL)
        if e.key == "T" and not controller.is_focused:
            right_container.filter_section.change_active_filter(ImageType.THRESHOLD)

    page.on_resized = resize_handler
    page.on_keyboard_event = on_keyboard

    page.add(
        ft.Container(
            expand=True,
            gradient=ft.RadialGradient(
                colors=["#A878BC", "#6568F2"],
                center=ft.alignment.bottom_left,
                radius=1.6,
            ),
            content=ft.ResponsiveRow(
                [left_container, right_container],
                run_spacing=0,
                spacing=0,
            ),
        )
    )
    resize_handler(None)
