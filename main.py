import flet as ft
from app.Loading import Loading
from app.TestSection import TestPanel
from app.ImageSection import ImagePanel
from app.controller import Controller
from app.components.TestPathForm import TestPathForm
from time import sleep
from pathlib import Path
from services.ImageType import ImageType
import asyncio
from services.coollab_handler import (
    start_coollab,
)

export_folder = Path().resolve() / "assets" / "img" / "exp"

def main(page: ft.Page):
    
    page.title = "Coollab regression test"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.spacing = 0
    page.padding = 0

    loading_container = Loading()

    async def hide_loading():
            loading_container.opacity = 0
            loading_container.update()
            await asyncio.sleep(0.3)
            page.controls.clear()
    def show_loading():
            page.controls.clear()
            page.add(loading_container)
            loading_container.opacity = 1
            loading_container.update()
    
    async def try_start_coollab(controller: Controller):
        coollab_path = controller.get_coollab_path()

        if coollab_path.strip() == "":
            return False
        
        try:
            await asyncio.to_thread(start_coollab, Path(coollab_path))
            return True
        except Exception as e:
            print(f"Error on Coollab launch : {e}")
            return False
    
    async def coollab_path_loop(controller: Controller):
        async def on_submit():
            if await try_start_coollab(controller):
                event.set()
            else:
                show_form(error=True)

        def show_form(error=False):
            form = TestPathForm(controller, on_submit, submit_text="Launch Coollab")
            error_text = ft.Text(value="Invalid path", color="red") if error else ft.Text("")
            page.controls.clear()
            page.add(
                ft.Container(
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=["#79B9CA", "#E1AB91", "#9E71C5", "#6568F3", "#A49CB3", "#A38699"],
                    ),
                    expand=True,
                    content=ft.Column(
                        [
                            ft.Image(
                                src="assets/img/logo.png",
                                width=120,
                                height=120,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            ft.Text(
                                "Valid Coollab path required",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                            form,
                            error_text,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=30,
                    ),
                    alignment=ft.alignment.center,
                    padding=40,
                )
            )
            page.update()
            
        if await try_start_coollab(controller):
            return
        event = asyncio.Event()
        show_form()
        await event.wait()

    async def display_app(controller: Controller):
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

    async def initialize_app():
        controller = Controller(page)
        await coollab_path_loop(controller)
        show_loading()
        # await controller.check_tests_validity()
        # await hide_loading()
        # await display_app(controller)


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
