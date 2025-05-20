import flet as ft

def main(page: ft.Page):
    page.title = "Coollab regression test"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    def button_clicked(e):
        page.add(ft.Text("Clicked!"))

    t = ft.Text(value="Hello, world!", color="green")

    def add_clicked(e):
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        new_task.focus()
        new_task.update()

    new_task = ft.TextField(hint_text="What's needs to be done?", width=300)

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        t,
        ft.Row(controls=[
            ft.TextField(label="Your name"),
            ft.ElevatedButton(text="Say my name!", on_click=button_clicked)
        ]),
        ft.Row([new_task, ft.ElevatedButton("Add", on_click=add_clicked)])
    )

ft.app(main)