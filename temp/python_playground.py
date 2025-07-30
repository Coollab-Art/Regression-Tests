import flet as ft
from pynput.mouse import Controller as MouseController

def main(page: ft.Page):
    page.title = "Menu contextuel (pynput)"
    page.padding = 30

    mouse = MouseController()
    context_menu = ft.Container(visible=False)

    def hide_context_menu():
        context_menu.visible = False
        page.update()

    def on_redo_click(test_id):
        print(f"Refaire test {test_id}")
        hide_context_menu()

    def on_tile_click(test_id):
        print(f"Tile cliquée (ID: {test_id})")

    def on_secondary_tap(e: ft.ControlEvent, test_id: int):
        pos = mouse.position  # Position globale
        screen_x, screen_y = pos[0], pos[1]

        # Convertir en position relative à la fenêtre Flet
        # Ici on considère que Flet est en haut à gauche
        offset_x = -50
        offset_y = -75

        context_menu.left = screen_x + offset_x
        context_menu.top = screen_y + offset_y
        # context_menu.left = screen_x
        # context_menu.top = screen_y
        context_menu.content = ft.Column(
            controls=[
                ft.TextButton("🔁 Refaire le test", on_click=lambda e: on_redo_click(test_id)),
            ],
            tight=True,
        )
        context_menu.visible = True
        page.update()

    test_data = {
        "id": 1,
        "test_name": "Test mémoire",
        "status": True,
        "score": 92,
    }

    tile_color = ft.Colors.GREEN_ACCENT_700 if test_data["score"] < 80 else ft.Colors.RED_ACCENT_400
    tile_icon = ft.Icons.CHECK_CIRCLE_OUTLINED if test_data["score"] < 80 else ft.Icons.CANCEL_OUTLINED
    subtitle_text = f"Résultat : {test_data['score']}"

    tile = ft.ListTile(
        leading=ft.Icon(tile_icon, color=tile_color),
        title=ft.Text(test_data["test_name"], color=tile_color, size=16, weight=ft.FontWeight.W_500),
        subtitle=ft.Text(subtitle_text, italic=True, color=tile_color, size=13),
        trailing=ft.IconButton(icon=ft.Icons.RESTART_ALT, on_click=lambda e: on_redo_click(test_data["id"])),
        on_click=lambda e: on_tile_click(test_data["id"]),
        bgcolor=ft.Colors.with_opacity(0.05, "#191C20"),
        shape=ft.RoundedRectangleBorder(radius=12),
    )


    gesture_tile = ft.GestureDetector(
        on_secondary_tap=lambda e: on_secondary_tap(e, test_data["id"]),
        content=tile
    )

    context_menu = ft.Container(
        visible=False,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=8,
        padding=10,
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=1,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 2),
        ),
    )

    # Clic global pour fermer le menu
    page.on_click = lambda e: hide_context_menu()

    page.add(
        ft.Stack(
            controls=[gesture_tile, context_menu],
            expand=True,
        )
    )

ft.app(target=main)
