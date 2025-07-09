# services/initialization.py
import asyncio
from pathlib import Path
import flet as ft
from services.coollab_handler import start_coollab
from app.components.TestPathForm import TestPathForm

async def try_start_coollab(controller):
    path = controller.get_coollab_path().strip()
    if not path:
        return False
    try:
        await asyncio.to_thread(start_coollab, Path(path))
        return True
    except Exception as e:
        print(f"Error on Coollab launch: {e}")
        return False

async def coollab_path_loop(page: ft.Page, controller):
    if await try_start_coollab(controller):
        return

    event = asyncio.Event()

    async def on_submit():
        if await try_start_coollab(controller):
            event.set()
        else:
            show_form(error=True)

    def show_form(error=False):
        form = TestPathForm(controller, on_submit, submit_text="Launch Coollab")
        error_text = ft.Text("Invalid path", color="red") if error else ft.Text("")
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
                        ft.Image(src="assets/img/logo.png", width=120, height=120),
                        ft.Text("Valid Coollab path required", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        form,
                        error_text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                    width=800,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(horizontal=30, vertical=20),
            )
        )
        page.update()

    show_form()
    await event.wait()
