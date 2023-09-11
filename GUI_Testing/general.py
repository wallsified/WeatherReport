""" Librerias """
#import os
import customtkinter as ctk

# Color Pallette
GRAY_BLUE = '#597f97'
CLEAR_BLUE = '#c4cbd8'
GRAY = '#6c747c'
NAVY_BLUE = '#183251'
LIGHT_GRAY = '#c8c4c4'

# Global Configurations
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("System")

class Frame(ctk.CTkFrame):
    """Clase Frame
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.fg_color = NAVY_BLUE
        self.border_color = NAVY_BLUE
        self.button = ctk.CTkButton(self)
        self.button._bg_color = GRAY_BLUE
        self.button._hover_color = NAVY_BLUE
        self.button._text = "Un Boton"
        self.button.corner_radius = "5"

class Application(ctk.CTk):
    """App """
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.frame = Frame(master=self)
        self.frame.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "nsew")


app = Application()
app.mainloop()
