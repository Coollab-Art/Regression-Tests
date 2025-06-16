import flet as ft
import requests
from PIL import Image
import io


IMAGE_URL = "https://papers.co/wallpaper/papers.co-vn04-rainbow-color-paint-art-ink-default-pattern-40-wallpaper.jpg"

downloaded_pil_image: Image.Image | None = None

def main(page: ft.Page):
    page.title = "Suivi de Souris"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = ft.Colors.BLUE_GREY_900 
    
    color_display_text = ft.Text(
        value="Je te suis !",
        color=ft.Colors.YELLOW_ACCENT_400, 
        size=20,
        weight=ft.FontWeight.BOLD
    )

    mouse_follower_container = ft.Container(
        content=color_display_text,
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
        offset = color_display_text.size * 0.5
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
    
    def load_image_for_processing():
        global downloaded_pil_image # Utilise 'global' car downloaded_pil_image est une variable globale
        try:
            print(f"DEBUG: Téléchargement de l'image depuis : {IMAGE_URL}")
            response = requests.get(IMAGE_URL)
            response.raise_for_status() # Lève une exception pour les codes d'état HTTP erronés
            image_bytes = io.BytesIO(response.content)
            # Ensure it's converted to 'RGB' mode. Pillow's RGB is always (R, G, B)
            downloaded_pil_image = Image.open(image_bytes).convert("RGB") 

            print(f"DEBUG: Image téléchargée et chargée en PIL. Dimensions : {downloaded_pil_image.size}")
        except requests.exceptions.RequestException as req_err:
            print(f"ERREUR: Échec du téléchargement de l'image : {req_err}")
        except Exception as e:
            print(f"ERREUR: Échec du chargement de l'image dans PIL : {e}")
    
    def on_image_hover(e: ft.ControlEvent):
        if downloaded_pil_image is None:
            color_display_text.value = "Image non chargée..."
            color_display_text.color = ft.Colors.RED_300
            color_display_text.update()
            return

        current_x = None
        current_y = None

        if hasattr(e, 'local_x') and hasattr(e, 'local_y'):
            current_x = int(e.local_x)
            current_y = int(e.local_y)
        elif hasattr(e, 'x') and hasattr(e, 'y'):
            current_x = int(e.x)
            current_y = int(e.y)
        
        if current_x is None or current_y is None:
            color_display_text.value = "Erreur: Coordonnées souris non disponibles."
            color_display_text.color = ft.Colors.RED_500
            color_display_text.update()
            return

        # VÉRIFICATION AJOUTÉE ICI
        if image_control.width is None or image_control.height is None:
            color_display_text.value = "Calcul des dimensions de l'image en cours..."
            color_display_text.color = ft.Colors.ORANGE_500
            color_display_text.update()
            return


        # Le reste de votre code reste le même, car il est correct une fois que les dimensions sont définies
        img_display_width = image_control.width
        img_display_height = image_control.height

        # S'assurer que les coordonnées sont dans les limites de l'image affichée
        pixel_x_display = min(max(0, current_x), img_display_width - 1)
        pixel_y_display = min(max(0, current_y), img_display_height - 1)

        # Calculer le pixel correspondant sur l'image PIL originale
        if downloaded_pil_image:
            pil_width, pil_height = downloaded_pil_image.size
            
            original_aspect_ratio = pil_width / pil_height
            display_aspect_ratio = image_control.width / image_control.height

            scaled_pil_width = image_control.width
            scaled_pil_height = image_control.height

            if original_aspect_ratio > display_aspect_ratio: # L'image est limitée par la largeur
                scaled_pil_height = image_control.width / original_aspect_ratio
            else: # L'image est limitée par la hauteur
                scaled_pil_width = image_control.height * original_aspect_ratio
            
            # Calculer l'offset si l'image n'occupe pas toute la surface de image_control
            offset_x = (image_control.width - scaled_pil_width) / 2
            offset_y = (image_control.height - scaled_pil_height) / 2

            # Mettre à l'échelle les coordonnées de la souris aux dimensions de l'image PIL
            # en tenant compte des offsets
            if current_x < offset_x or current_x > offset_x + scaled_pil_width or \
               current_y < offset_y or current_y > offset_y + scaled_pil_height:
                # La souris est en dehors de l'image effective, mais dans le cadre du contrôle Flet
                color_display_text.value = "Passez la souris sur l'image..."
                color_display_text.color = ft.Colors.WHITE
                color_display_text.update()
                return

            # Coordonnées dans l'image mise à l'échelle
            mapped_x = current_x - offset_x
            mapped_y = current_y - offset_y

            # Mettre à l'échelle aux dimensions de l'image PIL originale
            pixel_x = int(mapped_x * (pil_width / scaled_pil_width))
            pixel_y = int(mapped_y * (pil_height / scaled_pil_height))

            # Assurer que les coordonnées ne dépassent pas les limites de l'image PIL
            pixel_x = min(max(0, pixel_x), pil_width - 1)
            pixel_y = min(max(0, pixel_y), pil_height - 1)
        else:
            # Fallback si downloaded_pil_image est None
            color_display_text.value = "Image non chargée..."
            color_display_text.color = ft.Colors.RED_300
            color_display_text.update()
            return

        try:
            rgb = downloaded_pil_image.getpixel((pixel_x, pixel_y))
            
            displayed_r = rgb[0] 
            displayed_g = rgb[1]
            displayed_b = rgb[2]

            hex_color = f"#{displayed_r:02x}{displayed_g:02x}{displayed_b:02x}".upper()

            color_display_text.value = f"Couleur RGB du pixel ({pixel_x}, {pixel_y}): R={displayed_r}, G={displayed_g}, B={displayed_b}"
            color_display_text.color = hex_color
            color_display_text.update()
            
        except Exception as getpixel_err:
            color_display_text.value = f"Erreur de lecture pixel: {getpixel_err}"
            color_display_text.color = ft.Colors.ORANGE_300
            color_display_text.update()
            print(f"ERREUR: Échec de getpixel : {getpixel_err}")
    
    image_control = ft.Image(
        src=IMAGE_URL,
        width=500,
        height=500,
        expand=True,
        fit=ft.ImageFit.CONTAIN,
        error_content=ft.Text("Impossible de charger l'image", color=ft.Colors.RED_500),
    )
    

    page.add(
        ft.Row(
            controls=[
                ft.Container(
                    content=ft.GestureDetector(
                        on_hover=lambda e: (
                            update_text_position(e),
                            on_image_hover(e),
                        ),
                        on_exit=lambda e: (
                            hide_text(e),
                            setattr(color_display_text, 'value', "Déplacez la souris sur l'image..."),
                            setattr(color_display_text, 'color', ft.Colors.WHITE),
                            color_display_text.update()
                        ), 
                        drag_interval=0,
                        content=ft.Stack(
                            controls=[
                                image_control,
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

    page.run_thread(load_image_for_processing)

if __name__ == "__main__":
    ft.app(target=main)