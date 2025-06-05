import flet as ft

def main(page: ft.Page):
    # Configuration de la page Flet
    page.title = "Suivi de Souris avec Containers"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = ft.Colors.BLUE_GREY_900 

    # Contrôle de texte qui va suivre la souris
    follower_text = ft.Text(
        value="Je te suis !",
        color=ft.Colors.YELLOW_ACCENT_400, 
        size=20,
        weight=ft.FontWeight.BOLD
    )

    # Conteneur pour le texte suiveur, initialement invisible
    follower_container = ft.Container(
        content=follower_text,
        left=0, top=0, # Position initiale (sera mise à jour si les coordonnées sont disponibles)
        alignment=ft.alignment.center, # Centre le texte à l'intérieur du conteneur
        visible=False # Commence invisible
    )

    # --- Fonctions pour gérer la visibilité du texte suiveur ---
    def hide_follower_text(e: ft.ControlEvent):
        """
        Rend le conteneur suiveur invisible et met à jour la page.
        Ne change l'état que si c'est nécessaire pour éviter les mises à jour inutiles.
        """
        if follower_container.visible:
            # print(f"DEBUG: Hiding follower text. Event from: {e.control.content.value if hasattr(e.control, 'content') else 'GLOBAL_EXIT'}")
            follower_container.visible = False
            page.update()

    def show_follower_text(e: ft.ControlEvent):
        """
        Rend le conteneur suiveur visible et met à jour la page.
        Ne change l'état que si c'est nécessaire.
        """
        if not follower_container.visible:
            # print(f"DEBUG: Showing follower text. Event from: {e.control.content.value if hasattr(e.control, 'content') else 'UNKNOWN'}")
            follower_container.visible = True
            page.update()

    # --- Fonction pour mettre à jour la position du texte suiveur ---
    def update_follower_position(e: ft.ControlEvent):
        """
        Tente de mettre à jour la position du conteneur de texte en fonction des coordonnées de la souris.
        Gère l'absence d'attributs de coordonnées dans l'objet ControlEvent.
        """
        current_x = None
        current_y = None

        # Tente d'obtenir les coordonnées locales (préférable pour GestureDetector)
        if hasattr(e, 'local_x') and hasattr(e, 'local_y'):
            current_x = e.local_x
            current_y = e.local_y
        # Fallback aux coordonnées globales si les locales sont absentes
        elif hasattr(e, 'x') and hasattr(e, 'y'):
            current_x = e.x
            current_y = e.y
            # print("DEBUG: Avertissement: Utilisation de e.x et e.y (coordonnées globales) au lieu de local_x et local_y.")
        
        # Si aucune coordonnée n'a pu être obtenue, on ne peut pas suivre la souris
        if current_x is None or current_y is None:
            # print("DEBUG: Erreur: Coordonnées de la souris (local_x/y ou x/y) non trouvées dans ControlEvent. Impossible de mettre à jour la position.")
            return # Sort de la fonction si les coordonnées ne sont pas disponibles

        # Ajuste la position pour centrer le texte approximativement sous le curseur.
        offset_x = follower_text.size * 0.5 
        offset_y = follower_text.size * 0.5
        
        follower_container.left = current_x - offset_x
        follower_container.top = current_y - offset_y
        
        # Mets à jour la page uniquement si le texte est visible pour éviter des mises à jour inutiles
        # et si les coordonnées sont disponibles
        if follower_container.visible:
            page.update()

    # --- Les deux conteneurs d'interaction ---
    # Container One: Enveloppé dans un GestureDetector pour gérer on_hover et on_exit
    container_one_content = ft.Container(
        width=250,
        height=250,
        bgcolor=ft.Colors.RED_ACCENT_700, # Rouge pour cacher le texte
        content=ft.Text("Container 1 (Cache le texte)"),
        alignment=ft.alignment.center,
    )
    gesture_detector_one = ft.GestureDetector(
        content=container_one_content,
        on_hover=hide_follower_text, # Cache le texte quand la souris est ici
        on_exit=hide_follower_text, # Cache le texte quand la souris quitte ce container
    )

    # Container Two: Enveloppé dans un GestureDetector pour gérer on_hover et on_exit
    container_two_content = ft.Container(
        width=250,
        height=250,
        bgcolor=ft.Colors.GREEN_ACCENT_700, # Vert pour faire suivre le texte
        content=ft.Text("Container 2 (Fait suivre le texte)"),
        alignment=ft.alignment.center,
    )
    gesture_detector_two = ft.GestureDetector(
        content=container_two_content,
        on_hover=show_follower_text, # Montre le texte quand la souris est ici
        on_exit=hide_follower_text, # Cache le texte quand la souris quitte ce container
    )
    
    # --- Disposition principale des conteneurs ---
    main_layout_content = ft.Column(
        [
            gesture_detector_one, # Utilise le GestureDetector pour container_one
            gesture_detector_two  # Utilise le GestureDetector pour container_two
        ],
        spacing=20, # Espacement entre les deux conteneurs
        alignment=ft.MainAxisAlignment.CENTER, # Centre les conteneurs verticalement
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centre les conteneurs horizontalement
        expand=True # Permet à la colonne de prendre l'espace disponible
    )

    # --- GestureDetector global pour la détection de mouvement de la souris ---
    # Il englobe toute la zone où le texte peut potentiellement suivre (quand il est visible).
    # Revert to on_hover, as on_mouse_move is not a direct parameter.
    gesture_detector_area = ft.GestureDetector(
        on_hover=update_follower_position, # Revert: utilise on_hover pour les mises à jour de position
        on_exit=hide_follower_text, # Cache le texte si la souris quitte entièrement la zone du GestureDetector
        content=ft.Stack(
            controls=[
                main_layout_content, # Contient container_one et container_two (maintenant enveloppés dans GestureDetectors)
                follower_container # Le texte suiveur, qui est au-dessus des autres conteneurs
            ],
            expand=True # Le Stack prend tout l'espace disponible
        ),
        expand=True # Le GestureDetector lui-même prend tout l'espace disponible sur la page
    )
    
    # Ajoute le GestureDetector (qui contient toute la logique) à la page Flet.
    page.add(gesture_detector_area)

# Lance l'application Flet.
if __name__ == "__main__":
    ft.app(target=main)

