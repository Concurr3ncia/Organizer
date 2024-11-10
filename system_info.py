import subprocess

def ejecutar_comando_powershell(comando):
    try:
        resultado = subprocess.check_output(["powershell", "-Command", comando]).decode().strip()
        return resultado
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

def obtener_version_windows():
    comando = 'Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object -ExpandProperty Name'
    resultado = ejecutar_comando_powershell(comando)
    try:
        return resultado.split("|")[0]
    except:
        return "No disponible"

def obtener_info_cpu():
    comando = 'Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty Name'
    return ejecutar_comando_powershell(comando)

def obtener_arquitectura_cpu():
    comando = 'Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty Architecture'
    arquitectura_raw = ejecutar_comando_powershell(comando)
    arquitectura_map = {
        "0": "x86",
        "1": "MIPS",
        "2": "Alpha",
        "3": "PowerPC",
        "5": "ARM",
        "6": "Itanium-based systems",
        "9": "x64"
    }
    try:
        return arquitectura_map.get(arquitectura_raw, "Desconocida")
    except:
        return "Desconocida"

def obtener_info_gpu():
    comando = 'Get-CimInstance -ClassName Win32_VideoController | Select-Object -ExpandProperty Name'
    return ejecutar_comando_powershell(comando)

def obtener_nombre_equipo():
    comando = 'Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object -ExpandProperty UserName'
    resultado = ejecutar_comando_powershell(comando)
    try:
        return resultado.split('\\')[-1]
    except:
        return "No disponible"

def obtener_info_ram():
    comando = 'Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object -ExpandProperty TotalPhysicalMemory'
    resultado = ejecutar_comando_powershell(comando)
    try:
        ram_bytes = int(resultado)
        return f'{ram_bytes / (1024 ** 3):.2f} GB'
    except:
        return "No disponible"