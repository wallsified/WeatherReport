"""
Ventana de Búsqueda del clima 
Author:  @wallsified
Version: 1.2
"""

import flet as ft
import general_configurations as gc
import cache
import searcher

# Propiedades del botón de entrada de texto para la búsqueda
search_title_button = gc.new_text_field()
search_title_button.label = "Ingresa tu Búsqueda"
search_title_button.width = 400
search_title_button.height = 50
search_title_button.autofocus = True
search_title_button.hint_text = "Puedes Buscar por IATA, Ciudad o No. Ticket"

# Propiedades del botón de búsqueda
search_initation = gc.new_elevated_button()
search_initation.text = "Iniciar Busqueda"
search_initation.icon = ft.icons.SEARCH
search_initation.width = 320
search_initation.height = 50

headers = gc.table_headers()

# Propiedades del Botón para limpiar los resultados previos.
clean_button = gc.new_elevated_button()
clean_button.text = "Limpiar Resultados"
clean_button.icon = ft.icons.CLEANING_SERVICES_ROUNDED

# Tipografías de la ventana
ft.Page.fonts = {
    "Roboto Light": "/fonts/Roboto-Light.ttf",
    "Caviar": "fonts/CaviarDreams.ttf"
}

top_row = ft.ResponsiveRow(
    [
        ft.Column(col={"sm": 6}, controls=[search_title_button]),
        ft.Column(col={"sm": 6}, controls=[search_initation])
    ],
    run_spacing={"sm": 30},
)

second_row = ft.ResponsiveRow([headers], run_spacing={"sm": 30})

def main(page: ft.Page):
    """
    Método Main para poder ejecutar la Ventana Principal
    """
    page.bgcolor = gc.CLOUD_WHITE
    page.title = "Weather Reporter"
    page.window_width = 850
    page.window_height = 600
    page.window_max_height = 600
    page.window_max_width = 850
    page.window_maximized = False
    page.window_center = True
    page.auto_scroll = True
    page.window_focused = True
    page.window_full_screen = False


    def button_clicked(event):
        query.value = f"{search_title_button.value}"
        result_grid = items(query.value)
        page.add(second_row, result_grid, clean_button)
        search_initation.disabled = True
        search_title_button.disabled = True
        page.update()
    
    def clean_table(event):
        search_initation.disabled = False
        search_title_button.disabled = False
        page.remove(second_row, clean_button) #y en teoria la información...
        page.update()
        

    def items(value):
        data_table = gc.new_grid_view()
        for index, sublista in enumerate(searcher.search_cache(value)):
            for data in sublista:
                data_table.controls.append(
                    ft.Container(
                        ft.Text(value=data, font_family='Caviar'),
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(5),
                        border=ft.border.all(width=1, color=gc.NAVY_BLUE),
                        width=60,
                        height=20,
                        padding=15,
                    )
                )
        page.update()
        return data_table


    cache.run_cache()
    query = ft.Text()
    search_initation.on_click = button_clicked
    clean_button.on_click = clean_table
    page.add(top_row)

ft.app(
    target=main,
    assets_dir="Assets/"
)
