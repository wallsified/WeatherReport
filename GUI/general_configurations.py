"""
Configuraciones Principales de la GUI.
Author:  @wallsified
Version: 1.0

Notas:
Flet permite cambiar parámetros de cada elemento gráfico a posteriori, pero
necesita tener algunos valores de por medio declarados como en los métodos
siguientes.

"""
from typing import Final
import flet as ft

# Paleta de Colores de la GUI. La declaración de esta forma es lo más parecido a un "final"
GRAY_BLUE: Final = '#597f97'
CLEAR_BLUE: Final = '#c4cbd8'
GRAY: Final = '#6c747c'
NAVY_BLUE: Final = '#183251'
LIGHT_GRAY: Final = '#c8c4c4'


def new_elevated_button():
    """ 
	Método para construir una instancia de ElevatedButton
	con caracterísitcas fijas. 
	
    """
    return ft.ElevatedButton(
		style= ft.ButtonStyle
			(color= {
				ft.MaterialState.HOVERED: ft.colors.WHITE,
				ft.MaterialState.FOCUSED: ft.colors.WHITE,
				ft.MaterialState.DEFAULT: ft.colors.BLACK,
				},
			overlay_color=ft.colors.TRANSPARENT,
			elevation={"pressed": 0, "": 1},
			bgcolor={ft.MaterialState.HOVERED: NAVY_BLUE, "": CLEAR_BLUE}
				)
	)

def new_text_button():
    """ 
    Método para construir una instancia de TextButton
    con caracterísitcas fijas. 
    """
    return ft.TextButton(
		style=ft.ButtonStyle(
		padding={ft.MaterialState.HOVERED: 20},
		# BUG: overlay_color=ft.colors.TRANSPARENT,
		# BUG: elevation={"pressed": 0, "": 1},
		animation_duration=200
		)
	)

def new_text_field():
    """ 
	Método para construir una instancia de TextField
	con caracterísitcas fijas. 
	
    """
    return ft.TextField(
		border_color = NAVY_BLUE,
		keyboard_type= ft.KeyboardType.TEXT,
		max_lines= "1",
		multiline= False,
		disabled= False,
		capitalization= ft.TextCapitalization.WORDS,
		filled= True,
	)