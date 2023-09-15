"""
Tabla para mostrar información del caché en la GUI.
Author:  @wallsified
Version: 1.0
"""
# Librería Gráfica del Proyecto. Flutter adaptado a Python
import flet as ft

def weather_table():
    """
	Método para crear una tabla con la información
 	del clima según la búsqueda realizada en el caché
    """
    return ft.DataTable(
		border= ft.border.all(1,"black"),
		sort_column_index=0,
		sort_ascending=True,
		heading_row_height=50,
		divider_thickness=2,
		column_spacing=30,
		width= 800,
		columns=[

   			ft.DataColumn(
				ft.Text("No. Ticket"),
				on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
				tooltip= "Valor Alfanumérico Identificador del Ticket"
				),

			ft.DataColumn(
				ft.Text("IATA Partida"),
				on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
				tooltip= "Valor IATA del Punto de Partida"
				),

   			ft.DataColumn(
				ft.Text("Clima Partida"),
				on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
				tooltip= "Clima del Punto de Partida"
				),

			ft.DataColumn(
				ft.Text("IATA Destino"),
				on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
				tooltip= "Valor IATA del Punto de Destino"
				),

			ft.DataColumn(
				ft.Text("Clima Destino"),
				on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
				tooltip= "Clima del Punto de Destino"
			),
		],

		rows = [
			ft.DataRow(
					#esta es la parte que se debe de llenar buscando en la caché / llamando a API
								cells=[
					ft.DataCell(ft.Text("#1")),
					ft.DataCell(ft.Text("MEX")),
					ft.DataCell(ft.Text("Nublado")),
									ft.DataCell(ft.Text("USA")),
					ft.DataCell(ft.Text("Tormenta Eléctrica")),
				]
			)
		]
	)
