import flet as ft
import subprocess

def obtener_version_windows():
    comando = 'Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object -ExpandProperty Name'
    try:
        cpu_info_raw = subprocess.check_output(["powershell", "-Command", comando]).decode().strip()
        cpu_info = cpu_info_raw.split("|")
        return cpu_info[0]
    except subprocess.CalledProcessError as e:
        return f"Error al obtener información de Windows: {e}"

def obtener_info_cpu():
    comando = 'Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty Name'
    try:
        processor_info_raw = subprocess.check_output(["powershell", "-Command", comando]).decode().strip()
        return processor_info_raw
    except subprocess.CalledProcessError as e:
        return f"Error al obtener información del CPU: {e}"

def obtener_arquitectura_cpu():
    comando = 'Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty Architecture'
    try:
        arquitectura_raw = subprocess.check_output(["powershell", "-Command", comando]).decode().strip()
        arquitectura_map = {
            "0": "x86",
            "1": "MIPS",
            "2": "Alpha",
            "3": "PowerPC",
            "5": "ARM",
            "6": "Itanium-based systems",
            "9": "x64"
        }
        arquitectura = arquitectura_map.get(arquitectura_raw, "Desconocida")
        return arquitectura
    except subprocess.CalledProcessError as e:
        return f"Error al obtener arquitectura del CPU: {e}"

def obtener_info_gpu():
    comando = 'Get-CimInstance -ClassName Win32_VideoController | Select-Object -ExpandProperty Name'
    try:
        gpu_info_raw = subprocess.check_output(["powershell", "-Command", comando]).decode().strip()
        return gpu_info_raw
    except subprocess.CalledProcessError as e:
        return f"Error al obtener información de la GPU: {e}"

def obtener_nombre_equipo():
    comando = 'Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object -ExpandProperty UserName'
    try:
        nombre_equipo = subprocess.check_output(["powershell", "-Command", comando]).decode().strip()
        return nombre_equipo
    except subprocess.CalledProcessError as e:
        return f"Error al obtener el nombre del equipo: {e}"

def obtener_info_ram():
    comando = 'Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object -ExpandProperty TotalPhysicalMemory'
    try:
        ram_info_raw = subprocess.check_output(["powershell", "-Command", comando]).decode().strip()
        ram_total_gb = int(ram_info_raw) / (1024 ** 3)  # Convertir bytes a GB 
        return f'{ram_total_gb:.2f} GB'
    except subprocess.CalledProcessError as e:
        return f"Error al obtener información de la RAM: {e}"

def mostrar_info_general():
    nombre_equipo = obtener_nombre_equipo().split('\\')[-1]  # Obtener solo el nombre del usuario
    info = {
        "Nombre de CPU": obtener_info_cpu(),
        "Arquitectura de CPU": obtener_arquitectura_cpu(),
        "Nombre de la GPU": obtener_info_gpu(),
        "Cantidad de memoria RAM": obtener_info_ram(),
        "Versión del Sistema Operativo": obtener_version_windows(),
        "Nombre del Usuario": nombre_equipo
    }
    return info

def display_hardware_info(page):
    info = mostrar_info_general()
    
    containers = []
    for key, value in info.items():
        container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(key, size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(value, size=16)
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=5,
            ),
            padding=ft.padding.all(10),
            bgcolor="#3C3D5C",
            border_radius=10,
            width=page.width // 3 - 20,
        )
        containers.append(container)

    list_view = ft.ListView(
        controls=containers,
        height=page.height,
        width=page.width,
        padding=ft.padding.all(10),
        spacing=10
    )

    return list_view
