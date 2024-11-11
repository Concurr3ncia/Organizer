import flet as ft

languages = ["English", "Spanish", "Portuguese", "French"]

def options_tab(page: ft.Page):
    dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(idioma) for idioma in languages],
        border_color="#565782",
        on_change=print("asd"),
        expand=True,
        border_radius=10
    )

    change_language_container = ft.Container(
        content=ft.Column(
            controls=[ft.Text("Select language:"), dropdown]
        ),
        bgcolor="#3C3D5C",
        width=page.width * 0.2,
        padding=ft.padding.all(5),
        height=page.height * 0.12,
        border_radius=10
    )

    # Aseguramos que el contenedor se alinee en la esquina superior izquierda
    main_container = ft.Container(
        content=ft.Row(
            controls=[change_language_container],
        ),
        alignment=ft.alignment.top_left  # Aquí especificamos la alineación top_left
    )

    return main_container
