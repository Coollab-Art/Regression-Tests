import flet as ft
from time import sleep
import asyncio
from app.controller import Controller

dark_color = '#191C20'
light_blue = '#A0CAFD'

def TestPanel(controller:Controller, height: float) -> ft.Container:

    version_section = versionSelection(controller)
    project_section = testListSection(controller)
    counter_section = counterSection(controller)

    return ft.Container(
        content=ft.Column(
            [
                version_section,
                ft.Divider(height=1, color=dark_color),
                project_section,
                ft.Divider(height=1, color=dark_color),
                counter_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=ft.Colors.with_opacity(0.6, dark_color),
        col={"md": 6},
        height=height,
    )

def versionSelection(controller:Controller) -> ft.Container:

    input_field = ft.TextField(
        label="Coollab version path",
        border_radius=50,
        text_size=12,
        expand=True,
    )
    submit_button = ft.ElevatedButton(
        "Launch test",
        icon=ft.Icons.PLAY_ARROW,
        style=ft.ButtonStyle(padding=ft.padding.only(left=10, right=15, top=18, bottom=20)),
    )
    def launch_test(e):
        input_field.disabled = True
        submit_button.disabled = True
        e.page.update()
        # TODO : Launch the test
    submit_button.on_click = launch_test

    return ft.Container(
        content=ft.Row(
            [
                input_field,
                submit_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            height=40,
        ),
    )

def create_tile(controller:Controller, test_id:int, score:int, status:bool) -> ft.ListTile:
    if not status:
        tile_color = ft.Colors.GREY_500
        tile_icon = ft.Icons.TIMER_SHARP
    else:
        if score >= 80:
            tile_color = ft.Colors.GREEN_ACCENT_700
            tile_icon = ft.Icons.CHECK_CIRCLE_OUTLINED
        else :
            tile_color = ft.Colors.RED_ACCENT_400
            tile_icon = ft.Icons.CANCEL_OUTLINED

    subtitle_text = "Processing..." if not status else "Result : " + str(score)

    return ft.ListTile(
        leading=ft.Icon(tile_icon, color=tile_color),
        title=ft.Text(f"Test {test_id}", color=tile_color),
        subtitle=ft.Text(subtitle_text, color=tile_color, size=10),
        trailing=ft.ElevatedButton(
            content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
            on_click=lambda e: controller.update_preview(test_id),
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                padding=0,
                bgcolor=dark_color
            ),
        ),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
    )

def testListSection(controller:Controller) -> ft.Container:
    lv = ft.ListView(spacing=10, padding=20, auto_scroll=False)

    return ft.Container(
        content=ft.Column(
            [
                ft.ListView(
                    [
                        create_tile(controller, 1, 90, True),
                        create_tile(controller, 2, 79, True),
                        create_tile(controller, 3, 0, False),
                        create_tile(controller, 4, 0, False),
                        create_tile(controller, 5, 0, False),
                    ],
                    spacing=5, 
                    padding=0, 
                    auto_scroll=True,
                    expand=True,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        ),
        expand=True,
    )

def counterSection(controller:Controller) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Text(value="Results :", color=ft.Colors.WHITE,  size=12),
                ft.Text(value="0/25", color=ft.Colors.WHITE,  size=12),
            ],
            alignment=ft.MainAxisAlignment.END,
            expand=True,
        ),
    )