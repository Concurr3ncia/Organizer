import flet as ft
import subprocess
import re
import threading
import concurrent.futures

# Mapear nombres de aplicaciones a identificadores de Winget
apps_identifiers = {
    "WinRar": "RARLab.WinRAR",
    "7-Zip": "7zip.7zip",
    "LibreOffice": "TheDocumentFoundation.LibreOffice",
    "Adobe Reader": "Adobe.Acrobat.Reader.64-bit",
    "MSI Afterburner": "Guru3D.Afterburner",
    "LightShot": "Skillbrains.Lightshot",
    ".NET Framework": "Microsoft.DotNet.Framework.DeveloperPack_4",
    "CCleaner": "Piriform.CCleaner",
    "Driver Booster": "IObit.DriverBooster",
    "Malwarebytes": "Malwarebytes.Malwarebytes",
    "Revo Uninstaller": "RevoUninstaller.RevoUninstaller",
    "TeamViewer": "TeamViewer.TeamViewer",
    "OPAutoClicker": "OPAutoClicker.OPAutoClicker",
    "Discord": "Discord.Discord",
    "Steam": "Valve.Steam",
    "Epic Games": "EpicGames.EpicGamesLauncher",
    "OBS": "OBSProject.OBSStudio",
    "Spotify": "Spotify.Spotify",
    "Zoom": "Zoom.Zoom",
    "Skype": "Microsoft.Skype",
    "Slack": "SlackTechnologies.Slack",
    "Microsoft Teams": "Microsoft.Teams",
    "Google Chrome": "Google.Chrome",
    "Brave": "Brave.Brave",
    "Firefox": "Mozilla.Firefox",
    "Opera": "Opera.Opera",
    "Microsoft Edge": "Microsoft.Edge",
    "Tor": "TorProject.TorBrowser",
    "Vivaldi": "Vivaldi.Vivaldi",
    "Yandex": "Yandex.Browser",
    "VSCode": "Microsoft.VisualStudioCode",
    #"Python": "Python.Python.3",
    "Notepad++": "Notepad++.Notepad++",
    "Sublime Text": "SublimeHQ.SublimeText.4",
    "WinSCP": "WinSCP.WinSCP",
    "GitHub": "GitHub.GitHubDesktop",
    "Atom": "GitHub.Atom",
    "XAMPP": "ApacheFriends.Xampp.8.2",
    "Git": "Git.Git",
    "PyCharm": "JetBrains.PyCharm.Community",
    "Docker": "Docker.DockerDesktop",
    "Postman": "Postman.Postman",
    "Notion": "Notion.Notion",
    "Adobe Photoshop": "XPFD4T9N395QN6",
    "GIMP": "GIMP.GIMP",
    "Audacity": "Audacity.Audacity",
    "Shotcut": "Meltytech.Shotcut",
    "Blender": "BlenderFoundation.Blender",
    "Camtasia": "TechSmith.Camtasia",
    "Krita": "KDE.Krita",
    "Inkscape": "Inkscape.Inkscape",
    "Filmora": "Wondershare.Filmora",
    "OBS Studio": "OBSProject.OBSStudio",
    "Bandicam": "BandicamCompany.Bandicam",
    "Streamlabs": "Streamlabs.StreamlabsOBS"
}

apps_categories = {
    "System": {"WinRar", "7-Zip", "LibreOffice", "Adobe Reader", "MSI Afterburner", "LightShot", ".NET Framework", "CCleaner", "Driver Booster", "Malwarebytes", "Revo Uninstaller", "TeamViewer", "OPAutoClicker"},
    "Internet": {"Discord", "Steam", "Epic Games", "OBS", "Spotify", "Zoom", "Skype", "Slack", "Microsoft Teams"},
    "Browsers": {"Google Chrome", "Brave", "Firefox", "Opera", "Microsoft Edge", "Tor", "Vivaldi", "Yandex"},
    "Coding": {"VSCode", "Notepad++", "Sublime Text", "WinSCP", "GitHub", "Atom", "XAMPP", "Git", "PyCharm", "Docker", "Postman", "Notion"},
    "Editing": {"GIMP", "Audacity", "Shotcut", "Blender", "Camtasia", "Krita", "Inkscape", "Filmora"},
    "Record": {"OBS Studio", "Bandicam", "Streamlabs"},
}

def get_app_url(app_id):
    print(f"Consultando URL para: {app_id}")
    try:
        result = subprocess.run(
            ["winget", "show", app_id],
            capture_output=True, text=True, check=True, encoding="utf-8"
        )
        
        if result.stdout:
            lines = result.stdout.splitlines()
            for line in lines:
                if "URL" in line and "editor" in line.lower():
                    match = re.search(r"https?://[^\s]+", line)
                    if match:
                        return match.group(0)
        else:
            print(f"Error: No se encontró información en la salida de winget para {app_id}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando winget para {app_id}: {e}")
        return None
    except UnicodeDecodeError as e:
        print(f"Error de decodificación al ejecutar winget para {app_id}: {e}")
        return None

