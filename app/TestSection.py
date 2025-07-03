import flet as ft
from app.controller import Controller
from app.components.TestPathForm import TestPathForm
from app.components.TestList import TestList
from app.components.TestFooter import TestFooter
from app.theme.AppColors import AppColors


class TestPanel(ft.Container):
    def __init__(self, controller: Controller, height: float):
        super().__init__()
        self.controller = controller
        self.height = height
        
        self.path_section = TestPathForm(self.controller)
        self.project_section = TestList(self.controller)
        self.counter_section = TestFooter(self.controller)

        self._build()
    
    def _build(self):
        self.content = ft.Column(
            [
                self.path_section,
                ft.Divider(height=1, color=AppColors.DARK, thickness=1),
                self.project_section,
                ft.Divider(height=1, color=AppColors.DARK, thickness=1),
                self.counter_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
            spacing=5,
        )
        self.padding = ft.padding.symmetric(horizontal=20, vertical=10)
        self.bgcolor = ft.Colors.with_opacity(0.6, AppColors.DARK)
        self.col = {"md": 4}
        self.height = self.height
# To do
    # def start_test(self, pending_number:int):
    #     self.path_section.disable_controls()
    #     self.project_section.clear_view()
    #     self.counter_section.update_size(pending_number)
    #     self.path_section.update_progress(0)