import flet as ft

def main(page: ft.Page):
    # Configuration de la page Flet
    page.title = "Suivi de Souris"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = ft.Colors.BLUE_GREY_900 
    
    # Contrôle de texte qui va suivre la souris
    mouse_follower_text_content = ft.Text(
        value="Je te suis !",
        color=ft.Colors.YELLOW_ACCENT_400, 
        size=20,
        weight=ft.FontWeight.BOLD
    )

    # Crée un ft.Container qui va contenir le texte et sera positionné.
    # C'est ce Container qui aura les propriétés 'left' et 'top' pour le positionnement absolu.
    mouse_follower_container = ft.Container(
        content=mouse_follower_text_content,
        left=0, # Position initiale
        top=0,  # Position initiale
        # Optionnel: définir une taille pour le conteneur si le texte est très petit,
        # et aligner le texte à l'intérieur de ce conteneur.
        # width=150,
        # height=30,
        alignment=ft.alignment.center # Centre le texte à l'intérieur du conteneur
    )

    def update_text_position(e: ft.ControlEvent):
        """
        Met à jour la position du conteneur de texte en fonction des coordonnées de la souris.
        L'événement 'on_hover' (ou 'on_mouse_move') de GestureDetector fournit bien local_x et local_y.
        """
        # Pour ft.GestureDetector.on_hover, 'e.local_x' et 'e.local_y' sont fiables.
        # Plus besoin des vérifications hasattr complexes car GestureDetector est conçu pour ça.
        current_x = e.local_x
        current_y = e.local_y

        # Ajuste la position pour centrer le texte approximativement sous le curseur.
        # Ces offsets peuvent nécessiter un ajustement fin en fonction de la taille réelle du texte/conteneur.
        offset_x = mouse_follower_text_content.size * 0.5 
        offset_y = mouse_follower_text_content.size * 0.5
        
        # Met à jour les propriétés 'left' et 'top' du conteneur qui suit la souris.
        mouse_follower_container.left = current_x - offset_x
        mouse_follower_container.top = current_y - offset_y
        
        # Met à jour la page pour refléter le nouveau positionnement du texte.
        # C'est crucial pour que les changements soient rendus à l'écran.
        page.update()

    # Crée un GestureDetector qui couvrira toute la zone d'écoute.
    # L'événement 'on_hover' de GestureDetector est celui qui fournit les coordonnées de manière fiable.
    # Alternativement, on pourrait utiliser 'on_mouse_move' si tu veux des événements continus
    # même quand la souris ne "survole" pas activement (par exemple, si elle est immobile dans la zone).
    # Pour un suivi simple, 'on_hover' (qui se déclenche à chaque mouvement de la souris dans la zone) est suffisant.
    mouse_tracker_detector = ft.GestureDetector(
        on_hover=lambda e: update_text_position(e), # Utilise on_hover ici
        # Le contenu du GestureDetector est un Stack pour positionner le texte.
        content=ft.Stack(
            controls=[mouse_follower_container],
            expand=True # Permet au Stack de prendre tout l'espace disponible
        ),
        expand=True # Permet au GestureDetector de prendre tout l'espace disponible
    )

    # Ajoute le GestureDetector (qui contient le Stack et le texte) à la page Flet.
    page.add(mouse_tracker_detector)

# Lance l'application Flet.
if __name__ == "__main__":
    ft.app(target=main)

