"""
Principal Ventana de la GUI. (Idealmente)

10/sept/23: Si, no es mucho. Pero era necesario intentar 
con una nueva libreria por que customtkinter se veia medio 
extraño. Flet permite usar las guias de Material Design de 
Google ya que es un wrapper (y añadidos) de Flutter

Author:  @wallsified
Version: 1.0
"""
import flet as ft

# Paleta de Colores de la GUI
GRAY_BLUE = '#597f97'
CLEAR_BLUE = '#c4cbd8'
GRAY = '#6c747c'
NAVY_BLUE = '#183251'
LIGHT_GRAY = '#c8c4c4'

def main(page : ft.Page):
    """Método Main para poder ejecutar la Ventana Principal
    
    Parameters: 
        page: Recibe una página (o un self) para poder iniciar modificaciones
    """

    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 15
    page.fonts = {
        "Roboto_Light": "fonts/Roboto-Light.ttf",
    }

    def elevated_was_clicked(event):
        """Prueba de función para un botón. 
        
        Parameters:
            event: La biblioteca ocupa un parámetro en tiempo ejecución para referirse
                   a lo que está aconteciendo la GUI. Sin embargo, no se ocupa para 
                   alguna otra función. Por convencción, se le llama "event".
        
        Returns: 
            Cuantas veces se ha presionado el botón.  
        
        """
        boton_inicio.data +=1
        boton_texto.value = f"Search Times: {boton_inicio.data}"
        page.update()

    #Se pueden crear variables de "objetos" gráficos y solo llamarlos.
    boton_inicio = ft.ElevatedButton(text = "Iniciar Busqueda", icon= ft.icons.AIRPLANEMODE_ACTIVE,
                               icon_color = NAVY_BLUE, on_click= elevated_was_clicked, data= 0)
    boton_texto = ft.Text(font_family="Roboto_Light")

    imagen_central = ft.Image(
        src= "images/logo.jpg",
        width= 330,
        height= 330,
        fit = ft.ImageFit.CONTAIN
    )

    # Se construye primero cada fila y posteriormente las columnas. Imagina una estructura matriz.
    row1 = ft.Row(controls=[
        boton_inicio,
		boton_texto
	])

    column1 = ft.Container(
		width=1000,
		bgcolor=CLEAR_BLUE,
		border_radius= 20,
		padding= 20,
  		content= row1
	)

    column2 = ft.Container(
		width=1000,
		bgcolor=CLEAR_BLUE,
		border_radius= 20,
		padding= 20,
  		content= imagen_central
	)

    page.add(column2, column1)

ft.app(
    target= main,
    assets_dir="assets"
)
