import flet as ft
import time
import subprocess

def main(page: ft.Page):
    page.window.maximized = True
    page.bgcolor = "#30303d"
    page.title = "Organizer"

    apps_categories = {
        "System": {"WinRar", "7-Zip", "LibreOffice", "Adobe Reader", "MSI Afterburner", "LightShot", ".NET Framework", "CCleaner", "Driver Booster", "Malwarebytes", "Revo Uninstaller", "TeamViewer"},
        "Internet": {"Discord", "Steam", "Epic Games", "OBS", "Spotify", "Zoom", "Skype", "Slack", "Twitch", "Facebook Messenger", "Microsoft Teams"},
        "Browsers": {"Google Chrome", "Brave", "Firefox", "Opera", "Microsoft Edge", "Tor", "Safari", "Vivaldi", "Midori", "Yandex"},
        "Coding": {"VSCode", "Python", "Notepad++", "Sublime Text", "WinSCP", "GitHub", "Atom", "XAMPP", "Git", "PyCharm", "Eclipse", "Docker", "Postman", "Notion"},
        "Editing": {"Adobe Photoshop", "GIMP", "Adobe Premiere Pro", "DaVinci Resolve", "Audacity", "Lightroom", "Shotcut", "Final Cut Pro", "Blender", "Camtasia", "Vegas Pro", "Krita", "Inkscape", "Filmora"},
        "Record": {"OBS Studio", "Bandicam", "Camtasia", "ScreenFlow", "NVIDIA ShadowPlay", "XSplit", "TinyTake", "FlashBack Express", "Streamlabs"},
    }

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(name=ft.icons.FOLDER),
                ft.Text("Organizer", size=20, weight=ft.FontWeight.BOLD)
            ]
        ),
        padding=ft.padding.only(left=10, top=10),
        alignment=ft.alignment.top_left
    )

    def create_menu_item(icon_name, label, tab_content):
        is_hovered = False
        text = None

        def on_hover(e):
            nonlocal is_hovered, text
            if e.data == "true" and not is_hovered:
                text = ft.Stack(
                    [
                        ft.Text(
                            spans=[
                                ft.TextSpan(
                                    label,
                                    ft.TextStyle(
                                        weight=ft.FontWeight.BOLD,
                                        foreground=ft.Paint(
                                            color=ft.colors.GREY_100,
                                            stroke_width=1,
                                            stroke_join=ft.StrokeJoin.ROUND
                                        ),
                                    ),
                                ),
                            ],
                        ),
                        ft.Text(
                            spans=[
                                ft.TextSpan(
                                    label,
                                    ft.TextStyle(
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.WHITE,
                                    ),
                                ),
                            ],
                        ),
                    ]
                )
                e.control.content.controls.append(text)
                label_width = len(label) * 8
                e.control.width = 50 + label_width + 20
                menu.width = 360 + label_width + 20
                child_container.width = 360 + label_width + 20
                e.control.bgcolor = "#9a9bb5"
                is_hovered = True
            elif e.data == "false" and is_hovered:
                e.control.content.controls.pop()
                menu.width = 360
                child_container.width = 360
                e.control.width = 50
                e.control.bgcolor = "#5D5F92"
                is_hovered = False
            menu.update()
            child_container.update()
            e.control.update()

        def on_click(e):
            e.control.scale = ft.Scale(scale=0.9)
            e.control.update()
            switch_tab(tab_content)
            page.update()
            time.sleep(0.1)
            e.control.scale = ft.Scale(scale=1.0)
            e.control.update()

        return ft.Container(
            content=ft.Row(
                controls=[ft.Icon(name=icon_name, color=ft.colors.WHITE, size=30)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=50,
            height=35,
            bgcolor="#5D5F92",
            border_radius=10,
            alignment=ft.alignment.center,
            on_click=on_click,
            on_hover=on_hover,
            animate=ft.animation.Animation(duration=300, curve="easeInOut")
        )

    def apps_tab():
        rows = []
        container_width = 200
        container_height = 500
        checkboxes = []

        row = []
        for category, apps in apps_categories.items():
            category_container = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(category, size=18, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                        ft.Column(
                            controls=[
                                ft.Checkbox(label=app, value=False) for app in apps
                            ],
                            alignment=ft.alignment.center,
                            spacing=5,
                            scroll=ft.ScrollMode.ALWAYS,
                            height=container_height - 10,
                        ),
                    ],
                    alignment=ft.alignment.center,
                    spacing=10,
                ),
                width=container_width,
                height=container_height,
                padding=ft.padding.only(left=10, top=10),
                border_radius=10,
                bgcolor="#3C3D5C",
                border=ft.border.only(bottom=ft.border.BorderSide(3, "#313252")),
                animate=ft.animation.Animation(duration=300, curve="easeInOut")
            )

            shadow_categories = ft.Container(
                width=container_width,
                height=container_height + 10,
                border_radius=10,
                bgcolor="#3C3D5C",
                content=category_container,
                animate=ft.animation.Animation(duration=300, curve="easeInOut"),
                border=ft.border.only(bottom=ft.border.BorderSide(3.5, "#1B1C30")),
            )

            row.append(shadow_categories)

            if len(row) == 10:
                rows.append(ft.Row(controls=row, alignment=ft.MainAxisAlignment.CENTER, spacing=10))
                row = []

            for app_checkbox in category_container.content.controls[1].controls:
                checkboxes.append(app_checkbox)

        if row:
            rows.append(ft.Row(controls=row, alignment=ft.MainAxisAlignment.CENTER, spacing=10))

        app_container = ft.Column(
            controls=rows,
            alignment=ft.alignment.center,
            expand=True,
        )

        progress_bar = ft.ProgressBar(width=400)
        progress_bar.value = 0
        current_task_text = ft.Text("")

        download_button = ft.ElevatedButton(
            text="Download",
            on_click=lambda e: manage_apps(checkboxes, "install", progress_bar, current_task_text)
        )

        uninstall_button = ft.ElevatedButton(
            text="Uninstall",
            on_click=lambda e: manage_apps(checkboxes, "uninstall", progress_bar, current_task_text)
        )

        buttons_container = ft.Row(
            controls=[download_button, uninstall_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        return ft.Column(
            controls=[app_container, current_task_text, progress_bar, buttons_container],
            alignment=ft.alignment.center,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    def manage_apps(checkboxes, action, progress_bar, current_task_text):
        selected_apps = [checkbox.label for checkbox in checkboxes if checkbox.value]
        total_apps = len(selected_apps)
        progress_step = 1 / total_apps if total_apps else 0

        progress_bar.value = 0
        progress_bar.update()

        for idx, app in enumerate(selected_apps):
            try:
                current_task_text.value = f"{app} ({idx + 1}/{total_apps}) - {int((idx + 1) / total_apps * 100)}%"
                current_task_text.update()
                if action == "install":
                    subprocess.run(["choco", action, app, "-y", "--force"], check=True)
                else:
                    subprocess.run(["choco", action, app, "-y"], check=True)
                print(f"Successfully {action}ed {app}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to {action} {app}: {e}")
            
            progress_bar.value += progress_step
            progress_bar.update()

        current_task_text.value = "Completed!"
        current_task_text.update()
        progress_bar.value = 1
        progress_bar.update()

    tabs_content = {
        "Windows": ft.Text("Windows Content", size=24, color=ft.colors.WHITE),
        "Apps": apps_tab(),
        "Utilities": ft.Text("Utilities Content", size=24, color=ft.colors.WHITE),
        "Hardware": ft.Text("Hardware Content", size=24, color=ft.colors.WHITE),
        "Restart": ft.Text("Restart Content", size=24, color=ft.colors.WHITE),
        "Options": ft.Text("Options Content", size=24, color=ft.colors.WHITE)
    }

    iconos_menu = [
        create_menu_item(ft.icons.WINDOW_ROUNDED, "Home", tabs_content["Windows"]),
        create_menu_item(ft.icons.APPS, "Apps", tabs_content["Apps"]),
        create_menu_item(ft.icons.SETTINGS, "Utilities", tabs_content["Utilities"]),
        create_menu_item(ft.icons.HARDWARE_ROUNDED, "Hardware", tabs_content["Hardware"]),
        create_menu_item(ft.icons.RESTART_ALT_ROUNDED, "Restart", tabs_content["Restart"]),
        create_menu_item(ft.icons.SETTINGS_ROUNDED, "Options", tabs_content["Options"])
    ]

    child_container = ft.Container(
        content=ft.Row(
            controls=iconos_menu,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        alignment=ft.alignment.center,
        width=page.width * 0.285,
        height=50,
        border_radius=10,
        bgcolor="#3C3D5C",
        border=ft.border.only(bottom=ft.border.BorderSide(3, "#313252")),
        animate=ft.animation.Animation(duration=300, curve="easeInOut")
    )

    menu = ft.Container(
        alignment=ft.alignment.center,
        width=page.width * 0.285,
        height=50,
        border_radius=10,
        bgcolor="#1B1C30",
        border=ft.border.only(bottom=ft.border.BorderSide(3.5, "#1B1C30")),
        content=child_container,
        animate=ft.animation.Animation(duration=300, curve="easeInOut")
    )

    tab_content_container = ft.Container(
        width=page.width,
        height=page.height - 100,
        alignment=ft.alignment.center,
        animate=ft.animation.Animation(duration=300, curve="easeInOut")
    )

    def switch_tab(content):
        tab_content_container.content = content
        tab_content_container.update()

    main_container = ft.Column(
        controls=[
            header,
            ft.Container(content=tab_content_container, alignment=ft.alignment.center, expand=True),
            ft.Container(content=menu, alignment=ft.alignment.bottom_center)
        ],
        alignment=ft.alignment.top_center,
        expand=True,
    )

    page.add(main_container)
    page.update()
    switch_tab(tabs_content["Windows"])

ft.app(target=main)
