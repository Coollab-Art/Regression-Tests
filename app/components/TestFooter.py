import flet as ft
from app.controller import Controller
from app.theme.AppColors import AppColors


class TestFooter(ft.Container):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self.current_count = 0
        self.ended_test_num=ft.Text(value="0", color=ft.Colors.WHITE,  size=12)
        self.total_pending=ft.Text(value="/ ?", color=ft.Colors.WHITE,  size=12)
        self._build()

    def _build(self):
        self.content=ft.Row(
            [
                ft.Text(value="Results :", color=ft.Colors.WHITE, size=12),
                self.ended_test_num,
                self.total_pending,
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=5,
            expand=True,
        )

    def update_size(self, pending_size: int):
        self.total_pending.value = "/ " + str(pending_size)
        self.current_count = 0
        self.ended_test_num.value = str(self.current_count)
        self.update()

    def increment_current(self):
        self.current_count += 1
        self.ended_test_num.value = str(self.current_count)
        self.update()

    def decrement_current(self):
        self.current_count -= 1
        self.ended_test_num.value = str(self.current_count)
        self.update()