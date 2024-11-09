import flet as ft

def system_optimization_function_1():
    print("System optimization function 1 executed.")

def system_optimization_function_2():
    print("System optimization function 2 executed.")

def display_optimization_options(page: ft.Page):
    def create_switch(label, on_change):
        return ft.Row(
            controls=[
                ft.Switch(
                    value=False,
                    on_change=on_change,
                    active_color=ft.colors.GREEN,
                    scale=0.75
                ),
                ft.Text(label, size=12, color=ft.colors.WHITE)
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,  # Minimal space between switch and label
        )

    def create_container(title, switches):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Column(
                        controls=switches,
                        spacing=0,  # Minimal space between switches
                        alignment=ft.MainAxisAlignment.START
                    )
                ],
                spacing=5,  # Minimal space between title and switches
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.all(10),  # Add small padding inside container
            margin=ft.margin.all(10),  # Margin to create space between containers
            border_radius=10,
            bgcolor="#3C3D5C",
            alignment=ft.alignment.top_center,
            expand=True,  # Allow container to expand vertically based on content
            width=page.width / 3 - 20,  # Adjust width based on page size
        )

    # Define the switches for each category
    system_switches = [
        create_switch("Restore Classic File Explorer", lambda e: system_optimization_function_1()),
        create_switch("Hide Taskbar Weather", lambda e: system_optimization_function_2()),
        create_switch("Hide Taskbar Search", lambda e: system_optimization_function_2()),
        create_switch("Disable My People", lambda e: system_optimization_function_2()),
        create_switch("Enable Long Paths", lambda e: system_optimization_function_2()),
        create_switch("Disable TPM Check", lambda e: system_optimization_function_2()),
        create_switch("Disable Sensor Services", lambda e: system_optimization_function_2()),
        create_switch("Remove Cast to Device", lambda e: system_optimization_function_2()),
        create_switch("Disable Virtualization Based Security", lambda e: system_optimization_function_2()),
        create_switch("Restore Classic Photo Viewer", lambda e: system_optimization_function_2()),
        create_switch("Disable Modern Standby", lambda e: system_optimization_function_2()),
    ]
    
    windows_update_switches = [
        create_switch("Disable Automatic Updates", lambda e: system_optimization_function_1()),
        create_switch("Disable Microsoft Store Updates", lambda e: system_optimization_function_2()),
        create_switch("Disable Insider Service", lambda e: system_optimization_function_2()),
        create_switch("Exclude Drivers from Updates", lambda e: system_optimization_function_2()),
    ]

    taskbar_switches = [
        create_switch("Align Taskbar to Left", lambda e: system_optimization_function_1())
    ]

    privacy_switches = [
        create_switch("Disable Telemetry Services", lambda e: system_optimization_function_1()),
        create_switch("Disable Cortana", lambda e: system_optimization_function_2()),
        create_switch("Enhance Privacy", lambda e: system_optimization_function_2()),
        create_switch("Disable News & Interests", lambda e: system_optimization_function_2()),
        create_switch("Disable Start Menu Ads", lambda e: system_optimization_function_2()),
        create_switch("Disable Edge Telemetry", lambda e: system_optimization_function_2()),
        create_switch("Disable Edge Discover", lambda e: system_optimization_function_2()),
    ]

    gaming_switches = [
        create_switch("Enable Gaming Mode", lambda e: system_optimization_function_1()),
        create_switch("Disable Xbox Live", lambda e: system_optimization_function_2()),
        create_switch("Disable Game Bar", lambda e: system_optimization_function_2()),
    ]

    touch_switches = [
        create_switch("Disable Windows Ink", lambda e: system_optimization_function_1()),
        create_switch("Disable Spell Checking", lambda e: system_optimization_function_2()),
        create_switch("Disable Cloud Clipboard", lambda e: system_optimization_function_2()),
    ]

    extras_switches = [
        create_switch("Disable Snap Assist", lambda e: system_optimization_function_1()),
    ]

    # Create containers for each category
    containers = [
        create_container("System", system_switches),
        create_container("Windows Update", windows_update_switches),
        create_container("Taskbar", taskbar_switches),
        create_container("Privacy", privacy_switches),
        create_container("Gaming", gaming_switches),
        create_container("Touch", touch_switches),
        create_container("Extras", extras_switches),
    ]

    # Create rows by grouping containers into 3 per row
    rows = []
    for i in range(0, len(containers), 4):
        row_controls = containers[i:i+4]
        
        # Adjusting each row's container for even alignment
        while len(row_controls) < 3:
            row_controls.append(
                ft.Container(content=ft.Column(), expand=True)
            )
        
        rows.append(
            ft.Row(
                controls=row_controls,  # Agrupar los contenedores de a 3 por fila
                alignment=ft.MainAxisAlignment.START,  # Alineamos los contenedores desde el inicio de la fila
                spacing=10,  # Espacio entre contenedores
                vertical_alignment=ft.CrossAxisAlignment.START,  # Alineación al tope
            )
        )

    # Usamos ListView para hacerlo desplazable
    main_container = ft.ListView(
        controls=rows,
        expand=True,
        padding=ft.padding.all(10)
    )

    return main_container
