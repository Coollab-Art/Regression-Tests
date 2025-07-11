import flet as ft
from TestsData import TestData, TestStatus
from app.theme.AppColors import AppColors

def create_tile(test_data: TestData, on_tile_click, on_restart_click) -> ft.ListTile:
    is_ready = test_data.status in [TestStatus.READY, TestStatus.PASSED, TestStatus.FAILED]
    match test_data.status:
        case TestStatus.CHECKING:
            tile_color = ft.Colors.GREY_700
            tile_icon = ft.Icons.TIMER_SHARP
            subtitle_text = "Checking test..."
        case TestStatus.READY:
            tile_color = ft.Colors.GREY_300
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

    trailing_button = ft.ElevatedButton(
        content=ft.Icon(ft.Icons.RESTART_ALT_ROUNDED, color=ft.Colors.SECONDARY if is_ready else ft.Colors.GREY_800),
        on_click=lambda e: on_restart_click(test_data.id),
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            padding=0,
            bgcolor=AppColors.DARK,
        ),
        disabled=False if is_ready else True,
    )
    
    return ft.ListTile(
        leading=ft.Icon(tile_icon, color=tile_color),
        title=ft.Text(test_data.name, color=tile_color, size=16, weight=ft.FontWeight.W_500,),
        subtitle=ft.Text(subtitle_text, color=tile_color, size=13, weight=ft.FontWeight.W_400, italic=True,),
        trailing=trailing_button,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        on_click=lambda e: on_tile_click(test_data.id) if is_ready else None,
    )