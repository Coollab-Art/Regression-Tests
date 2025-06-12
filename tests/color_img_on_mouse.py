import flet as ft
import requests
from PIL import Image # Nécessite 'Pillow': pip install Pillow
import io
import flet.canvas as cv # Importe le module canvas

# URL de l'image à charger
IMAGE_URL = "https://papers.co/wallpaper/papers.co-vn04-rainbow-color-paint-art-ink-default-pattern-40-wallpaper.jpg"

# Variable globale pour stocker l'image PIL après téléchargement
downloaded_pil_image: Image.Image | None = None

def main(page: ft.Page):
    page.title = "Couleur du Pixel sous la Souris"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 1200 # Augmenter la largeur de la fenêtre pour le canevas
    page.window_height = 700 # Ajuster la hauteur si nécessaire
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

    # Canvas pour recréer le pixel survolé
    # La taille du canevas est proportionnelle à la taille d'affichage de l'image
    # Par exemple, un carré de 50x50 pixels pour représenter le pixel unique
    pixel_canvas_size = 50 
    pixel_canvas = cv.Canvas(
        [
            # Initialement vide, sera rempli dynamiquement
        ],
        width=pixel_canvas_size,
        height=pixel_canvas_size,
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
            page.show_snack_bar(
                ft.SnackBar(
                    ft.Text("Image chargée avec succès ! Passez la souris sur l'image.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_500,
                    open=True
                )
            )
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
        Tente d'obtenir la couleur du pixel à la position de la souris et de l'afficher sur le canevas.
        """
        if downloaded_pil_image is None:
            color_display_text.value = "Image non chargée..."
            color_display_text.color = ft.Colors.RED_300
            hex_display_text.value = "" # Efface le HEX si l'image n'est pas chargée
            pixel_canvas.shapes.clear() # Vide le canevas
            pixel_canvas.update()
            page.update()
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
            hex_display_text.value = "" # Efface le HEX si les coordonnées sont manquantes
            pixel_canvas.shapes.clear() # Vide le canevas
            pixel_canvas.update()
            page.update()
            return

        # Vérifie si les coordonnées sont dans les limites de l'image Flet
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
                hex_display_text.value = ""
                pixel_canvas.shapes.clear() # Vide le canevas si la souris est en dehors de l'image
                pixel_canvas.update()
                page.update()
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
            hex_display_text.value = ""
            pixel_canvas.shapes.clear()
            pixel_canvas.update()
            page.update()
            return

        try:
            rgb = downloaded_pil_image.getpixel((pixel_x, pixel_y))
            
            displayed_r = rgb[0] 
            displayed_g = rgb[1]
            displayed_b = rgb[2]

            hex_color = f"#{displayed_r:02x}{displayed_g:02x}{displayed_b:02x}".upper()

            color_display_text.value = f"Couleur RGB du pixel ({pixel_x}, {pixel_y}): R={displayed_r}, G={displayed_g}, B={displayed_b}"
            color_display_text.color = ft.Colors.WHITE
            hex_display_text.value = f"HEX: {hex_color}"
            hex_display_text.color = ft.Colors.WHITE

            # Dessiner le pixel sur le canevas
            pixel_canvas.shapes.clear() # Efface les anciens dessins
            pixel_canvas.shapes.append(
                cv.Rect(
                    0, 0, # Dessine au coin supérieur gauche du canevas
                    pixel_canvas_size, 
                    pixel_canvas_size,
                    # On passe directement la chaîne HEX comme couleur
                    paint=ft.Paint(style=ft.PaintingStyle.FILL, color=hex_color) 
                )
            )
            pixel_canvas.update() # Mettre à jour le canevas
            
        except Exception as getpixel_err:
            color_display_text.value = f"Erreur de lecture pixel: {getpixel_err}"
            color_display_text.color = ft.Colors.ORANGE_300
            hex_display_text.value = "" # Efface le HEX en cas d'erreur
            pixel_canvas.shapes.clear() # Vide le canevas en cas d'erreur
            pixel_canvas.update()
            print(f"ERREUR: Échec de getpixel : {getpixel_err}")
        
        page.update()

    # --- Configuration de l'interface utilisateur ---
    image_control = ft.Image(
        src=IMAGE_URL,
        width=500, # Largeur fixe pour l'image
        height=500, # Hauteur fixe pour l'image
        fit=ft.ImageFit.CONTAIN, # Assure que l'image est contenue dans ces dimensions
        error_content=ft.Text("Impossible de charger l'image", color=ft.Colors.RED_500),
        border_radius=10,
    )

    image_gesture_detector = ft.GestureDetector(
        content=image_control,
        on_hover=on_image_hover, # Gère le mouvement de la souris sur l'image
        on_exit=lambda e: (
            setattr(color_display_text, 'value', "Déplacez la souris sur l'image..."),
            setattr(color_display_text, 'color', ft.Colors.WHITE),
            setattr(hex_display_text, 'value', ""), # Efface le HEX quand la souris quitte l'image
            pixel_canvas.shapes.clear(), # Vide le canevas
            pixel_canvas.update(),
            page.update()
        ), 
        drag_interval=0, 
    )

    # Disposition principale de la page avec une Row pour l'image et le canevas
    page.add(
        ft.Column(
            [
                ft.Text("Couleur du Pixel sous la Souris", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Divider(),
                ft.Row( # Utilise une Row pour aligner l'image et le canevas horizontalement
                    [
                        ft.Column( # Colonne pour l'image et ses informations
                            [
                                image_gesture_detector, 
                                color_display_text, 
                                hex_display_text,  
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10, # Moins d'espace entre les éléments ici
                        ),
                        ft.VerticalDivider(), # Un diviseur vertical pour séparer les deux parties
                        ft.Column( # Colonne pour le canevas
                            [
                                ft.Text("Pixel survolé", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                pixel_canvas, # Le canevas
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START, # Aligne le haut des colonnes
                    spacing=30, # Espace entre l'image et le canevas
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

    # Lancement du téléchargement de l'image en arrière-plan
    page.run_thread(load_image_for_processing)


# Lance l'application Flet
if __name__ == "__main__":
    ft.app(target=main)