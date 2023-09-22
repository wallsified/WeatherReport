""" 
Ventana de Búsqueda del clima 
Author:  @wallsified
Version: 1.1
"""
import flet as ft

# Métodos de la clase general
import general_configurations as gc

search_initation = gc.new_elevated_button()
search_initation.text = "Iniciar Busqueda"
search_initation.icon = ft.icons.SEARCH
search_initation.width = 320
search_initation.height = 50

search_title_button = gc.new_text_field()
search_title_button.label = "Ingresa tu Búsqueda"
search_title_button.width = 400
search_title_button.height = 50
search_title_button.autofocus = True

info_grid = gc.new_grid_view()

headers = gc.table_headers()

clean_button = gc.new_elevated_button()
clean_button.text = "Limpiar Resultados"
clean_button.icon = ft.icons.CLEANING_SERVICES_ROUNDED

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

second_row = ft.ResponsiveRow([headers], run_spacing={"sm":30})


static_dictionary = {
    "flightone" : ['MTY', 25.7785, -100.107, 'MTY', 25.7785, -100.107],
    "flightwo" : ['MEX', 25.7785, -100.107, 'MTY', 25.7785, -100.107]
}

#lista estática de prueba
static_list = ['MTY', 25.7785, -100.107, 'Soleado', 'MTY', 25.7785, -100.107, 'Soleado']

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

    def items():
        """testeo de generación de n filas """
        data_table = gc.new_grid_view()
        for item in static_list:
            data_table.controls.append(
                ft.Container(
                    ft.Text(value= item, font_family= 'Caviar'),
                    alignment=ft.alignment.center,
                    border_radius=ft.border_radius.all(5),
                    border=ft.border.all(width=1, color=gc.NAVY_BLUE),
                    width = 60,
                    height= 20,
                    padding = 15,

                )
            )
        page.update()
        return data_table

    datos = items()

    def add_table(event):
        page.add(datos, clean_button)
        page.update()
        
    def clean_table(event):
        page.remove(datos, clean_button)
        page.update()

    search_initation.on_click = add_table
    clean_button.on_click = clean_table

    page.add(top_row, second_row)

ft.app(
    target= main,
    assets_dir= "Assets/"
)
