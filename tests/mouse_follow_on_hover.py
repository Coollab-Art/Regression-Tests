import flet as ft

def main(page: ft.Page):
    page.title = "Suivi de Souris"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = ft.Colors.BLUE_GREY_900 
    
    mouse_follower_text_content = ft.Text(
        value="Je te suis !",
        color=ft.Colors.YELLOW_ACCENT_400, 
        size=20,
        weight=ft.FontWeight.BOLD
    )

    mouse_follower_container = ft.Container(
        content=mouse_follower_text_content,
        left=0,
        top=0,
        alignment=ft.alignment.center,
        visible=False,
        expand=False,
    )

    mouse_inside = False

    def update_text_position(e: ft.ControlEvent):
        nonlocal mouse_inside
        mouse_inside = True
        offset = mouse_follower_text_content.size * 0.5
        new_left = e.local_x - offset
        new_top = e.local_y - offset

        if not mouse_follower_container.visible:
            mouse_follower_container.visible = True

        if (
            mouse_follower_container.left != new_left or
            mouse_follower_container.top != new_top
        ):
            mouse_follower_container.left = new_left
            mouse_follower_container.top = new_top
            mouse_follower_container.update()

    def hide_text(e: ft.ControlEvent):
        nonlocal mouse_inside
        mouse_inside = False
        if mouse_follower_container.visible:
            mouse_follower_container.visible = False
            mouse_follower_container.update()

    page.add(
        ft.Row(
            controls=[
                ft.Container(
                    content=ft.GestureDetector(
                        on_hover=lambda e: update_text_position(e),
                        on_exit=lambda e: hide_text(e),
                        content=ft.Stack(
                            controls=[
                                ft.Image(
                                    src="https://papers.co/wallpaper/papers.co-vn04-rainbow-color-paint-art-ink-default-pattern-40-wallpaper.jpg",
                                    fit=ft.ImageFit.COVER,
                                    error_content=ft.Text("Impossible de charger l'image", color=ft.Colors.RED_500),
                                ),
                                mouse_follower_container,
                            ],
                            expand=True,
                        ),
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.GREEN_ACCENT_700,
                ),
                ft.Container(
                    content=ft.Text("Ca ne passe plus ici !"),
                    expand=True,
                    bgcolor=ft.Colors.RED_700,
                    alignment=ft.alignment.center,
                )
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)