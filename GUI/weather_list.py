"""
Tabla para mostrar información del caché en la GUI.
Author:  @wallsified
Version: 1.0
"""
# Librería Gráfica del Proyecto. Flutter adaptado a Python
import flet as ft
import general_configurations as gc

#https://flet.dev/docs/controls/responsiverow


ft.Page.fonts = {
    'Caviar': 'Assets/fonts/CaviarDreams.ttf'
}


def table_headers():
    """
    Método para crear los encabezados de la tabla para mostrar
    la información resultante de la búsqueda.
    """
    return ft.DataTable(
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
                ft.Text("IATA\n\tPartida"),
                #on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                tooltip="Identificador IATA del Lugar de Origen"
            ),
            ft.DataColumn(
                ft.Text("Latitud\n\t\tPartida"),
                #on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                tooltip="Latitud del Lugar de Origen"
            ),
            ft.DataColumn(
                ft.Text("Longitud\n\tPartida"),
                #on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                tooltip="Longitud del Lugar de Origen"
            ),
            ft.DataColumn(
                ft.Text("Clima\n\tPartida"),
                #on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                tooltip="Clima del Punto de Partida"
            ),
            ft.DataColumn(
                ft.Text("IATA\n\tDestino"),
                #on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                tooltip="Identificador IATA del Lugar de Destino"
            ),
            ft.DataColumn(
                ft.Text("Latitud\n\tDestino"),
                #on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                tooltip="Latitud del Lugar de Destino"
            ),
            ft.DataColumn(
                ft.Text("Longitud\n\tDestino"),
                #on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                tooltip="Longitud del Lugar de Destino"
            ),
            ft.DataColumn(
                ft.Text("Clima\n\tDestino"),
                #on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                tooltip="Clima del Punto de Partida"
            ),
            ft.DataColumn(
                ft.Text("IATA\n\tDestino"),
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                tooltip="Valor IATA del Punto de Destino"
            ),
        ],
    )

def generate_row(lista):
    """ 
    Método para generar una fila con
    información definida
    """
    #esto para limitar el tamaño de la lista recibida

    def iterate_list():
        """Auxiliar para iterar sobre la lista."""
        for element in lista:
            return ft.DataCell(ft.Text(element))

    return ft.Row([
        iterate_list()
    ])

def table_content(dictionary):
    """
    Método para generar las filas para llenar la tabla
    resultante de la búsqueda de información. 
    """

    def iterate_dictionary():
        """ Misma idea"""
        for lista in dictionary:
            return generate_row(lista=lista)

    return ft.DataTable(
        rows=[
            iterate_dictionary()
        ]
    )
