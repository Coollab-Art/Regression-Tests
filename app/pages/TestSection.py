import flet as ft
from app.controller import Controller
from app.components.TestPathForm import TestPathForm
from app.components.TestList import TestList
from app.components.TestFooter import TestFooter
from app.theme.AppColors import AppColors
from pathlib import Path


class TestPanel(ft.Container):
    def __init__(self, controller: Controller, height: float):
        super().__init__()
        self.controller = controller
        self.height = height
        
        self.path_section = TestPathForm(self.controller, submit_text="Launch All Tests", submit_action=self.controller.launch_all_tests)
        self.progress_bar = ft.ProgressBar(value=0.005, expand=True, height=5, bgcolor=AppColors.DARK)
        self.project_section = TestList(self.controller)
        self.counter_section = TestFooter(self.controller)

        self._build()
    
    def _build(self):
        self.content = ft.Column(
            [
                self.path_section,
                ft.Container(content=self.progress_bar,height=5,),
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
    
    def update_progress(self, progress: int):
        self.progress_bar.value = progress
        self.progress_bar.update()
    
    def disable_controls(self):
        self.path_section.disable_controls()
        self.counter_section.disable_controls()
    def enable_controls(self):
        self.path_section.enable_controls()
        self.counter_section.enable_controls()