"""
Ventana de Búsqueda del clima 
Author:  @wallsified
Version: 1.1

Nota: Flet se puede manejar a nivel ventana como una matriz 
con elementos 'Column' y 'Row', por lo que diversas
instancias de dichos elementos y derivados cumplen con
ser la construcción de la ventana. 
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

second_row = ft.ResponsiveRow([gc.table_headers], run_spacing={"sm": 30})

lista_de_listas = [
    [1, 2, 3, 4, 5, 6, 7, 8],
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
    [True, False, True, False, True, False, True, False],
    [10, 20, 30, 40, 50, 60, 70, 80],
    ['x', 'y', 'z', 'w', 'v', 'u', 't', 's']
]

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

    def textbox_changed(event):
        search_query.value = f"{search_title_button.value}"
        page.update()

    search_query = ft.Text()
    search_initation.on_click= textbox_changed
    
    cache.run_cache()

    def items():
        data_table = gc.new_grid_view()
        for i, sublista in enumerate(lista_de_listas):
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

    def load_results(event):
        value = search_query.value
        # quiero ver primero como se visualiza el puro resultado y de ahi 
        # empezar a entender lo demás pero no me deja.
        data = ft.Text(searcher.search_cache(value))
        page.add(gc.table_headers, data, clean_button)
        page.update()

    def clean_table(event):
        page.remove(gc.table_headers, clean_button)
        page.update()

    clean_button.on_click = clean_table

    result_button = ft.ElevatedButton(
        text= "Resultados",
        on_click= load_results,
    )

    page.add(top_row, result_button)

ft.app(
    target=main,
    assets_dir="Assets/"
)
