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
    TextStyle, DataTable, DataColumn,
    FontWeight
)

# Esto garantiza orden en la estructura y que al momento de
# interpretar el archivo no tengamos errores de tipo "ModuleNotFoundError"
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

    Métodos
    -------
        __init__: Método constructor de la clase WeatherSearcher
        build: Es donde propiamente se crea la funcionalidad de la clase. 

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
        Funcionalidad de la clase. 
        El nombre "build" es una particularidad 
        de la librería. 

        Regresa
        -------
            Column: Elemento gráfico Columna en donde se acomodan 
                    los diferentes elementos que construyen la clase:
                    botones y entradas de búsqueda, indicadores y 
                    resultados de la búsqueda.

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
            max_length= 16, #Longitud máxima de ID del boleto
            filled= True,
            border_color= NAVY_BLUE,
            keyboard_type= KeyboardType.TEXT,
            width= 400,
            on_submit=lambda e: display_icons(e.control.value),
        )

        # Acción a realizar cuando se hace click en el boton de búsqueda
        def search_click(event):
            display_icons(search_txt.value)

        # Botón de búsqueda
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
        search_results_grid = GridView(
            expand=1,
            runs_count=15,
            max_extent= 110,
            spacing=8,
            run_spacing=8,
            child_aspect_ratio=1,
        )

        # Headers para señalizar la información en pantalla
        departure_arrival_headers = DataTable(
            border= border.all(1, NAVY_BLUE),
            border_radius=15,
            heading_row_height=40,
            #divider_thickness=2,
            bgcolor= NAVY_BLUE,
            heading_text_style= TextStyle(size=15,
                                        weight='W_500', color = CLOUD_WHITE,),
            vertical_lines=border.BorderSide(5, CLOUD_WHITE),
            #column_spacing=50,
            width=1500,
            columns= [
                DataColumn(
                    Text(value= "Información Lugar de Partida", text_align= 'JUSTIFY'),
                        tooltip="Información de la Ubicación de Partida"
                ),
                DataColumn(
                    Text(value= "Información Lugar de Llegada",text_align= 'JUSTIFY'),
                        tooltip="Información de la Ubicación de Llegada"
                ),
            ]
        )

        information_headers = DataTable(
            border= border.all(2, NAVY_BLUE),
            border_radius=15,
            heading_row_height=100,
            divider_thickness=2,
            heading_text_style= TextStyle(size=15,
                                      color=NAVY_BLUE, weight='W_500'),
            vertical_lines=border.BorderSide(2, NAVY_BLUE),
            column_spacing=28,
            width=1500,
            columns=[
                        DataColumn(
                            Text(value= "Código\n\tIATA", text_align= 'JUSTIFY'),
                            tooltip="Identificador IATA del Lugar de Origen"
                        ),
                        DataColumn(
                            Text(value= "   Latitud   ",text_align= 'JUSTIFY'),
                            tooltip="Latitud del Lugar de Origen"
                        ),
                        DataColumn(
                            Text(value= "   Longitud   ", text_align= 'JUSTIFY'),
                            tooltip="Longitud del Lugar de Origen"
                        ),
                        DataColumn(
                            Text("   Clima   ", text_align= "JUSTIFY"),
                            tooltip="Clima del Punto de Partida"
                        ),
                        DataColumn(
                            Text(value= "Temp.\nMin./Max.", text_align= "JUSTIFY"),
                            tooltip= "Temperaturas del Punto de Partida"
                        ),
                        DataColumn(
                            Text(value= "        %\nHumedad", text_align= "JUSTIFY"),
                            tooltip= "Humedad del Punto de Partida"
                        ),
                        DataColumn(
                            Text(value=" Código\n IATA ", text_align= 'JUSTIFY'),
                            tooltip="Identificador IATA del Lugar de Destino"
                        ),
                        DataColumn(
                            Text(value="   Latitud   ", text_align= 'JUSTIFY'),
                            tooltip="Latitud del Lugar de Destino"
                        ),
                        DataColumn(
                            Text(value="   Longitud   ", text_align= 'JUSTIFY'),
                            tooltip="Longitud del Lugar de Destino"
                        ),
                        DataColumn(
                            Text(value="   Clima   ", text_align= 'JUSTIFY'),
                            tooltip="Clima del Punto de Destino"
                        ),
                        DataColumn(
                            Text(value= "Temp.\nMin./Max.", text_align= "JUSTIFY"),
                            tooltip= "Temperaturas del Punto de Destino"
                        ),
                        DataColumn(
                            Text(value= "        %\nHumedad", text_align= "JUSTIFY"),
                            tooltip= "Humedad del Punto de Destino"
                        ),
                    ],
        )

        def display_icons(search_term: str):
            """
            Función para mostrar en pantalla los resultados 
            de la búsqueda del clima, buscando en caché. 

            Parametros
            ----------
                search_term: Término de búsqueda ingresado para consultar.
            """

            # Se limpian las entradas previas con cada búsqueda.
            search_query.disabled = True
            self.update()
            search_results_grid.clean()

            if len(search_term) == 0:
                search_results_grid.clean()
                self.page.show_snack_bar(SnackBar(content=
                Text("La Búsqueda No Arrojó Resultados. Favor de Intentar de nuevo.",
                color= CLOUD_WHITE),
                    open=True, bgcolor= NAVY_BLUE, duration= 2000, close_icon_color= True,))
                #weather_results = []
            else:
                for index, sublista in enumerate(searcher.search_cache(search_term)):
                    for data in sublista:
                        search_results_grid.controls.append(
                            Container(
                                Text(
                                    value=f"{data}",
                                    size=14,
                                    width=90,
                                    height= 40,
                                    text_align="center",
                                    weight= FontWeight.W_500
                                ),
                            border= border.all(width= 1.5, color = NAVY_BLUE),
                            alignment= alignment.center,
                            bgcolor = CLEAR_BLUE,
                            border_radius= border_radius.all(15)
                            )
                        )
                    self.update()

            search_query.disabled = False
            self.update()

        return Column(
            [
                search_query,
                departure_arrival_headers,
                information_headers,
                search_results_grid,
            ],
            expand=True,
        )


def main(page: Page):
    """
    Main de la ventana de ejecución.
    """

    page.title = "Weather Reporter"
    #? Si esta creando con las fuentes de aqui?
    page.fonts = {
        "Roboto Light": "/fonts/Roboto-Light.ttf",
        "Caviar": "fonts/CaviarDreams.ttf"
    }
    page.window_focused = True
    page.add(WeatherSearcher(expand=True))


flet.app(target=main)
