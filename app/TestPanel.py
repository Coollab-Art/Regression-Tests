import flet as ft
from time import sleep
import asyncio

dark_color = '#191C20'
light_blue = '#A0CAFD'

def TestPanel(height: float) -> ft.Container:

    version_section = versionSelection()
    project_section = testListSection()
    counter_section = counterSection()

    return ft.Container(
        content=ft.Column(
            [
                version_section,
                ft.Divider(height=1, color=dark_color),
                project_section,
                ft.Divider(height=1, color=dark_color),
                counter_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=ft.Colors.with_opacity(0.6, dark_color),
        col={"md": 6},
        height=height,
    )

def versionSelection() -> ft.Container:

    input_field = ft.TextField(
        label="Coollab version path",
        border_radius=50,
        text_size=12,
        expand=True,
    )
    submit_button = ft.ElevatedButton(
        "Launch test",
        icon=ft.Icons.PLAY_ARROW,
        style=ft.ButtonStyle(padding=ft.padding.only(left=10, right=15, top=18, bottom=20)),
    )
    def launch_test(e):
        input_field.disabled = True
        submit_button.disabled = True
        e.page.update()
        # TODO : Launch the test
    submit_button.on_click = launch_test

    return ft.Container(
        content=ft.Row(
            [
                input_field,
                submit_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            height=40,
        ),
    )

# test_data = [
#     {"name": "User Login", "score": 90, "status": True},
#     {"name": "Product Search", "score": 50.6, "status": True},
#     {"name": "Add to Cart", "score": 96, "status": True},
#     {"name": "Admin Dashboard", "score": 30, "status": True},
#     {"name": "Reporting Module", "score": 85, "status": True},
#     {"name": "API Endpoint A", "score": 79.7, "status": True},
#     {"name": "API Endpoint B", "score": 80.2, "status": True},
#     {"name": "Email Notifications", "score": 100, "status": True},
#     {"name": "Checkout Process", "score": 0, "status": False},
#     {"name": "Database Connection", "score": 0, "status": False},
# ]

def testListSection() -> ft.Container:
    lv = ft.ListView(spacing=10, padding=20, auto_scroll=False)

    # def create_test_tile(data: dict) -> ft.ListTile:
    #     icon_data = ft.Icons.QUESTION_MARK
    #     color = ft.Colors.GREY_500
    #     if data["status"] == False:
    #         icon_data = ft.Icons.TIMER_SHARP
    #         color_state = ft.Colors.GREY_700
    #     elif data["score"] < 80:
    #         icon_data = ft.Icons.CANCEL_OUTLINED
    #         color_state = ft.Colors.RED_ACCENT_700
    #     elif data["score"] >= 80:
    #         icon_data = ft.Icons.CHECK_CIRCLE_OUTLINED
    #         color_state = ft.Colors.GREEN_ACCENT_700

    #     return ft.ListTile(
    #         leading=ft.Icon(icon_data, color=color_state),
    #         title=ft.Text(f"{data['name']}", color=color_state),
    #         subtitle=ft.Text(f"Score: {data['score']}", color=ft.Colors.GREEN_ACCENT_400, size=10),
    #         trailing=ft.ElevatedButton(
    #             content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
    #             # on_click=display_test_result,
    #             style=ft.ButtonStyle(
    #                 shape=ft.CircleBorder(),
    #                 padding=0,
    #                 bgcolor=ft.Colors.BLUE_GREY_900
    #             ),
    #         ),
    #         bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
    #     )
    
    # def load_test_list(e=None):
    #     print("Loading test data...")
    #     lv.controls.clear()
    #     for data in test_data:
    #         tile = create_test_tile(data)
    #         lv.controls.append(tile)
    #     lv.update()
    #     print("Test data loaded.")
    
    # def display_test_result(e):
    #     lv.controls.clear()
    #     this.icon = ft.Icons.REMOVE_RED_EYE_ROUNDED
    #     this.icon_color = ft.Colors.ON_SECONDARY
    #     lv.update()

    return ft.Container(
        content=ft.Column(
            [
                ft.ListView(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.CANCEL_OUTLINED, color=ft.Colors.RED_ACCENT_400),
                            title=ft.Text("Test fhffh", color=ft.Colors.RED_ACCENT_400),
                            subtitle=ft.Text(f"Score: 90", color=ft.Colors.RED_ACCENT_400, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINED, color=ft.Colors.GREEN_ACCENT_700),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREEN_ACCENT_700),
                            subtitle=ft.Text(f"Score: 90", color=ft.Colors.GREEN_ACCENT_400, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.TIMER_SHARP, color=ft.Colors.GREY_500),
                            title=ft.Text("Test fhffh", color=ft.Colors.GREY_500),
                            subtitle=ft.Text(f"Processing", color=ft.Colors.GREY_500, size=10),
                            trailing=ft.ElevatedButton(
                                content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, color=ft.Colors.SECONDARY),
                                # on_click=display_test_result,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=0,
                                    bgcolor=dark_color
                                ),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                    ],
                    spacing=5, 
                    padding=0, 
                    auto_scroll=True,
                    expand=True,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        ),
        expand=True,
    )

def counterSection() -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Text(value="Results :", color=ft.Colors.WHITE,  size=12),
                ft.Text(value="0/25", color=ft.Colors.WHITE,  size=12),
            ],
            alignment=ft.MainAxisAlignment.END,
            expand=True,
        ),
    )