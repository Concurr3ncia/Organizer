import flet as ft
import time
import asyncio
from typing import Dict, Any

# Import modules
from apps_tab import *
from hardware_tab import *
from windows import *
from organizer import organize_tab  # Importamos la función organize_tab

def main(page: ft.Page):
    page.window.maximized = True
    page.bgcolor = "#25253d"
    page.title = "Organizer"
    
    # Loading screen components
    progress_bar = ft.ProgressBar(
        width=page.width * 0.3 if page.width > 1000 else page.width * 0.8,
        color="#888abf",
        bgcolor="#3C3D5C",
        value=0
    )
    
    loading_text = ft.Text(
        "Initializing...", 
        size=20, 
        weight=ft.FontWeight.BOLD,
        color="#B5BFE3"
    )

    loading_logo = ft.Icon(
        name=ft.icons.FOLDER_ROUNDED,
        size=50,
        color="#888abf"
    )
    
    loading_container = ft.Container(
        content=ft.Column(
            controls=[
                loading_logo,
                ft.Container(height=10),
                loading_text,
                ft.Container(height=20),
                progress_bar
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    def page_resize(e):
        progress_bar.width = page.width * 0.3 if page.width > 1000 else page.width * 0.8
        page.update()

    page.on_resized = page_resize
    page.add(loading_container)
    
    # Initialize empty containers for modules
    tabs_content: Dict[str, Any] = {}
    
    async def load_modules():
        nonlocal tabs_content
        
        # Define module loading steps
        async def load_windows_module():
            loading_text.value = "Loading Windows Module..."
            page.update()
            await asyncio.sleep(0.5)  # Simulate actual loading time
            tabs_content["Windows"] = display_optimization_options(page)
            progress_bar.value = 0.2
            page.update()
            
        async def load_apps_module():
            loading_text.value = "Loading Apps Module..."
            page.update()
            await asyncio.sleep(0.5)  # Simulate actual loading time
            tabs_content["Apps"] = apps_tab()
            progress_bar.value = 0.4
            page.update()
            
        async def load_hardware_module():
            loading_text.value = "Loading Hardware Module..."
            page.update()
            await asyncio.sleep(0.5)  # Simulate actual loading time
            tabs_content["Hardware"] = display_hardware_info(page)
            progress_bar.value = 0.6
            page.update()
            
        async def load_organizer_module():
            loading_text.value = "Loading Organizer Module..."
            page.update()
            await asyncio.sleep(0.5)  # Simulate actual loading time
            tabs_content["Organize"] = organize_tab(page)
            progress_bar.value = 0.8
            page.update()
            
        async def load_remaining_modules():
            loading_text.value = "Loading Additional Modules..."
            page.update()
            await asyncio.sleep(0.5)  # Simulate actual loading time
            # Initialize remaining modules
            tabs_content.update({
                "Utilities": ft.Text("Utilities Content", size=24, color=ft.colors.WHITE),
                "Startup": ft.Text("Startup Content", size=24, color=ft.colors.WHITE),
                "Cleaner": ft.Text("Cleaner Content", size=24, color=ft.colors.WHITE),
                "Options": ft.Text("Options Content", size=24, color=ft.colors.WHITE)
            })
            progress_bar.value = 1.0
            page.update()
        
        # Execute module loading sequence
        await load_windows_module()
        await load_apps_module()
        await load_hardware_module()
        await load_organizer_module()
        await load_remaining_modules()
        
        loading_text.value = "Finalizing..."
        page.update()
        await asyncio.sleep(0.5)
        
        # Remove loading screen and initialize main UI
        page.clean()
        initialize_main_ui()
    
    def create_menu_item(icon_name, label, tab_content, colorselect):
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
                                            color="#b8bfd9",
                                            stroke_width=1,
                                            stroke_join=ft.StrokeJoin.ROUND
                                        ),
                                    ),
                                ),
                            ],
                        )
                    ]
                )
                e.control.content.controls.append(text)
                label_width = len(label) * 8
                e.control.width = 50 + label_width
                menu.width = page.width * 0.352 + label_width
                child_container.width = page.width * 0.352 + label_width
                e.control.bgcolor = "#888abf"
                is_hovered = True
            elif e.data == "false" and is_hovered:
                e.control.content.controls.pop()
                menu.width = page.width * 0.352
                child_container.width = page.width * 0.352
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
                controls=[ft.Icon(name=icon_name, color=colorselect, size=25)],
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

    def initialize_main_ui():
        nonlocal tabs_content
        
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

        iconos_menu = [
            create_menu_item(ft.icons.WINDOW_ROUNDED, "Windows", tabs_content["Windows"], "#B5BFE3"),
            create_menu_item(ft.icons.APPS, "Apps", tabs_content["Apps"], "#B5BFE3"),
            create_menu_item(ft.icons.FOLDER_ROUNDED, "Organize", tabs_content["Organize"], "#B5BFE3"),
            create_menu_item(ft.icons.RESTART_ALT_ROUNDED, "Startup", tabs_content["Startup"], "#B5BFE3"),
            create_menu_item(ft.icons.CLEANING_SERVICES, "Cleaner", tabs_content["Cleaner"], "#B5BFE3"),
            create_menu_item(ft.icons.TASK, "Utilities", tabs_content["Utilities"], "#B5BFE3"),
            create_menu_item(ft.icons.HARDWARE_ROUNDED, "Hardware", tabs_content["Hardware"], "#B5BFE3"),
            create_menu_item(ft.icons.SETTINGS_ROUNDED, "Options", tabs_content["Options"], "#B5BFE3")
        ]

        nonlocal child_container, menu, tab_content_container
        
        child_container = ft.Container(
            content=ft.Row(
                controls=iconos_menu,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=ft.alignment.center,
            width=page.width * 0.35,
            height=50,
            border_radius=10,
            bgcolor="#3C3D5C",
            border=ft.border.only(bottom=ft.border.BorderSide(3, "#313252")),
            animate=ft.animation.Animation(duration=300, curve="easeInOut")
        )

        menu = ft.Container(
            alignment=ft.alignment.center,
            width=page.width * 0.35,
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

    def switch_tab(content):
        tab_content_container.content = content
        tab_content_container.update()

    # Initialize containers at module level
    child_container = None
    menu = None
    tab_content_container = None
    
    # Start the loading process
    asyncio.run(load_modules())

if __name__ == "__main__":
    ft.app(target=main)