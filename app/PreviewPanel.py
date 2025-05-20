import flet as ft

def PreviewPanel(height: float) -> ft.Container:
    return ft.Container(
        ft.Text("Column 2"),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=ft.Colors.with_opacity(0.8, '#1B1B1D'),
        col={"md": 6},
        height=height,
    )