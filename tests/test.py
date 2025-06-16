import flet as ft
import requests
from PIL import Image
import io
import time # Importation de time pour un petit délai si nécessaire

IMAGE_URL = "https://papers.co/wallpaper/papers.co-vn04-rainbow-color-paint-art-ink-default-pattern-40-wallpaper.jpg"

downloaded_pil_image: Image.Image | None = None

# Déclarons une variable pour le GestureDetector pour y accéder facilement
image_detector_area: ft.GestureDetector | None = None

def main(page: ft.Page):
    global downloaded_pil_image, image_detector_area
    original_width = None
    original_height = None

    page.title = "Suivi de Souris"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = ft.Colors.BLUE_GREY_900 
    
    color_display_text = ft.Text(
        value="Déplacez la souris sur l'image...", 
        color=ft.Colors.WHITE, 
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
        global downloaded_pil_image
        try:
            print(f"DEBUG: Téléchargement de l'image depuis : {IMAGE_URL}")
            response = requests.get(IMAGE_URL)
            response.raise_for_status()
            image_bytes = io.BytesIO(response.content)
            downloaded_pil_image = Image.open(image_bytes).convert("RGB") 
            original_width, original_height = downloaded_pil_image.size
            print(f"DEBUG: Image téléchargée et chargée en PIL. Dimensions : {downloaded_pil_image.size}")
            # Mettre à jour la page après le chargement de l'image pour rafraîchir l'UI
            page.update() 
            
            # Attendre un très court instant et forcer une mise à jour sur le GestureDetector
            # Cela donne au framework le temps de calculer les dimensions réelles.
            # C'est un "hack" mais souvent nécessaire pour les contrôles expand=True.
            time.sleep(0.1) 
            if image_detector_area:
                image_detector_area.update()
                print(f"DEBUG: GestureDetector forcé à mettre à jour. Dimensions: {image_detector_area.width}x{image_detector_area.height}")
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

        # Récupérer les dimensions du contrôle sur lequel l'événement on_hover s'est produit
        img_w = e.control.width 
        img_h = e.control.height

        # Si les dimensions ne sont toujours pas disponibles, afficher le message d'attente
        if img_w is None or img_h is None or img_w == 0 or img_h == 0:
            print(f"DEBUG: Dimensions de e.control encore indisponibles: {img_w}x{img_h}") # Aide au débogage
            color_display_text.value = "Calcul des dimensions de l'image en cours..."
            color_display_text.color = ft.Colors.GREY_500
            color_display_text.update()
            return

        # Le reste du code de calcul des pixels est correct
        pixel_x_display = min(max(0, current_x), img_w - 1)
        pixel_y_display = min(max(0, current_y), img_h - 1)

        if downloaded_pil_image:
            pil_width, pil_height = downloaded_pil_image.size
            
            original_aspect_ratio = pil_width / pil_height
            display_aspect_ratio = img_w / img_h

            scaled_pil_width = img_w
            scaled_pil_height = img_h

            if original_aspect_ratio > display_aspect_ratio:
                scaled_pil_height = img_w / original_aspect_ratio
            else:
                scaled_pil_width = img_h * original_aspect_ratio
            
            offset_x = (img_w - scaled_pil_width) / 2
            offset_y = (img_h - scaled_pil_height) / 2

            if current_x < offset_x or current_x > offset_x + scaled_pil_width or \
               current_y < offset_y or current_y > offset_y + scaled_pil_height:
                color_display_text.value = "Passez la souris sur l'image..."
                color_display_text.color = ft.Colors.WHITE
                color_display_text.update()
                return

            mapped_x = current_x - offset_x
            mapped_y = current_y - offset_y

            pixel_x = int(mapped_x * (pil_width / scaled_pil_width))
            pixel_y = int(mapped_y * (pil_height / scaled_pil_height))

            pixel_x = min(max(0, pixel_x), pil_width - 1)
            pixel_y = min(max(0, pixel_y), pil_height - 1)
        else:
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
        fit=ft.ImageFit.CONTAIN,
        width = original_width,
        height= original_height,
        error_content=ft.Text("Impossible de charger l'image", color=ft.Colors.RED_500),
        expand=True,
    )

    # Référence directe au GestureDetector pour pouvoir appeler update() dessus
    image_detector_area = ft.GestureDetector(
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
    )

    image_container = ft.Container(
        content=image_detector_area, 
        expand=True, 
        bgcolor=ft.Colors.GREEN_ACCENT_700,
    )

    page.add(
        ft.Row(
            controls=[
                image_container, 
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

    # Lancer le chargement de l'image en tâche de fond
    page.run_thread(load_image_for_processing)

    # Après l'ajout à la page, forcez un update pour aider le layout à se stabiliser
    # Cela peut aider les propriétés width/height à être définies plus tôt.
    # Un petit délai peut parfois être nécessaire pour laisser le thread UI se mettre à jour.
    page.update()
    # time.sleep(0.05) # Décommenter si cela ne fonctionne toujours pas
    # if image_detector_area:
    #     image_detector_area.update()

if __name__ == "__main__":
    ft.app(target=main)