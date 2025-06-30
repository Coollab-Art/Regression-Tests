import flet as ft
from app.TestPanel import TestPanel
from app.PreviewPanel import PreviewPanel
from app.controller import Controller
from time import sleep
from pathlib import Path

export_folder = Path().resolve() / "assets" / "img" / "exp"

def main(page: ft.Page):
    
    page.title = "Coollab regression test"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.spacing = 0
    page.padding = 0

    controller = Controller(page)
    controller.export_folder_path = str(export_folder)

    left_container = TestPanel(controller, page.height)
    right_container = PreviewPanel(controller, page.height)

    controller.set_test_panel(left_container)
    controller.set_preview_panel(right_container)

    def resize_handler(e):
        left_container.height = page.height
        right_container.height = page.height
        left_container.update()
        right_container.update()
    page.on_resized = resize_handler

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == " " and not controller.is_focused:
            current_filter = right_container.filter_section.get_active_filter()
            if current_filter != "exported":
                right_container.filter_section.change_active_filter("exported")
            else:
                right_container.filter_section.change_active_filter("original")
    page.on_keyboard_event = on_keyboard

    page.add(
        ft.Container(
            expand=True,
            gradient = ft.RadialGradient(
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

if __name__ == "__main__":
    try:
        ft.app(target=main, assets_dir="assets")
    finally:
        for file in export_folder.iterdir():
            if file.is_file():
                file.unlink()
        print("L'application Flet est fermée.")