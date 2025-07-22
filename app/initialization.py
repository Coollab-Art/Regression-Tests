# services/initialization.py
import asyncio
from pathlib import Path
import flet as ft
from services.coollab_handler import start_coollab
from app.components.TestPathForm import TestPathForm
from services.Coollab import Coollab
from time import sleep
from app.controller import Controller

async def coollab_path_loop(page: ft.Page, controller: Controller):
    if await controller.try_start_coollab(controller.get_coollab_path()):
        return
    
    event = asyncio.Event()

    async def on_submit():
        if controller.coollab is not None:
            event.set()
        else:
            show_form(error=True)

    def show_form(error=False):
        form = TestPathForm(controller, submit_text="Launch Coollab", submit_action=on_submit)
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
