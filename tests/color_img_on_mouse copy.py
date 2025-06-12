import flet as ft
import requests
from PIL import Image # Nécessite 'Pillow': pip install Pillow
import io
import numpy as np # Pour le type hinting si on utilisait cv2 pour l'image locale

# URL de l'image à charger
IMAGE_URL = "https://papers.co/wallpaper/papers.co-vn04-rainbow-color-paint-art-ink-default-pattern-40-wallpaper.jpg"

# Variable globale pour stocker l'image PIL après téléchargement
# Ceci est nécessaire pour que la fonction de rappel de l'événement puisse y accéder.
downloaded_pil_image: Image.Image | None = None

def main(page: ft.Page):
    page.title = "Couleur du Pixel sous la Souris"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = ft.Colors.BLUE_GREY_900

    # Texte pour afficher la couleur RGB
    color_display_text = ft.Text(
        value="Déplacez la souris sur l'image...",
        color=ft.Colors.WHITE,
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # Nouveau texte pour afficher la couleur HEX
    hex_display_text = ft.Text(
        value="", # Vide initialement
        color=ft.Colors.WHITE,
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # --- Téléchargement et chargement de l'image une seule fois ---
    def load_image_for_processing():
        """
        Télécharge l'image depuis l'URL et la charge dans un objet PIL.Image.
        Cette opération est effectuée dans un thread séparé pour ne pas bloquer l'UI.
        """
        global downloaded_pil_image # Utilise 'global' car downloaded_pil_image est une variable globale

        try:
            print(f"DEBUG: Téléchargement de l'image depuis : {IMAGE_URL}")
            response = requests.get(IMAGE_URL)
            response.raise_for_status() # Lève une exception pour les codes d'état HTTP erronés
            image_bytes = io.BytesIO(response.content)
            # Ensure it's converted to 'RGB' mode. Pillow's RGB is always (R, G, B)
            downloaded_pil_image = Image.open(image_bytes).convert("RGB") 

            print(f"DEBUG: Image téléchargée et chargée en PIL. Dimensions : {downloaded_pil_image.size}")
            
            # Une fois l'image chargée, on peut mettre à jour l'UI si nécessaire
            # Par exemple, activer le texte ou un indicateur.
            page.show_snack_bar(
                ft.SnackBar(
                    ft.Text("Image chargée avec succès ! Passez la souris sur l'image.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_500,
                    open=True
                )
            )
            # Met à jour la page pour que la SnackBar soit visible
            page.update()

        except requests.exceptions.RequestException as req_err:
            print(f"ERREUR: Échec du téléchargement de l'image : {req_err}")
            page.show_snack_bar(
                ft.SnackBar(
                    ft.Text(f"Erreur de téléchargement d'image: {req_err}", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_500,
                    open=True
                )
            )
            page.update()
        except Exception as e:
            print(f"ERREUR: Échec du chargement de l'image dans PIL : {e}")
            page.show_snack_bar(
                ft.SnackBar(
                    ft.Text(f"Erreur de traitement d'image: {e}", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_500,
                    open=True
                )
            )
            page.update()

    # --- Gestionnaire de mouvement de souris ---
    def on_image_hover(e: ft.ControlEvent):
        """
        Fonction appelée lorsque la souris survole l'image.
        Tente d'obtenir la couleur du pixel à la position de la souris.
        """
        if downloaded_pil_image is None:
            color_display_text.value = "Image non chargée..."
            color_display_text.color = ft.Colors.RED_300
            hex_display_text.value = "" # Efface le HEX si l'image n'est pas chargée
            page.update()
            return

        current_x = None
        current_y = None

        # Tente d'obtenir les coordonnées locales (préférable pour GestureDetector)
        if hasattr(e, 'local_x') and hasattr(e, 'local_y'):
            current_x = int(e.local_x)
            current_y = int(e.local_y)
        # Fallback aux coordonnées globales si les locales sont absentes
        elif hasattr(e, 'x') and hasattr(e, 'y'):
            current_x = int(e.x)
            current_y = int(e.y)
            # print("DEBUG: Avertissement: Utilisation de e.x et e.y (coordonnées globales).")
        
        # Si aucune coordonnée n'a pu être obtenue, affiche une erreur et ne fait rien de plus
        if current_x is None or current_y is None:
            color_display_text.value = "Erreur: Coordonnées souris non disponibles."
            color_display_text.color = ft.Colors.RED_500
            hex_display_text.value = "" # Efface le HEX si les coordonnées sont manquantes
            # print("DEBUG: Erreur: Coordonnées de la souris (local_x/y ou x/y) non trouvées dans ControlEvent.")
            page.update()
            return

        # Vérifie si les coordonnées sont dans les limites de l'image PIL
        img_width, img_height = downloaded_pil_image.size
        
        # IMPORTANT: Ceci suppose que l'image Flet n'est PAS redimensionnée par rapport à l'image PIL.
        # Si ft.Image a une taille fixe ou un fit différent, il faudrait un calcul de mise à l'échelle.
        pixel_x = min(max(0, current_x), img_width - 1)
        pixel_y = min(max(0, current_y), img_height - 1)

        try:
            rgb = downloaded_pil_image.getpixel((pixel_x, pixel_y))
            
            # Utilise les valeurs de pixels directement comme R, G, B
            # Si Image.open().convert("RGB") a bien fonctionné, elles devraient être dans cet ordre.
            displayed_r = rgb[0] # Canal Rouge
            displayed_g = rgb[1] # Canal Vert
            displayed_b = rgb[2] # Canal Bleu

            # Convertit RGB en HEX
            hex_color = f"#{displayed_r:02x}{displayed_g:02x}{displayed_b:02x}".upper()


            color_display_text.value = f"Couleur RGB du pixel ({pixel_x}, {pixel_y}): R={displayed_r}, G={displayed_g}, B={displayed_b}"
            color_display_text.color = ft.Colors.WHITE
            hex_display_text.value = f"HEX: {hex_color}"
            hex_display_text.color = ft.Colors.WHITE
        except Exception as getpixel_err:
            color_display_text.value = f"Erreur de lecture pixel: {getpixel_err}"
            color_display_text.color = ft.Colors.ORANGE_300
            hex_display_text.value = "" # Efface le HEX en cas d'erreur
            print(f"ERREUR: Échec de getpixel : {getpixel_err}")
        
        page.update()

    # --- Configuration de l'interface utilisateur ---
    # L'image Flet qui sera affichée
    image_control = ft.Image(
        src=IMAGE_URL,
        width=500, # Définir une largeur fixe pour éviter un redimensionnement excessif et simplifier le mapping
        height=500, # Définir une hauteur fixe
        fit=ft.ImageFit.CONTAIN, # Assure que l'image est contenue dans ces dimensions
        error_content=ft.Text("Impossible de charger l'image", color=ft.Colors.RED_500),
        border_radius=10,
    )

    # GestureDetector pour détecter les événements de la souris sur l'image
    image_gesture_detector = ft.GestureDetector(
        content=image_control,
        on_hover=on_image_hover, # Gère le mouvement de la souris sur l'image
        on_exit=lambda e: (
            setattr(color_display_text, 'value', "Déplacez la souris sur l'image..."),
            setattr(color_display_text, 'color', ft.Colors.WHITE),
            setattr(hex_display_text, 'value', ""), # Efface le HEX quand la souris quitte l'image
            page.update()
        ), # Réinitialise le texte quand la souris quitte l'image
        drag_interval=0, # Active le on_hover/on_mouse_move même avec des mouvements infimes
    )

    # Disposition principale de la page
    page.add(
        ft.Column(
            [
                ft.Text("Couleur du Pixel sous la Souris", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Divider(),
                image_gesture_detector, # Le détecteur de gestes autour de l'image
                color_display_text, # Le texte d'affichage de la couleur RGB
                hex_display_text,   # Le texte d'affichage de la couleur HEX
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

    # --- Lancement du téléchargement de l'image en arrière-plan ---
    # Important : Utiliser page.run_thread pour les opérations bloquantes comme requests.get
    # pour ne pas bloquer l'interface utilisateur de Flet.
    page.run_thread(load_image_for_processing)


# Lance l'application Flet
if __name__ == "__main__":
    ft.app(target=main) # Exécuter en mode application native
