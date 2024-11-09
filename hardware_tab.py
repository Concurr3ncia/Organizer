import flet as ft
import subprocess

def get_cpu_info():
    command = 'Get-CimInstance -ClassName Win32_Processor'
    try:
        cpu_raw = subprocess.check_output(["powershell", "-Command", command], stderr=subprocess.PIPE)
        cpu_info = {}
        for line in cpu_raw.decode('latin1').strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                cpu_info[key.strip()] = value.strip()
        return cpu_info
    except subprocess.CalledProcessError as e:
        return f"Error getting CPU info: {e}"

def get_mainboard_info():
    command = 'Get-CimInstance -ClassName Win32_BaseBoard'
    try:
        mainboard_raw = subprocess.check_output(["powershell", "-Command", command], stderr=subprocess.PIPE)
        mainboard_info = {}
        for line in mainboard_raw.decode('latin1').strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                mainboard_info[key.strip()] = value.strip()
        return mainboard_info
    except subprocess.CalledProcessError as e:
        return f"Error getting mainboard info: {e}"

def get_gpu_info():
    command = 'Get-CimInstance -ClassName Win32_VideoController'
    try:
        gpu_raw = subprocess.check_output(["powershell", "-Command", command], stderr=subprocess.PIPE)
        gpu_info = {}
        for line in gpu_raw.decode('latin1').strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                gpu_info[key.strip()] = value.strip()
        # Convert VRAM from bytes to GB
        if "AdapterRAM" in gpu_info:
            gpu_info["AdapterRAM"] = str(int(gpu_info["AdapterRAM"]) // (1024 ** 3)) + " GB"
        return gpu_info
    except subprocess.CalledProcessError as e:
        return f"Error getting GPU info: {e}"

def get_ram_info():
    command = 'Get-CimInstance -ClassName Win32_PhysicalMemory'
    try:
        ram_raw = subprocess.check_output(["powershell", "-Command", command], stderr=subprocess.PIPE)
        ram_info = {}
        for line in ram_raw.decode('latin1').strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                ram_info[key.strip()] = value.strip()
        # Convert RAM capacity from bytes to GB
        if "Capacity" in ram_info:
            ram_info["Capacity"] = str(int(ram_info["Capacity"]) // (1024 ** 3)) + " GB"
        return ram_info
    except subprocess.CalledProcessError as e:
        return f"Error getting RAM info: {e}"

def get_disk_info():
    command = 'Get-CimInstance -ClassName Win32_LogicalDisk | Select-Object DeviceID, Size, MediaType'
    try:
        disk_raw = subprocess.check_output(["powershell", "-Command", command], stderr=subprocess.PIPE)
        disk_info = []
        for line in disk_raw.decode('latin1').strip().splitlines():
            if ":" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    key, value = parts[0].strip(), parts[1].strip()
                    if key in ["DeviceID", "Size", "MediaType"]:
                        # Convert disk size from bytes to GB
                        if key == "Size":
                            value = str(int(value) // (1024 ** 3)) + " GB"
                        disk_info.append((key, value))
        return disk_info
    except subprocess.CalledProcessError as e:
        return f"Error getting disk info: {e}"

def display_hardware_info(page):
    cpu = get_cpu_info()
    mainboard = get_mainboard_info()
    gpu = get_gpu_info()
    ram = get_ram_info()
    disks = get_disk_info()

    cpu_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("CPU", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Name: {cpu.get('Name', 'Unknown')}"),
                ft.Text(f"Family: {cpu.get('Family', 'Unknown')}"),
                ft.Text(f"MaxClockSpeed: {cpu.get('MaxClockSpeed', 'Unknown')} MHz"),
                ft.Text(f"Architecture: {cpu.get('Architecture', 'Unknown')}")
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=ft.padding.all(10),
        bgcolor="#3C3D5C",
        border_radius=10,
        height=page.height // 5  # Dynamic height based on the page height
    )

    mainboard_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Mainboard", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Manufacturer: {mainboard.get('Manufacturer', 'Unknown')}"),
                ft.Text(f"Product: {mainboard.get('Product', 'Unknown')}")
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=ft.padding.all(10),
        bgcolor="#3C3D5C",
        border_radius=10,
        height=page.height // 5  # Dynamic height based on the page height
    )

    gpu_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("GPU", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Name: {gpu.get('Name', 'Unknown')}"),
                ft.Text(f"VRAM: {gpu.get('AdapterRAM', 'Unknown')}")
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=ft.padding.all(10),
        bgcolor="#3C3D5C",
        border_radius=10,
        height=page.height // 5  # Dynamic height based on the page height
    )

    ram_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("RAM", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Capacity: {ram.get('Capacity', 'Unknown')}"),
                ft.Text(f"Speed: {ram.get('Speed', 'Unknown')}")
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=ft.padding.all(10),
        bgcolor="#3C3D5C",
        border_radius=10,
        height=page.height // 5  # Dynamic height based on the page height
    )

    disks_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Disks", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(" | ".join([f"{disk[0]}: {disk[1]}" for disk in disks]))
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=ft.padding.all(10),
        bgcolor="#3C3D5C",
        border_radius=10,
        height=page.height // 5  # Dynamic height based on the page height
    )

    # Organize in a ListView to allow scrolling
    list_view = ft.ListView(
        controls=[
            cpu_container,
            mainboard_container,
            gpu_container,
            ram_container,
            disks_container,
        ],
        height=page.height - 100,  # Take the remaining height after header and footer
        width=page.width,  # Full page width
        padding=ft.padding.all(20),  # Add padding between components
    )

    return list_view
