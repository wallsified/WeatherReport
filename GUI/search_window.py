""" 
Ventana de Búsqueda del clima 
Author:  @wallsified
Version: 1.0
"""
# Métodos de la clase general
import general_configurations as gc

# Métodos de la clase del elemento gráfico WeatherList
import weather_list as wl

# Librería Gráfica del Proyecto. Flutter adaptado a Python
import flet as ft

search_initation = gc.new_elevated_button()
search_initation.text = "Iniciar Busqueda"
search_initation.icon = ft.icons.SEARCH
search_initation.width = "250"
search_initation.height = "30"

search_title_button = gc.new_text_field()
search_title_button.label = "Ingresa tu Búsqueda"
search_initation.width = "200"
search_initation.height = "50"


def main(page : ft.Page):
    """
    Método Main para poder ejecutar la Ventana Principal
    
    """
    #page.bgcolor = gc.CLEAR_BLUE
    page.window_resizable = True
    page.window_max_height = "800"
    page.window_max_width = "800"
    page.window_min_height = "300"
    page.window_min_width = "300"
    page.window_full_screen = False
    page.title = "Weather Reporter"
    page.fonts = {
        "Roboto Light": "/fonts/Roboto-Light.ttf"
    }

    top_row = ft.Row(
        controls=[
            search_title_button,
		    search_initation,

        ],
        spacing = "40",
        alignment= ft.alignment.center
    )

    second_row = ft.Row(
        controls=[
            wl.weather_table()
        ],
        spacing = "10",
        alignment= ft.alignment.center
    )

    page.add(top_row, second_row)


ft.app(
    target= main,
    assets_dir= "assets/"
)
