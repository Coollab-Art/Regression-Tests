import flet as ft
from app.controller import Controller
from app.components.ImgFilter import ImgFilter
from app.components.ImgDisplay import ImgDisplay
from app.theme.AppColors import AppColors


class ImagePanel(ft.Container):
    def __init__(self, controller: Controller, height: float):
        super().__init__()
        self.controller = controller
        self.height = height
        self.filter_section = ImgFilter(self.controller)
        self.image_section = ImgDisplay(self.controller, 'No image preview available yet')
        self._build()

    def _build(self):

        self.content = ft.Column(
            [
                self.filter_section,
                ft.Divider(height=1, color=AppColors.DARK, thickness=2),
                self.image_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
            spacing=0,
        )
        self.padding = ft.padding.all(0)
        self.bgcolor = ft.Colors.with_opacity(0.7, AppColors.DARK)
        self.col = {"md": 8}
        self.height = self.height

    def reset(self):
        self.filter_section.reset()
        self.image_section.reset()

