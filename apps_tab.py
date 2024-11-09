import flet as ft
import subprocess

apps_categories = {
    "System": {"WinRar", "7-Zip", "LibreOffice", "Adobe Reader", "MSI Afterburner", "LightShot", ".NET Framework", "CCleaner", "Driver Booster", "Malwarebytes", "Revo Uninstaller", "TeamViewer","OPautoclicker"},
    "Internet": {"Discord", "Steam", "Epic Games", "OBS", "Spotify", "Zoom", "Skype", "Slack", "Twitch", "Facebook Messenger", "Microsoft Teams"},
    "Browsers": {"Google Chrome", "Brave", "Firefox", "Opera", "Microsoft Edge", "Tor", "Safari", "Vivaldi", "Midori", "Yandex"},
    "Coding": {"VSCode", "Python", "Notepad++", "Sublime Text", "WinSCP", "GitHub", "Atom", "XAMPP", "Git", "PyCharm", "Eclipse", "Docker", "Postman", "Notion"},
    "Editing": {"Adobe Photoshop", "GIMP", "Adobe Premiere Pro", "DaVinci Resolve", "Audacity", "Lightroom", "Shotcut", "Final Cut Pro", "Blender", "Camtasia", "Vegas Pro", "Krita", "Inkscape", "Filmora"},
    "Record": {"OBS Studio", "Bandicam", "Camtasia", "ScreenFlow", "NVIDIA ShadowPlay", "XSplit", "TinyTake", "FlashBack Express", "Streamlabs"},
}

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