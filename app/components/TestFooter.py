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
        
        self.update_all_refs_button = ft.ElevatedButton(
            "Update all ref files",
            icon=ft.Icons.BROWSER_UPDATED,
            on_click=self.on_update_refs_click,
            opacity=0.5,
            style=ft.ButtonStyle(padding=ft.padding.only(left=10, right=15, top=10, bottom=12)),
        )

        self.coollab_version = ft.Text(value="Coollab version", color=ft.Colors.with_opacity(0.7, AppColors.LIGHT_BLUE), size=11)
        self._build()

    def _build(self):
        self.content=ft.Row(
            [
                self.update_all_refs_button,
                self.coollab_version,
                ft.Row(
                    [
                        ft.Text(value="Results :", color=ft.Colors.WHITE, size=12),
                        self.ended_test_num,
                        self.total_pending,
                    ],
                    spacing=5,
                    expand=False
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
        self.update_current()

    def decrement_current(self):
        self.current_count = max(0, self.current_count - 1)
        self.update_current()

    def reset_current(self):
        self.current_count = 0
        self.update_current()

    def update_current(self):
        self.ended_test_num.value = str(self.current_count)
        self.update()
    
    def update_coollab_version_name(self, version_name: str):
        self.coollab_version.value = f"Version : {version_name}"
        self.coollab_version.update()
    
    async def on_update_refs_click(self, e):
        await self.controller.update_all_tests_ref()

    def disable_controls(self):
        self.update_all_refs_button.disabled = True
        self.update_all_refs_button.update()
    def enable_controls(self):
        self.update_all_refs_button.disabled = False
        self.update_all_refs_button.update()