import flet as ft
from pathlib import Path
from app.controller import Controller
from app.Loading import Loading
from app.initialization import coollab_path_loop
from app.layout import display_app
import asyncio
from services.Coollab import Coollab

export_folder = Path().resolve() / "assets" / "img" / "exp"
controller: Controller | None = None

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
        if loading in page.controls:
            loading.opacity = 0
            loading.update()
            await asyncio.sleep(0.3)
        page.controls.clear()

    async def initialize_app():
        global controller
        controller = Controller(page)
        show_loading()
        await coollab_path_loop(page, controller)
        # controller.coollab = Coollab()
        await hide_loading()
        display_app(page, controller)
        controller.init_test_tiles()
        await controller.check_tests_validity()
        controller.update_all_test_tiles()
        controller.test_panel.update_progress(0.005)

    page.run_task(initialize_app)

if __name__ == "__main__":
    try:
        ft.app(target=main, assets_dir="assets")
    finally:
        if controller and getattr(controller, "coollab", None):
            controller.coollab.close_app()
        for file in export_folder.iterdir():
            if file.is_file():
                file.unlink()

# Exemple de commande pour l'app packagée : pyinstaller --noconsole --onefile --icon=assets/favicon.ico main.py
# Permet de packager l'application en un seul fichier exécutable, avec une icône personnalisée
