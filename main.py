import flet as ft
from app.Loading import Loading
from app.TestSection import TestPanel
from app.ImageSection import ImagePanel
from app.controller import Controller
from time import sleep
from pathlib import Path
from services.ImageType import ImageType
import asyncio

export_folder = Path().resolve() / "assets" / "img" / "exp"

def main(page: ft.Page):
    
    page.title = "Coollab regression test"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.spacing = 0
    page.padding = 0

    loading_container = Loading()
    page.add(loading_container)

    async def initialize_app():

        controller = Controller(page)
        controller.export_folder_path = str(export_folder)

        await asyncio.to_thread(controller.check_tests_validity)

        loading_container.opacity = 0
        loading_container.update()
        await asyncio.sleep(0.3)
        page.controls.clear()

        left_container = TestPanel(controller, page.height)
        right_container = ImagePanel(controller, page.height)
        controller.set_test_panel(left_container)
        controller.set_image_panel(right_container)

        def resize_handler(e):
            left_container.height = page.height
            right_container.height = page.height
            left_container.update()
            right_container.update()
        page.on_resized = resize_handler

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

    page.run_task(initialize_app)

if __name__ == "__main__":
    try:
        ft.app(target=main, assets_dir="assets")
    finally:
        for file in export_folder.iterdir():
            if file.is_file():
                file.unlink()

# Exemple de commande pour l'app packagée : pyinstaller --noconsole --onefile --icon=assets/favicon.ico main.py
# Permet de packager l'application en un seul fichier exécutable, avec une icône personnalisée
