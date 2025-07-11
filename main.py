import flet as ft
from pathlib import Path
from app.controller import Controller
from app.Loading import Loading
from app.initialization import coollab_path_loop
from app.layout import display_app
import asyncio

export_folder = Path().resolve() / "assets" / "img" / "exp"

def main(page: ft.Page):
    page.title = "Coollab regression test"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.spacing = 0
    page.padding = 0

    loading = Loading()

    def show_loading():
        page.controls.clear()
        page.add(loading)
        loading.opacity = 1
        loading.update()

    async def hide_loading():
        loading.opacity = 0
        loading.update()
        await asyncio.sleep(0.3)
        page.controls.clear()

    async def initialize_app():
        controller = Controller(page)
        await coollab_path_loop(page, controller)
        display_app(page, controller)
        # TODO init all test tiles
        await controller.check_tests_validity()
        controller.test_panel.update_progress(0)
        # show_loading()
        # await hide_loading()

    page.run_task(initialize_app)

if __name__ == "__main__":
    try:
        ft.app(target=main, assets_dir="assets")
    finally:
        # todo close coollab with controller.coollab.close_app()
        for file in export_folder.iterdir():
            if file.is_file():
                file.unlink()

# Exemple de commande pour l'app packagée : pyinstaller --noconsole --onefile --icon=assets/favicon.ico main.py
# Permet de packager l'application en un seul fichier exécutable, avec une icône personnalisée
