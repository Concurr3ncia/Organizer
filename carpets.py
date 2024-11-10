from pathlib import Path
import shutil
biblioteca_carpetas = {
    "imagenes": ["png", "jpg", "jpeg", "gif", "bmp"],
    "documentos": ["pdf", "docx", "txt", "xlsx", "pptx"],
    "audio": ["mp3", "wav", "ogg", "flac"],
    "videos": ["mp4", "avi", "mov", "mkv"],
    "archivos_comprimidos": ["zip", "tar", "gz", "rar"]
}

def move_to_carpet(carpeta,item):
    shutil.move(str(item), str(carpeta / item.name))

directorio_Actual = Path(r"E:\Prueba_parafotos")
def make_carpet(carpeta,item):
    # Crear la ruta completa para la nueva carpeta
    nueva_carpeta = directorio_Actual / carpeta

    # Crear la carpeta si no existe
    nueva_carpeta.mkdir(parents=True, exist_ok=True)

    for item in directorio_Actual.iterdir():
        if item.is_file():  # Solo mover archivos (no carpetas)
            move_to_carpet(nueva_carpeta, item)
    
def get_files():
    for item in directorio_Actual.iterdir():
        if item.is_file():  # Solo imprime archivos
            item_path = item.resolve()
            sufijo_formatted = item.suffix[1:]
            for carpeta,extensiones in biblioteca_carpetas.items():
                if sufijo_formatted in extensiones:
                    make_carpet(carpeta,item_path)
                    
