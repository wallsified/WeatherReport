import os
import customtkinter as ctk
from PIL import ImageTk, Image

# Global Configurations
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("System")
global_dir = os.path.dirname(__file__)
graphic_dir = os.path.join(global_dir, "Images")
bitmap = os.path.join(graphic_dir,"airplane.ico")

# Color Pallette
gray_blue = '#597f97'
clear_blue = '#c4cbd8'
gray = '#6c747c'
navy_blue = '#183251'
light_gray = '#c8c4c4'


class Welcome:


    """Ventana de Bienvenida"""
    def __init__(self):
        """Inicialización de la página principal"""
        
        # Creamos la ventana principal
        self.root = ctk.CTk(fg_color=clear_blue)
        self.root.title = "Bienvenidx al Sistema de Registro del Clima"
        #self.root.iconbitmap(os.path.join(graphic_dir,"airplane.ico"))
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        self.root.iconify()

        # Contenido de la ventana principal
        logo =  ctk.CTkImage(
            light_image = Image.open(os.path.join(graphic_dir, "logo.jpeg")),
            dark_image =  Image.open(os.path.join(graphic_dir, "logo.jpeg")),
            size= (350,350)
        )
        image_tag = ctk.CTkLabel(master=self.root, image= logo, text="", bg_color=clear_blue)
        image_tag.pack(pady = 15)       
        
        # Campos de Texto
        user_input_ask_string = "Ingresa Tu Búsqueda:"
        ctk.CTkLabel(master= self.root, text = user_input_ask_string).pack()
        self.search = ctk.CTkEntry(
            master=self.root, 
            placeholder_text="Ciudad, Vuelo, Código IATA...", 
            width= 400, 
            height= 20, 
            )
        # idk how this works, yet
        #self.search.insert(0, "Puedes buscar por Ciudad, Vuelo, Código IATA...")
        self.search.bind("<Button-1>", lambda e: self.search.delete(0, "end"))
        self.search.pack()

        # Boton de Envio de la información
        ctk.CTkButton(self.root, 
        text="Inicar Búsqueda",
        width= 400, 
        height= 20).pack(pady=10)
        
        self.root.mainloop()