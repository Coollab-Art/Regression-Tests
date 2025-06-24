import flet as ft
from app.controller import Controller
from app.ImgFilter import ImgFilter
from app.ImgDisplay import ImgDisplay

dark_color = '#191C20'
light_blue = '#A0CAFD'

class PreviewPanel(ft.Container):
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
                ft.Divider(height=1, color=dark_color, thickness=2),
                self.image_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
            spacing=0,
        )
        self.padding = ft.padding.all(0)
        self.bgcolor = ft.Colors.with_opacity(0.7, dark_color)
        self.col = {"md": 8}
        self.height = self.height

    def start_test(self):
        self.filter_section.reset()
        self.image_section.reset()

    def update_content(self, result: str):
        self.image_section.update_label(result)
        self.image_section.label_container.alignment = ft.alignment.bottom_left

