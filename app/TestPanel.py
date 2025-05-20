import flet as ft
import asyncio

def TestPanel(height: float) -> ft.Container:

    version_section = versionSelection()
    project_section = testListSection()
    counter_section = counterSection()

    return ft.Container(
        content=ft.Column(
            [
                version_section,
                ft.Divider(height=1, color="#1B1B1D"),
                project_section,
                ft.Divider(height=1, color="#1B1B1D"),
                counter_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=ft.Colors.with_opacity(0.7, '#1B1B1D'),
        col={"md": 6},
        height=height,
    )

def versionSelection() -> ft.Container:

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

def testListSection() -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(value="Test list", color=ft.Colors.WHITE),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        ),
        bgcolor=ft.Colors.PURPLE_700,
        expand=True,
    )

def counterSection() -> ft.Container:
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