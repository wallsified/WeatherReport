""" 
Ventana de Búsqueda del clima 
Author:  @wallsified
Version: 1.0
"""
# Librería Gráfica del Proyecto. Flutter adaptado a Python
import flet as ft

# Métodos de la clase general
import GUI.general_configurations as gc

# Métodos de la clase del elemento gráfico WeatherList
#import weather_list as wl

search_initation = gc.new_elevated_button()
search_initation.text = "Iniciar Busqueda"
search_initation.icon = ft.icons.SEARCH
search_initation.width= 250,
search_initation.height=50

search_title_button = gc.new_text_field()
search_title_button.label = "Ingresa tu Búsqueda"
search_title_button.width= 500
search_title_button.height = 50
search_title_button.autofocus = True
info_grid = gc.new_grid_view()

static_dictionary = {
	"flightone" : ['MTY', 25.7785, -100.107, 'MTY', 25.7785, -100.107],
 	"flightwo" : ['MEX', 25.7785, -100.107, 'MTY', 25.7785, -100.107]
}

#lista estática de prueba
static_list = ['MTY', 25.7785, -100.107, 'MTY', 25.7785, -100.107]

def items(count):
    """testeo de generación de n filas """
    item_array = []
    for i in range(1, count + 1):
        item_array.append(
            ft.DataTable(
                border=ft.border.all(1, "black"),
                border_radius=15,
                heading_row_height=50,
                divider_thickness=2,
                heading_text_style=ft.TextStyle(font_family='Caviar', size=13,
                            color="black", weight='W_300'),
                horizontal_margin=5,
                bgcolor=gc.CLEAR_BLUE,
                vertical_lines=ft.border.BorderSide(1, gc.NAVY_BLUE),
                column_spacing=25,
                width=1000,
                columns=[
                    ft.DataColumn(
                    ft.Text({static_list[0]}),
                    ),
                    ft.DataColumn(
                    ft.Text({static_list[1]}),
                    ),
                    ]
                )
            )
        return item_array

def main(page : ft.Page):
    """
    Método Main para poder ejecutar la Ventana Principal
    """

    page.bgcolor = gc.CLOUD_WHITE
    page.window_resizable = True
    page.window_max_height = "800"
    page.window_max_width = "1200"
    page.window_min_height = "300"
    page.window_min_width = "300"
    page.title = "Weather Reporter"
    page.fonts = {
        "Roboto Light": "/fonts/Roboto-Light.ttf",
        "Caviar": "fonts/CaviarDreams.ttf" 
    }

    #idea de una fila responsiva. Se vería como una tabla sin ser una.
    testing_row = ft.ResponsiveRow(
        [
            search_title_button,
            search_initation,
        ],
        run_spacing={"xs": 15},
    )

    other_testing_row = ft.ResponsiveRow(
        spacing=2, controls=items(10), )

    page.add(testing_row, other_testing_row)


ft.app(
    target= main,
    assets_dir= "Assets/"
)
