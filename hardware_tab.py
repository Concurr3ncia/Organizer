import subprocess
from concurrent.futures import ThreadPoolExecutor
from win32api import GetSystemMetrics
import flet as ft

def run_command(comando):
    try:
        result = subprocess.check_output(["powershell", "-Command", comando]).decode().strip()
        if not result:
            return "No se pudo obtener el valor"
        return result
    except subprocess.CalledProcessError as e:
        return f"Error al ejecutar el comando: {e}"

# Diccionario de generaciones de AMD y los modelos asociados
Amd_cpu_generations = {
    "Zen 2": [
        "3950X", "3900XT", "3900X", "3900", "3800XT", "3800X", "3700X", "3600XT",
        "3600X", "3600", "3500X", "3500", "3300X", "3100", "3995WX", "3975WX", 
        "3955WX", "3945WX", "3990X", "3970X", "3960X", "4700S", "4500", "4100", 
        "4700G", "4700GE", "4600G", "4600GE", "4300G", "4300GE", "4900H", "4900HS", 
        "4800H", "4800HS", "4980U", "4800U", "4700U", "4600H", "4680U", "4600U", 
        "4500U", "4300U", "5700U", "5500U", "5300U", "7520U", "7320U", "V2516", 
        "V2546", "V2718", "V2748"
    ],
    "Zen 3": [
        "5950X", "5900XT", "5900X", "5900", "PRO 5945", "5800X3D", "5800XT", "5800X",
        "5800", "5700X3D", "5700X", "PRO 5845", "5600X3D", "5600X", "5600", "PRO 5645",
        "5700", "5500", "5995WX", "5975WX", "5965WX", "5955WX", "5945WX", "5700G", 
        "5700GE", "5600GT", "5600G", "5600GE", "5500GT", "5300G", "5300GE", "PRO", 
        "PRO", "PRO", "6980HX", "6980HS", "6900HX", "6900HS", "6800H", "6800HS", "6800U", 
        "6600H", "6600HS", "6600U", "7735HS", "7735H", "7736U", "7735U", "7435HS", 
        "7435H", "7535HS", "7535H", "7535U", "7235HS", "7235H", "7335U"
    ],
    "Zen 4": [
        "8640HS", "8640U", "8540U", "8440U", "4124P", "4244P", "4344P", "4364P", 
        "4464P", "4484PX", "4564P", "4584PX", "8024P", "8024PN", "8124P", "8124PN", 
        "8224P", "8224PN", "8324P", "8324PN", "8434P", "8434PN", "8534P", "8534PN", 
        "9124", "9224", "9254", "9334", "9354", "9354P", "9174F", "9184X", "9274F", 
        "9374F", "9384X", "9474F", "9454", "9454P", "9534", "9554", "9554P", "9634", 
        "9654", "9654P", "9684X", "9734", "9754S", "9754"
    ],
    "Ryzen 5": [
        "9950X", "9900X", "9800X3D", "9700X", "9600X", "PRO", "PRO", "365", "PRO 360"
    ],
    "Zen+": [
        "2700X", "2700", "2700E", "2600X", "2600", "2600E", "1600 (AF)", "2500X", 
        "2300X", "Athlon Pro 300GE", "Athlon Silver Pro 3125GE", "Athlon Gold 3150GE", 
        "Athlon Gold Pro 3150GE", "Athlon Gold 3150G", "Athlon Gold Pro 3150G", 
        "Ryzen 3 3200GE", "Ryzen 3 Pro 3200GE", "Ryzen 3 3200G", "Ryzen 3 Pro 3200G", 
        "Ryzen 5 Pro 3350GE", "Ryzen 5 Pro 3350G", "Ryzen 5 3400GE", "Ryzen 5 Pro 3400GE", 
        "Ryzen 5 3400G", "Ryzen 5 Pro 3400G", "R2312", "R2314"
    ],
    "Ryzen": [
        "Ryzen 7 7700X", "Ryzen 7 7600X", "Ryzen 7 5700X", "Ryzen 7 5800X3D", "Ryzen 7 5800X", 
        "Ryzen 9 7950X", "Ryzen 9 7900X", "Ryzen 9 5900X", "Ryzen 9 5950X", "Ryzen 9 3900X", 
        "Ryzen 9 3950X", "Ryzen 7 3800X", "Ryzen 7 3700X", "Ryzen 5 5600X", "Ryzen 5 5600G", 
        "Ryzen 5 5500", "Ryzen 5 3400G", "Ryzen 5 3600", "Ryzen 5 3600X", "Ryzen 5 3500X", 
        "Ryzen 3 3300X", "Ryzen 3 3100", "Ryzen 3 3200G", "Ryzen 3 3200GE"
    ]
}

def get_cpu_generation(cpu_info):
    # Check which generation the processor belongs to
    for generation, models in Amd_cpu_generations.items():
        if any(model in cpu_info for model in models):
            return generation
    return "Unknown generation"

