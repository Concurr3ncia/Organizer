import flet as ft
from flet_contrib.color_picker import ColorPicker

languages = ["English", "Spanish", "Portuguese", "French"]

def options_tab(page: ft.Page):
    # Botones Start with Windows y Update on Launch
    start_with_windows_button = ft.Switch(active_color="#b1b2e6",)
    update_on_launch_button = ft.Switch(active_color="#b1b2e6",)


    # Dropdown para cambiar el idioma
    dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(idioma) for idioma in languages],
        border_color="#565782",
        on_change=print("asd"),
        border_radius=10,
        padding=ft.padding.all(5),
        width=page.width * 0.25,  # Fijo el ancho para evitar que cambie
    )


    # Contenedor del cambio de idioma (en la parte derecha)
    change_language_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Select language:", size=20),
                dropdown,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        bgcolor="#3C3D5C",
        width=page.width * 0.2,
        padding=ft.padding.all(10),
        alignment=ft.alignment.top_right,
        height=page.height * 0.17,
        border_radius=10
    )

    # Color picker para el tema
    color_picker_container = ft.Container(
        content=ft.Column(
            controls=[ft.Text("Select color theme:", size=20), ColorPicker(color="#c8df6f")]
        ),
        bgcolor="#3C3D5C",
        width=page.width * 0.26,
        padding=ft.padding.all(10),
        height=page.height * 0.53,
        border_radius=10,
        margin=10
    )

    # Contenedor principal que organiza todo en una fila
    main_container = ft.Container(
        content=ft.Row(
            controls=[
                # Columna izquierda con los botones Start with Windows y Update on Launch
                ft.Column(
                    controls=[
                        ft.Row(controls=[start_with_windows_button, ft.Text("Start with windows", size=12, color=ft.colors.WHITE)]),
                        ft.Row(controls=[update_on_launch_button, ft.Text("Update on launch", size=12, color=ft.colors.WHITE)]),
                        color_picker_container
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,  # Espaciado entre los controles
                ),
                ft.Column(
                    controls=[
                        change_language_container
                    ],
                    alignment=ft.alignment.top_right,
                    horizontal_alignment=ft.MainAxisAlignment.START
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=20,
            width=page.width  # Esto asegura que los elementos se distribuyan correctamente
        ),
        padding=ft.padding.all(15),
        expand=True
    )

    return main_container
