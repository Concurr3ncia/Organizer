import flet as ft
import subprocess

def obtener_info_cpu():
    comando = 'Get-CimInstance -ClassName Win32_Processor'
    try:
        cpu_raw = subprocess.check_output(["powershell", "-Command", comando], stderr=subprocess.PIPE)
        cpu_info = {}
        for line in cpu_raw.decode('latin1').strip().splitlines():  # Cambiar a 'latin1'
            if ":" in line:
                key, value = line.split(":", 1)
                cpu_info[key.strip()] = value.strip()
        return cpu_info
    except subprocess.CalledProcessError as e:
        return f"Error al obtener información de la CPU: {e}"

def obtener_info_mainboard():
    comando = 'Get-CimInstance -ClassName Win32_BaseBoard'
    try:
        mainboard_raw = subprocess.check_output(["powershell", "-Command", comando], stderr=subprocess.PIPE)
        mainboard_info = {}
        for line in mainboard_raw.decode('latin1').strip().splitlines():  # Cambiar a 'latin1'
            if ":" in line:
                key, value = line.split(":", 1)
                mainboard_info[key.strip()] = value.strip()
        return mainboard_info
    except subprocess.CalledProcessError as e:
        return f"Error al obtener información de la placa base: {e}"

def obtener_info_gpu():
    comando = 'Get-CimInstance -ClassName Win32_VideoController'
    try:
        gpu_raw = subprocess.check_output(["powershell", "-Command", comando], stderr=subprocess.PIPE)
        gpu_info = {}
        for line in gpu_raw.decode('latin1').strip().splitlines():  # Cambiar a 'latin1'
            if ":" in line:
                key, value = line.split(":", 1)
                gpu_info[key.strip()] = value.strip()
        return gpu_info
    except subprocess.CalledProcessError as e:
        return f"Error al obtener información de la GPU: {e}"

def obtener_info_ram():
    comando = 'Get-CimInstance -ClassName Win32_PhysicalMemory'
    try:
        ram_raw = subprocess.check_output(["powershell", "-Command", comando], stderr=subprocess.PIPE)
        ram_info = {}
        for line in ram_raw.decode('latin1').strip().splitlines():  # Cambiar a 'latin1'
            if ":" in line:
                key, value = line.split(":", 1)
                ram_info[key.strip()] = value.strip()
        return ram_info
    except subprocess.CalledProcessError as e:
        return f"Error al obtener información de la RAM: {e}"

def obtener_info_disco():
    comando = 'Get-CimInstance -ClassName Win32_LogicalDisk | Select-Object DeviceID, Size, MediaType'
    try:
        disco_raw = subprocess.check_output(["powershell", "-Command", comando], stderr=subprocess.PIPE)
        disco_info = []
        for line in disco_raw.decode('latin1').strip().splitlines():  # Cambiar a 'latin1'
            if ":" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    key, value = parts[0].strip(), parts[1].strip()
                    if key in ["DeviceID", "Size", "MediaType"]:
                        disco_info.append((key, value))
        return disco_info
    except subprocess.CalledProcessError as e:
        return f"Error al obtener información de los discos duros: {e}"

def mostrar_info_hardware():
    cpu = obtener_info_cpu()
    mainboard = obtener_info_mainboard()
    gpu = obtener_info_gpu()
    ram = obtener_info_ram()
    discos = obtener_info_disco()

    cpu_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("CPU", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Nombre: {cpu.get('Name', 'Desconocido')}"),
                ft.Text(f"Familia: {cpu.get('Family', 'Desconocido')}"),
                ft.Text(f"MaxClockSpeed: {cpu.get('MaxClockSpeed', 'Desconocido')} MHz"),
                ft.Text(f"Arquitectura: {cpu.get('Architecture', 'Desconocida')}")
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=ft.padding.all(10),
        bgcolor="#3C3D5C",
        border_radius=10,
    )

    mainboard_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Mainboard", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Fabricante: {mainboard.get('Manufacturer', 'Desconocido')}"),
                ft.Text(f"Producto: {mainboard.get('Product', 'Desconocido')}")
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=ft.padding.all(10),
        bgcolor="#3C3D5C",
        border_radius=10,
    )

    gpu_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("GPU", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Nombre: {gpu.get('Name', 'Desconocido')}"),
                ft.Text(f"VRAM: {gpu.get('VRAM', 'Desconocido')} GB")
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=ft.padding.all(10),
        bgcolor="#3C3D5C",
        border_radius=10,
    )

    ram_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("RAM", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Capacidad: {ram.get('Capacity', 'Desconocida')}"),
                ft.Text(f"Velocidad: {ram.get('Speed', 'Desconocida')}")
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=ft.padding.all(10),
        bgcolor="#3C3D5C",
        border_radius=10,
    )

    discos_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Discos Duros", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(" | ".join([f"{disk[0]}: {disk[1]}" for disk in discos]))
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=ft.padding.all(10),
        bgcolor="#3C3D5C",
        border_radius=10,
    )

    return ft.Column(
        controls=[
            cpu_container,
            mainboard_container,
            gpu_container,
            ram_container,
            discos_container
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START
    )