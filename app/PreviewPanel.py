import flet as ft

dark_color = '#191C20'
light_blue = '#A0CAFD'

def PreviewPanel(height: float) -> ft.Container:

    selector_section = imgSelector()
    image_section = imgDisplay()
    comparison_section = startEndComparison(height*0.3)

    return ft.Container(
        content=ft.Column(
            [
                selector_section,
                ft.Divider(height=1, color=dark_color,  thickness=2),
                image_section,
                ft.Divider(height=1, color=dark_color, thickness=2),
                comparison_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
            spacing=0,
        ),
        padding=ft.padding.all(0),
        bgcolor=ft.Colors.with_opacity(0.7, dark_color),
        col={"md": 6},
        height=height,
    )

def imgSelector() -> ft.Container:

    selector_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=0),
        # padding=ft.padding.only(left=10, right=15, top=18, bottom=20),
        padding=ft.padding.symmetric(horizontal=20, vertical=28),
    )

    return ft.Container(
        content=ft.Row(
            [
                ft.ElevatedButton(
                    "Outlined",
                    icon=ft.Icons.IMAGE_SEARCH_OUTLINED,
                    style=selector_style,
                    bgcolor=dark_color,
                    color=ft.Colors.with_opacity(.6, light_blue),
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Diff",
                    icon=ft.Icons.GRADIENT_OUTLINED,
                    style=selector_style,
                    bgcolor=dark_color,
                    color=ft.Colors.with_opacity(.6, light_blue),
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Exported",
                    icon=ft.Icons.COMPARE_OUTLINED,
                    style=selector_style,
                    bgcolor=dark_color,
                    color=ft.Colors.with_opacity(.6, light_blue),
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Original",
                    icon=ft.Icons.IMAGE_OUTLINED,
                    style=selector_style,
                    bgcolor=dark_color,
                    color=ft.Colors.with_opacity(.6, light_blue),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            # height=100,
            spacing=0,
        ),
        padding=0,
        margin=0,
    )

def imgDisplay() -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [ft.Image(
                src="/img/chess.png",
                fit=ft.ImageFit.CONTAIN,
                repeat=ft.ImageRepeat.NO_REPEAT,
                expand=True,
            )],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            expand=True,
        ),
        bgcolor=ft.Colors.with_opacity(.3, dark_color),
        padding=0,
        margin=0,
        expand=True,
    )

def startEndComparison(height: float) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Image(
                    src="/img/test.png",
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    expand=True,
                ),
                ft.Image(
                    src="/img/chess-altered-hard.png",
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            expand=True,
        ),
        bgcolor=ft.Colors.with_opacity(.3, dark_color),
        padding=0,
        margin=0,
        height=height,
    )