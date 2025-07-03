import flet as ft

class Loading(ft.Container):
    def __init__(self):
        super().__init__()
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#79B9CA", "#E1AB91", "#9E71C5", "#6568F3", "#A49CB3", "#A38699"],
        )
        self._build()

    def _build(self):
        self.expand = True
        self.opacity=1.0
        self.animate_opacity=300
        self.content = ft.Column(
            [
                ft.Image(
                    src="assets/img/logo.png",
                    width=120,
                    height=120,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Text(
                    "Projects loading",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.ProgressRing(
                    color=ft.Colors.WHITE,
                    stroke_width=4,
                    width=40,
                    height=40,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        )