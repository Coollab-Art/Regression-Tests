import flet as ft
import threading
import time


def main(page: ft.Page):
    page.title = "Traitement progressif"
    items_column = ft.Column()
    progress_bar = ft.ProgressBar(width=400, value=0)
    process_button = ft.ElevatedButton(text="Lancer le traitement")
    rows = []

    def process_data():
        process_button.disabled = True
        total = 10
        items_column.controls.clear()
        rows.clear()
        page.update()

        for i in range(total):
            # Crée la ligne avec une barre de progression individuelle
            item_text = ft.Text(f"Traitement de l'élément {i + 1}...")
            item_bar = ft.ProgressBar(width=100, value=0.5)
            row = ft.Row([item_text, item_bar])
            rows.append((item_text, item_bar, row))
            items_column.controls.append(row)
            page.update()

            time.sleep(0.5)  # Simule le traitement

            # Mise à jour : traitement terminé
            item_text.value = f"Élément {i + 1} traité"
            check_icon = ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=20)
            rows[i][2].controls[1] = check_icon  # Remplace la barre par l'icône
            progress_bar.value = (i + 1) / total
            page.update()

        process_button.disabled = False
        page.update()

    def on_click(e):
        threading.Thread(target=process_data).start()

    process_button.on_click = on_click

    page.add(
        ft.Column(
            [
                process_button,
                progress_bar,
                ft.Divider(),
                items_column,
            ]
        )
    )


ft.app(target=main)
