import flet as ft
from TestsData import TestData, TestStatus
from app.theme.AppColors import AppColors
from app.controller import Controller

def create_tile(controller: Controller, test_data: TestData, on_tile_click) -> ft.GestureDetector:
    is_ready = test_data.status in [TestStatus.READY, TestStatus.PASSED, TestStatus.FAILED]
    is_done = test_data.status in [TestStatus.PASSED, TestStatus.FAILED]
    match test_data.status:
        case TestStatus.CHECKING:
            tile_color = ft.Colors.GREY_600
            tile_icon = ft.Icons.TIMER_SHARP
            subtitle_text = "Checking test..."
        case TestStatus.READY:
            tile_color = ft.Colors.GREY_400
            tile_icon = ft.Icons.CHECK_CIRCLE_OUTLINED
            subtitle_text = "Ready to launch"
        case TestStatus.IN_PROGRESS:
            tile_color = ft.Colors.GREY_500
            tile_icon = ft.Icons.TIMER_SHARP
            subtitle_text = "Processing..."
        case TestStatus.PASSED:
            tile_color = ft.Colors.GREEN_ACCENT_700
            tile_icon = ft.Icons.CHECK_CIRCLE_OUTLINED
            subtitle_text = "Result : " + str(test_data.score)
        case TestStatus.FAILED:
            tile_color = ft.Colors.RED_ACCENT_400
            tile_icon = ft.Icons.CANCEL_OUTLINED
            subtitle_text = "Result : " + str(test_data.score)
    
    popup_menu = ft.Container(
        visible=False,
        bgcolor=AppColors.DARK,
        opacity=0.8,
        padding=2,
        border_radius=18,
        right=10,
        top=15,
        content=None,
        shadow=ft.BoxShadow(
            blur_radius=12,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 2),
        ),
    )

    def hide_popup_menu(e=None):
        if popup_menu.visible:
            popup_menu.visible = False
            popup_menu.update()
    
    def on_secondary_tap(e: ft.ControlEvent):
        # popup_menu.right = 0
        # popup_menu.top = 

        popup_menu.content=ft.Column([ft.TextButton("🔁 Update ref image", on_click=on_update_ref),])
        popup_menu.visible = True
        popup_menu.update()
    
    async def on_restart(e):
        await controller.relaunch_test(test_data.id)

    async def on_update_ref(e):
        hide_popup_menu()
        await controller.update_test_ref(test_data.id)

    trailing_button = ft.ElevatedButton(
        content=ft.Icon(ft.Icons.RESTART_ALT_ROUNDED, color=ft.Colors.SECONDARY if is_ready else ft.Colors.GREY_800),
        on_click=on_restart,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            padding=0,
            bgcolor=AppColors.DARK,
        ),
        disabled=not is_ready,
    )
    
    tile = ft.ListTile(
        leading=ft.Icon(tile_icon, color=tile_color),
        title=ft.Text(test_data.name, color=tile_color, size=16, weight=ft.FontWeight.W_500),
        subtitle=ft.Text(subtitle_text, color=tile_color, size=13, italic=True),
        trailing=trailing_button,
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
        on_click=lambda e: on_tile_click(test_data.id) if is_done else None,
    )

    return ft.GestureDetector(
        content=ft.Stack(
            controls=[tile, popup_menu],
            expand=True,
        ),
        on_exit=hide_popup_menu,
        on_secondary_tap=on_secondary_tap
    )