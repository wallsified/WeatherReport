"""
Ventana de la Búsqueda del Clima,
ahora en versión Orientada a Objetos.

Author:  @wallsified
Version: 1.3
"""

# Librerias para el control de Modulos
import sys
from pathlib import Path
import os

# Libreria que nos permite tener lo más cercano a variables finales.
from typing import Final

# Libería Gráfica
import flet
from flet import (
    border, border_radius, Column, Container,
    GridView, Page, Row,
    SnackBar,Text, TextField,
    UserControl, alignment, icons,
    KeyboardType, ElevatedButton,
    ButtonStyle, MaterialState, colors
)

path_to_module = Path(__file__).parents[1]
sys.path.append(str(path_to_module))

# Se mantiene en esta linea para que al ir interpretando el archivo
# la aplicación sepa de donde hacer el import.
from Cache import cache, searcher

# Paleta de Colores
GRAY_BLUE: Final = '#597f97'
CLEAR_BLUE: Final = '#c4cbd8'
GRAY: Final = '#6c747c'
NAVY_BLUE: Final = '#183251'
LIGHT_GRAY: Final = '#c8c4c4'
CLOUD_WHITE: Final = "#ecf0f1"

os.environ["FLET_WS_MAX_MESSAGE_SIZE"] = "8000000"

class WeatherSearcher(UserControl):
    """
    Clase para poder buscar el clima en la GUI.
    Ahora nos basamos en tener un objeto GridView
    y refrescar dicho elemento en lugar de la ventana
    en si.

    Esto nos permite hacer la GUI más rapida para interactuar
    y funciona todo dentro del mismo archivo.

    Parametros
    ----------
        - UserControl: Nos permite interactuar con la GUI. Es una
            particularidad de usar Flet.

    """
    cache.run_cache()

    def __init__(self, expand=False, height=500):
        super().__init__()
        if expand:
            self.expand = expand
        else:
            self.height = height

    def build(self):
        """
        Esta es la función de "creación" de la clase.
        Nuevamente, es una particularidad de la librería
        gráfica.

        """

        search_txt = TextField(
            expand=1,
            label= "Ingresa tu Búsqueda",
            hint_text="Puedes Buscar por IATA, Ciudad, No.Ticket",
            autofocus=True,
            text_size= 14,
            max_lines=1,
            multiline= False,
            max_length= 20,
            filled= True,
            border_color= NAVY_BLUE,
            keyboard_type= KeyboardType.TEXT,
            width= 400,
            #height= 60,
            on_submit=lambda e: display_icons(e.control.value),
        )

        def search_click(event):
            display_icons(search_txt.value)

        search_button = ElevatedButton(
            style= ButtonStyle(
            color={
                MaterialState.HOVERED: colors.WHITE,
                MaterialState.FOCUSED: colors.WHITE,
                MaterialState.DEFAULT: colors.BLACK,
                },
            padding= 5,
            overlay_color= colors.TRANSPARENT,
            elevation={"pressed": 0, "": 1},
            bgcolor={MaterialState.HOVERED: NAVY_BLUE, "": CLEAR_BLUE},
            ),
            icon = icons.SEARCH,
            text = "Buscar",
            width= 150,
            height= 50,
            on_click = search_click
        )

        search_query = Row(
            [search_txt, search_button],
            spacing= 10,
            wrap = False
        )

        search_results = GridView(
            expand=1,
            runs_count=10,
            max_extent= 150,
            spacing=5,
            run_spacing=5,
            child_aspect_ratio=1.0,
            horizontal= False
        )
        status_bar = Text()

        def display_icons(search_term: str):

            # clean search results
            search_query.disabled = True
            self.update()
            search_results.clean()

            for index, sublista in enumerate(searcher.search_cache(search_term)):
                for data in sublista:
                    search_results.controls.append(
                        # ? Posible cambio a un DataTable.
                        Container(
                            Text(value=data),
                            alignment= alignment.center,
                            border_radius= border_radius.all(5),
                            border= border.all(width=2, color= NAVY_BLUE),
                            width=60,
                            height=20,
                            padding=15,
                    )
                )
                self.update()

            # BUG: Aunque si muestra el mensaje, momentaneamente aparecen los falsos positivos.
            if len(search_results.controls) == 0 or len(search_term) == 0:
                self.page.show_snack_bar(SnackBar(Text("Tu búsqueda no arrojó resultados"),
                    open=True))
                search_results.clean()

            search_query.disabled = False
            self.update()

        return Column(
            [
                search_query,
                search_results,
                status_bar,
            ],
            expand=True,
        )


def main(page: Page):
    """
    Main de la ventana de ejecución
    """
    page.title = "Weather Reporter"
    page.fonts = {
        "Roboto Light": "/fonts/Roboto-Light.ttf",
        "Caviar": "fonts/CaviarDreams.ttf"
    }
    page.add(WeatherSearcher(expand=True))


flet.app(target=main)