def get_general_info():
    commands = {
        "cpu": 'Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty Name',
        "architecture": 'Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty Architecture',
        "cores": 'Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty NumberOfCores',
        "threads": 'Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty NumberOfLogicalProcessors',
        "gpu": 'Get-CimInstance -ClassName Win32_VideoController | Select-Object -ExpandProperty Name',
        "vram": 'Get-CimInstance -ClassName Win32_VideoController | Select-Object -ExpandProperty AdapterRAM',
        "ram": 'Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object -ExpandProperty TotalPhysicalMemory',
        "ram_frequency": 'Get-CimInstance -ClassName Win32_PhysicalMemory | Select-Object -ExpandProperty Speed',
        "windows_version": 'Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object -ExpandProperty Name',
        "computer_name": 'Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object -ExpandProperty UserName',
        "disk_space": 'Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{Name="Used";Expression={[math]::round($_.Used/1GB,2)}}, @{Name="Free";Expression={[math]::round($_.Free/1GB,2)}} | Where-Object {$_.Name -in "C", "D", "E"}',
        "motherboard": 'Get-CimInstance -ClassName Win32_BaseBoard | Select-Object -ExpandProperty Product',
        "refresh_rate": 'Get-CimInstance -ClassName Win32_VideoController | Select-Object CurrentRefreshRate',
        "disk": 'Get-CimInstance -ClassName Win32_DiskDrive | Select-Object Model, MediaType'
    }

    with ThreadPoolExecutor() as executor:
        results = executor.map(run_command, commands.values())
    
    results = list(results)
    cpu_info = results[0]
    architecture_raw = results[1]
    cores = results[2]
    threads = results[3]
    gpu = results[4]
    vram_raw = results[5]
    ram_info_raw = results[6]
    ram_frequency_raw = results[7]
    windows_version = results[8]
    computer_name = results[9]
    disk_space_raw = results[10]
    motherboard = results[11]
    refresh_rate_raw = results[12]
    disks_raw = results[13]

    architecture_map = {
        "0": "x86",
        "1": "MIPS",
        "2": "Alpha",
        "3": "PowerPC",
        "5": "ARM",
        "6": "Itanium-based systems",
        "9": "x64"
    }
    architecture = architecture_map.get(architecture_raw, "Unknown")

    ram_total_gb = int(ram_info_raw) / (1024 ** 3)
    vram_total_gb = int(vram_raw) / (1024 ** 3) if vram_raw.isdigit() else 0

    windows_version = windows_version.split('|')[0].strip()

    disk_space = ""
    disk_info = {}
    for line in disk_space_raw.splitlines():
        if "Name" not in line and "----" not in line:
            parts = line.split()
            if len(parts) >= 3:
                drive = parts[0]
                used = parts[1]
                free = parts[2]
                if drive not in disk_info:
                    disk_info[drive] = {'used': used, 'free': free}

    ram_frequency = ''.join(filter(str.isdigit, ram_frequency_raw.split()[0]))

    # Get resolution using win32api
    screen_width = GetSystemMetrics(0)  # Screen width
    screen_height = GetSystemMetrics(1)  # Screen height
    resolution = f"{screen_width} x {screen_height}"

    # Clean and format refresh rate
    refresh_rate = ''.join(filter(str.isdigit, refresh_rate_raw)) if refresh_rate_raw else "Not available"

    # Get disk brands and types
    disks = disks_raw.splitlines()
    disk_brands = []

    for disk in disks:
        if "Microsoft Storage Space Device" not in disk and "Model" not in disk and "-----" not in disk:
            model = disk.replace("Fixed hard disk media", "").strip()
            if model:
                type = "HDD"
                if "SSD" in model:
                    type = "SSD"
                disk_brands.append(f"Disk brand: {model}, Type: {type}")

    # Get CPU generation
    cpu_generation = get_cpu_generation(cpu_info)

    # Organize disk information
    disk_info_str = ""
    for drive, data in disk_info.items():
        disk_info_str += f"Drive {drive}: Used {data['used']} GB, Free {data['free']} GB\n"

    disk_brands_str = "\n".join(disk_brands)
    info = {
        "Mainboard": {
            "Motherboard": motherboard,
        },
        "CPU": {
            "CPU Name": cpu_info,
            "CPU Generation": cpu_generation,
            "CPU Architecture": architecture,
            "CPU Cores": cores,
            "CPU Threads": threads,
        },
        "GPU": {
            "GPU Name": gpu,
            "GPU VRAM": f"{vram_total_gb:.2f} GB",
        },
        "RAM": {
            "RAM Total": f"{ram_total_gb:.2f} GB",
            "RAM Frequency": f"{ram_frequency} MHz",
        },
        "OS": {
            "OS Version": windows_version,
            "User Name": computer_name,
        },
        "Display": {
            "Display Resolution": resolution,
            "Refresh Rate": refresh_rate,
        },
        "Hard Drives": {
            "Disk Space": disk_info_str,
            "Disk Brands": disk_brands_str,
        }
    }
    
    return info

def display_hardware_info(page):
    info = get_general_info()
    
    containers = []
    for category, details in info.items():
        category_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(category, size=20, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            padding=ft.padding.all(10),
            bgcolor="#3C3D5C",
            border_radius=10,
            width=page.width // 2 - 20,
        )
        
        detail_containers = []
        for key, value in details.items():
            detail_container = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(key, size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(value, size=16),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                ),
                padding=ft.padding.all(10),
                bgcolor="#4E4F74",
                border_radius=8,
                width=page.width // 2 - 20,
            )
            detail_containers.append(detail_container)
        
        containers.append(category_container)
        containers.extend(detail_containers)
    
    list_view = ft.ListView(
        controls=containers,
        height=page.height,
        width=page.width,
        padding=ft.padding.all(10),
        spacing=10
    )

    return list_view