def fetch_all_urls():
    # Usamos un ThreadPoolExecutor para hacer las consultas de forma concurrente
    app_ids = list(apps_identifiers.values())  # Lista de identificadores de aplicaciones
    urls = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Ejecutamos las consultas de manera concurrente
        future_to_app = {executor.submit(get_app_url, app_id): app_id for app_id in app_ids}
        for future in concurrent.futures.as_completed(future_to_app):
            app_id = future_to_app[future]
            try:
                url = future.result()
                if url:
                    urls[app_id] = url
            except Exception as exc:
                print(f"Error obteniendo URL para {app_id}: {exc}")
    
    return urls

def apps_tab(page: ft.Page):
    urls = fetch_all_urls()  # Obtener las URLs de manera concurrente
    rows = []
    container_width = 220
    container_height = 440
    checkboxes = []

    # Crear una fila para contener todas las categorías
    category_row = []

    # Para cada categoría, crea un contenedor y añádelo a la fila
    for category, apps in apps_categories.items():
        category_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(category, size=18, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Image(
                                        src=f"https://logo.clearbit.com/{urls.get(apps_identifiers[app], '#')}",
                                        width=15, height=15
                                    ),
                                    ft.Checkbox(label=app, value=False),
                                    ft.IconButton(
                                        icon=ft.icons.LINK,
                                        tooltip="Open Website",
                                        on_click=lambda e, app=app: page.launch_url(urls.get(apps_identifiers[app], "#")),
                                        scale=0.8
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=0
                            ) for app in apps
                        ],
                        alignment=ft.alignment.center,
                        spacing=0,
                        scroll=ft.ScrollMode.ALWAYS,  # Habilitar el scroll dentro de esta columna
                        height=container_height - 70,
                    )
                ],
                alignment=ft.alignment.center,
            ),
            width=container_width,
            height=container_height * 0.98,
            padding=ft.padding.only(left=10, top=10),
            border_radius=10,
            bgcolor="#3C3D5C",
            border=ft.border.only(bottom=ft.border.BorderSide(3, "#313252")),
            animate=ft.animation.Animation(duration=300, curve="easeInOut")
        )
        category_row.append(category_container)

    # Ahora colocamos todas las categorías en un Row que tendrá scroll horizontal
    app_container = ft.Container(
        content=ft.Row(
            controls=category_row,
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS  # Activamos el scroll horizontal aquí
        ),
        expand=True,  # Expande para que ocupe el espacio disponible
        padding=ft.padding.only(left=10, top=5)
    )


    progress_bar = ft.ProgressBar(width=400)
    progress_bar.value = 0
    current_task_text = ft.Text("")

    def update_progress_bar(progress, task):
        progress_bar.value = progress
        current_task_text.value = f"{task} {progress}%"

    def run_winget_commands(commands):
        total_apps = len(commands)
        current_app_index = 0

        for command in commands:
            app_name = command.split(" ")[3]  # Obtener el nombre de la app
            current_app_index += 1
            update_progress_bar(0, f"Installing {app_name}")
            
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            for stdout_line in iter(process.stdout.readline, ""):
                # Aquí, intenta obtener el progreso de la salida de winget
                if "%" in stdout_line:
                    try:
                        progress = int(stdout_line.split()[0].replace('%', ''))
                        update_progress_bar(progress, f"Installing {app_name}")
                    except ValueError:
                        continue

            process.stdout.close()
            process.wait()

            if process.returncode != 0:
                current_task_text.value = f"Error: {app_name} failed"
                break

        update_progress_bar(100, "Completed")

    def handle_download(_):
        selected_apps = [cb.label for cb in checkboxes if cb.value]
        commands = [f"winget install --id {apps_identifiers[app]}" for app in selected_apps if apps_identifiers[app]]
        threading.Thread(target=run_winget_commands, args=(commands,)).start()

    def handle_uninstall(_):
        selected_apps = [cb.label for cb in checkboxes if cb.value]
        commands = [f"winget uninstall --id {apps_identifiers[app]}" for app in selected_apps if apps_identifiers[app]]
        threading.Thread(target=run_winget_commands, args=(commands,)).start()

    download_button = ft.ElevatedButton(
        text="Download",
        icon=ft.icons.DOWNLOAD,
        on_click=handle_download
    )

    uninstall_button = ft.ElevatedButton(
        text="Uninstall",
        icon=ft.icons.DELETE,
        on_click=handle_uninstall
    )

    buttons_container = ft.Row(
        controls=[download_button, uninstall_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    download_and_progressbar = ft.Column(
        controls=[current_task_text, progress_bar, buttons_container],
        alignment=ft.alignment.center,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Column(
        controls=[app_container, download_and_progressbar],
        alignment=ft.alignment.center,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )