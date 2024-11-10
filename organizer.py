import flet as ft
import os
import shutil
from datetime import datetime
import re
import tempfile
import zipfile
import traceback

def safe_move(src, dst):
    try:
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
        else:
            print(f"Warning: Source file not found - {src}")
    except Exception as e:
        print(f"Error moving file {src} to {dst}: {str(e)}")

def create_file_classification_section(page: ft.Page):
    selected_directory = ft.Text()
    
    def on_directory_result(e: ft.FilePickerResultEvent):
        selected_directory.value = e.path if e.path else "No directory selected"
        selected_directory.update()

    def classify_files(e):
        if not selected_directory.value or selected_directory.value == "No directory selected":
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Please select a directory first")))
            return

        organize_by_type = organize_by_type_checkbox.value
        organize_by_date = organize_by_date_checkbox.value
        create_subfolders = create_subfolders_checkbox.value

        progress_bar.visible = True
        progress_text.visible = True
        page.update()

        total_files = sum([len(files) for r, d, files in os.walk(selected_directory.value)])
        processed_files = 0
        error_count = 0

        for root, _, files in os.walk(selected_directory.value):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if organize_by_type:
                        file_type = os.path.splitext(file)[1][1:].lower() or "unknown"
                        type_folder = os.path.join(selected_directory.value, file_type)
                        safe_move(file_path, os.path.join(type_folder, file))
                    elif organize_by_date:
                        file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                        date_folder = os.path.join(selected_directory.value, file_date.strftime("%Y-%m-%d"))
                        safe_move(file_path, os.path.join(date_folder, file))
                except Exception as e:
                    error_count += 1
                    print(f"Error processing file {file_path}: {str(e)}")
                
                processed_files += 1
                progress = processed_files / total_files
                progress_bar.value = progress
                progress_text.value = f"Processed {processed_files} of {total_files} files"
                page.update()

        progress_bar.visible = False
        progress_text.visible = False
        if error_count > 0:
            page.open(ft.SnackBar(content=ft.Text(f"Classification completed with {error_count} errors. Check console for details.")))
        else:
            page.open(ft.SnackBar(content=ft.Text("Files classified successfully")))
        page.update()

    directory_picker = ft.FilePicker(on_result=on_directory_result)
    page.overlay.append(directory_picker)
    
    organize_by_type_checkbox = ft.Checkbox(label="Organize by file type", value=False)
    organize_by_date_checkbox = ft.Checkbox(label="Organize by date", value=False)
    create_subfolders_checkbox = ft.Checkbox(label="Create subfolders automatically", value=False)
    
    progress_bar = ft.ProgressBar(visible=False)
    progress_text = ft.Text("", visible=False)

    content = ft.Column(
        controls=[
            ft.Text("Select directory to classify:"),
            selected_directory,
            ft.ElevatedButton(
                "Select directory",
                icon=ft.icons.FOLDER_OPEN,
                on_click=lambda _: directory_picker.get_directory_path()
            ),
            ft.Divider(),
            organize_by_type_checkbox,
            organize_by_date_checkbox,
            create_subfolders_checkbox,
            ft.ElevatedButton(
                "Classify files",
                icon=ft.icons.PLAY_ARROW,
                on_click=classify_files
            ),
            progress_bar,
            progress_text
        ],
        spacing=10
    )
    return content

def create_mass_rename_section(page: ft.Page):
    selected_files = ft.Text()
    
    def on_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = ", ".join([os.path.basename(f.path) for f in e.files]) if e.files else "No files selected"
        selected_files.update()

    def rename_files(e):
        if not selected_files.value or selected_files.value == "No files selected":
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Please select files first")))
            return

        prefix = prefix_field.value
        suffix = suffix_field.value
        include_date = include_date_checkbox.value
        to_lower = to_lower_checkbox.value

        for file in file_picker.result.files:
            file_path = file.path
            file_name, file_ext = os.path.splitext(os.path.basename(file_path))
            new_name = prefix + file_name + suffix
            if include_date:
                file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                new_name += '_' + file_date.strftime("%Y%m%d")
            if to_lower:
                new_name = new_name.lower()
            new_name += file_ext
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            os.rename(file_path, new_path)

        page.show_snack_bar(ft.SnackBar(content=ft.Text("Files renamed successfully")))

    file_picker = ft.FilePicker(on_result=on_files_result)
    page.overlay.append(file_picker)

    prefix_field = ft.TextField(label="Prefix", border_color="white")
    suffix_field = ft.TextField(label="Suffix", border_color="white")
    include_date_checkbox = ft.Checkbox(label="Include date", value=False)
    to_lower_checkbox = ft.Checkbox(label="Convert to lowercase", value=False)

    content = ft.Column(
        controls=[
            ft.Text("Select files to rename:"),
            selected_files,
            ft.ElevatedButton(
                "Select files",
                icon=ft.icons.FOLDER_OPEN,
                on_click=lambda _: file_picker.pick_files(allow_multiple=True)
            ),
            ft.Divider(),
            prefix_field,
            suffix_field,
            include_date_checkbox,
            to_lower_checkbox,
            ft.ElevatedButton(
                "Rename files",
                icon=ft.icons.DRIVE_FILE_RENAME_OUTLINE,
                on_click=rename_files
            )
        ],
        spacing=10
    )
    return content

def create_temp_files_section(page: ft.Page):
    selected_directory = ft.Text()
    
    def on_directory_result(e: ft.FilePickerResultEvent):
        selected_directory.value = e.path if e.path else "No directory selected"
        selected_directory.update()

    def clean_temp_files(e):
        if not selected_directory.value or selected_directory.value == "No directory selected":
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Please select a directory first")))
            return

        include_temp = include_temp_checkbox.value
        include_cache = include_cache_checkbox.value
        preserve_recent = preserve_recent_checkbox.value

        for root, dirs, files in os.walk(selected_directory.value):
            for file in files:
                file_path = os.path.join(root, file)
                if preserve_recent:
                    file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_age.days <= 7:
                        continue
                if include_temp and file.endswith('.tmp'):
                    os.remove(file_path)
                if include_cache and 'cache' in root.lower():
                    os.remove(file_path)

        page.show_snack_bar(ft.SnackBar(content=ft.Text("Temporary files cleaned successfully")))

    directory_picker = ft.FilePicker(on_result=on_directory_result)
    page.overlay.append(directory_picker)

    include_temp_checkbox = ft.Checkbox(label="Include temporary files", value=False)
    include_cache_checkbox = ft.Checkbox(label="Include system cache", value=False)
    preserve_recent_checkbox = ft.Checkbox(label="Preserve last 7 days", value=False)

    content = ft.Column(
        controls=[
            ft.Text("Select directory to clean:"),
            selected_directory,
            ft.ElevatedButton(
                "Select directory",
                icon=ft.icons.FOLDER_OPEN,
                on_click=lambda _: directory_picker.get_directory_path()
            ),
            ft.Divider(),
            include_temp_checkbox,
            include_cache_checkbox,
            preserve_recent_checkbox,
            ft.ElevatedButton(
                "Clean files",
                icon=ft.icons.CLEANING_SERVICES,
                on_click=clean_temp_files
            )
        ],
        spacing=10
    )
    return content

def create_backup_section(page: ft.Page):
    source_directory = ft.Text()
    destination_directory = ft.Text()
    
    def on_source_result(e: ft.FilePickerResultEvent):
        source_directory.value = e.path if e.path else "No source directory selected"
        source_directory.update()

    def on_destination_result(e: ft.FilePickerResultEvent):
        destination_directory.value = e.path if e.path else "No destination directory selected"
        destination_directory.update()

    def backup_files(e):
        if not source_directory.value or source_directory.value == "No source directory selected":
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Please select a source directory")))
            return
        if not destination_directory.value or destination_directory.value == "No destination directory selected":
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Please select a destination directory")))
            return

        incremental = incremental_checkbox.value
        compress = compress_checkbox.value

        backup_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(destination_directory.value, backup_name)

        if incremental:
            shutil.copytree(source_directory.value, backup_path, dirs_exist_ok=True)
        else:
            if compress:
                shutil.make_archive(backup_path, 'zip', source_directory.value)
            else:
                shutil.copytree(source_directory.value, backup_path)

        page.show_snack_bar(ft.SnackBar(content=ft.Text("Backup completed successfully")))

    source_picker = ft.FilePicker(on_result=on_source_result)
    destination_picker = ft.FilePicker(on_result=on_destination_result)
    page.overlay.extend([source_picker, destination_picker])

    incremental_checkbox = ft.Checkbox(label="Incremental backup", value=False)
    compress_checkbox = ft.Checkbox(label="Compress files", value=False)

    content = ft.Column(
        controls=[
            ft.Text("Select source directory:"),
            source_directory,
            ft.ElevatedButton(
                "Select source",
                icon=ft.icons.FOLDER_OPEN,
                on_click=lambda _: source_picker.get_directory_path()
            ),
            ft.Text("Select destination directory:"),
            destination_directory,
            ft.ElevatedButton(
                "Select destination",
                icon=ft.icons.FOLDER_OPEN,
                on_click=lambda _: destination_picker.get_directory_path()
            ),
            ft.Divider(),
            incremental_checkbox,
            compress_checkbox,
            ft.ElevatedButton(
                "Start backup",
                icon=ft.icons.BACKUP,
                on_click=backup_files
            )
        ],
        spacing=10
    )
    return content

def create_advanced_search_section(page: ft.Page):
    selected_directory = ft.Text()
    search_results = ft.ListView(expand=1, spacing=10, padding=20)
    
    def on_directory_result(e: ft.FilePickerResultEvent):
        selected_directory.value = e.path if e.path else "No directory selected"
        selected_directory.update()

    def search_files(e):
        if not selected_directory.value or selected_directory.value == "No directory selected":
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Please select a directory first")))
            return

        search_term = search_field.value
        search_subfolders = search_subfolders_checkbox.value
        include_hidden = include_hidden_checkbox.value
        use_regex = use_regex_checkbox.value

        search_results.controls.clear()

        for root, dirs, files in os.walk(selected_directory.value):
            if not search_subfolders and root != selected_directory.value:
                continue
            for file in files:
                if not include_hidden and file.startswith('.'):
                    continue
                if use_regex:
                    if re.search(search_term, file):
                        search_results.controls.append(ft.Text(os.path.join(root, file)))
                elif search_term.lower() in file.lower():
                    search_results.controls.append(ft.Text(os.path.join(root, file)))

        search_results.update()
        page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Found {len(search_results.controls)} results")))

    directory_picker = ft.FilePicker(on_result=on_directory_result)
    page.overlay.append(directory_picker)

    search_field = ft.TextField(label="Search term", border_color="white", prefix_icon=ft.icons.SEARCH)
    search_subfolders_checkbox = ft.Checkbox(label="Search in subfolders", value=False)
    include_hidden_checkbox = ft.Checkbox(label="Include hidden files", value=False)
    use_regex_checkbox = ft.Checkbox(label="Use regular expressions", value=False)

    content = ft.Column(
        controls=[
            ft.Text("Select directory to search:"),
            selected_directory,
            ft.ElevatedButton(
                "Select directory",
                icon=ft.icons.FOLDER_OPEN,
                on_click=lambda _: directory_picker.get_directory_path()
            ),
            ft.Divider(),
            search_field,
            search_subfolders_checkbox,
            include_hidden_checkbox,
            use_regex_checkbox,
            ft.ElevatedButton(
                "Search",
                icon=ft.icons.SEARCH,
                on_click=search_files
            ),
            search_results
        ],
        spacing=10
    )
    return content

def create_section_container(title: str, content: ft.Control) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    title,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),
                content
            ],
            spacing=15
        ),
        padding=20,
        border_radius=10,
        bgcolor="#3C3D5C",
        width=400,
        border=ft.border.all(1, "#4F46E5")
    )

def organize_tab(page: ft.Page):
    sections = [
        ("Clasificación de archivos", create_file_classification_section(page)),
        ("Renombrado masivo de archivos", create_mass_rename_section(page)),
        ("Archivos temporales", create_temp_files_section(page)),
        ("Copias de seguridad", create_backup_section(page)),
        ("Búsqueda avanzada", create_advanced_search_section(page))
    ]

    containers = [create_section_container(title, content) for title, content in sections]

    content = ft.Container(
        content=ft.GridView(
            controls=containers,
            max_extent=400,
            child_aspect_ratio=0.75,
            spacing=20,
            padding=20,
        ),
        expand=True,
    )

    return ft.Container(
        content=ft.Column(
            controls=[content],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
        ),
        expand=True,
    )

def main(page: ft.Page):
    page.title = "File Organizer"
    page.bgcolor = "#25253d"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 0
    page.spacing = 0
    page.window_width = 1200
    page.window_min_width = 800
    page.window_height = 800
    page.window_min_height = 600
    page.add(organize_tab(page))

if __name__ == "__main__":
    ft.app(target=main)