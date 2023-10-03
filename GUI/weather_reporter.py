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
    border, border_radius, Column,
    Container, GridView, Page, Row,
    SnackBar,Text, TextField,
    UserControl, alignment, icons,
    KeyboardType, ElevatedButton,
    ButtonStyle, MaterialState, colors,
    DataTable, DataColumn, DataRow,
    DataCell, TextStyle
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
        # Campo de Búsqueda
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

        # Botón de búsqueda
        # TODO Corregir estilo.
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

        # Fila de Búsqueda. Campo de Búsqueda + Botón.
        search_query = Row(
            [search_txt, search_button],
            spacing= 10,
            wrap = False
        )

        # Vista de Resultados
        # ? Es necesario usar esto al añadir un DataTable?
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

        new_search_results = DataTable(
            border= border.all(1, NAVY_BLUE),
            border_radius=15,
            heading_row_height=100,
            divider_thickness=2,
            heading_text_style= TextStyle(size=15,
                                      color=NAVY_BLUE, weight='W_500'),
            #bgcolor=CLEAR_BLUE,
            vertical_lines=border.BorderSide(1, NAVY_BLUE),
            column_spacing=40,
            width=1500,
            columns=[
                        DataColumn(
                            Text(value= "IATA\nPartida", text_align= 'CENTER'),
                            tooltip="Identificador IATA del Lugar de Origen"
                        ),
                        DataColumn(
                            Text(value= "Latitud\nPartida",text_align= 'CENTER'),
                            tooltip="Latitud del Lugar de Origen"
                        ),
                        DataColumn(
                            Text(value= "Longitud\nPartida", text_align= 'CENTER'),
                            tooltip="Longitud del Lugar de Origen"
                        ),
                        DataColumn(
                            Text("Clima\nPartida"),
                            tooltip="Clima del Punto de Partida"
                        ),
                        DataColumn(
                            Text(value= "Temperaturas\nMínima / Máxima"),
                            tooltip= "Temperaturas del Punto de Partida"
                        ),
                        DataColumn(
                            Text(value= "Humedad\nPartida"),
                            tooltip= "Humedad del Punto de Partida"
                        ),
                        DataColumn(
                            Text(value="IATA\nDestino", text_align= 'CENTER'),
                            tooltip="Identificador IATA del Lugar de Destino"
                        ),
                        DataColumn(
                            Text(value="Latitud\nDestino", text_align= 'CENTER'),
                            tooltip="Latitud del Lugar de Destino"
                        ),
                        DataColumn(
                            Text(value="Longitud\nDestino", text_align= 'CENTER'),
                            tooltip="Longitud del Lugar de Destino"
                        ),
                        DataColumn(
                            Text(value="Clima\nDestino", text_align= 'CENTER'),
                            tooltip="Clima del Punto de Destino"
                        ),
                        DataColumn(
                            Text(value= "Temperaturas\nMínima / Máxima"),
                            tooltip= "Temperaturas del Punto de Destino"
                        ),
                        DataColumn(
                            Text(value= "Humedad\nDestino"),
                            tooltip= "Humedad del Punto de Partida"
                        ),
                    ],
        )

        def display_icons(search_term: str):

            # clean search results
            search_query.disabled = True
            self.update()
            search_results.clean()
            weather_results = searcher.search_cache(search_term)

            if len(search_term) == 0:
                search_results.clean()
                self.page.show_snack_bar(SnackBar(content= Text("Tu búsqueda no arrojó resultados", color= CLOUD_WHITE),
                    open=True, bgcolor= NAVY_BLUE, duration= 2000, close_icon_color= True, ))
                weather_results = []

            for index, sublista in enumerate(weather_results):
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

            search_query.disabled = False
            self.update()

        return Column(
            [
                search_query,
                new_search_results,
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
