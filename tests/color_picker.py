import flet as ft
import mss
import numpy as np
from pynput.mouse import Controller as MouseController

IMAGE_URL = "https://papers.co/wallpaper/papers.co-vn04-rainbow-color-paint-art-ink-default-pattern-40-wallpaper.jpg"

def get_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(*rgb)

def get_color_at_pos(x, y):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        img = sct.grab(monitor)
        color = np.array(img)[0, 0][:3]  # BGR order
        rgb = tuple(int(c) for c in color[::-1])  # convert to RGB
        return rgb

def main(page: ft.Page):
    page.title = "Color Picker visuel (survol)"
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = ft.Colors.BLACK

    title = ft.Text("🎨 Color Picker visuel", size=26, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    info_text = ft.Text(
        "Survole l'image avec ta souris\nLe texte change de couleur en fonction du pixel sous la souris",
        color=ft.Colors.WHITE,
    )

    result = ft.Text("Résultat : ", color=ft.Colors.GREEN_400, size=18)

    img = ft.Image(src=IMAGE_URL, width=600, height=400)

    mouse_ctrl = MouseController()

    def on_hover(e: ft.ControlEvent):
        pos = mouse_ctrl.position
        rgb = get_color_at_pos(pos[0], pos[1])
        hex_color = get_hex(rgb)
        result.value = f"Couleur détectée: RGB {rgb} | HEX {hex_color}"
        result.color = hex_color
        page.update()

    def on_exit(e: ft.ControlEvent):
        result.value = "Résultat : "
        result.color = ft.Colors.GREEN_400
        page.update()

    img_gesture = ft.GestureDetector(content=img, on_hover=on_hover, on_exit=on_exit)

    page.add(
        ft.Column(
            [
                title,
                img_gesture,
                info_text,
                ft.Divider(),
                result,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

ft.app(target=main)
