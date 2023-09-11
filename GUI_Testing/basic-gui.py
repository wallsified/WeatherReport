import customtkinter as ctk

def print_something():
    print("Button Pressed")

general_app = ctk.CTk()
general_app.title("Hello World")
general_app.geometry("400x150")
general_app.grid_columnconfigure(0, weight = 1)
general_app.grid_rowconfigure(0, weight = 1)

test_button = ctk.CTkButton(
master= general_app, text="Click Me!", corner_radius=3, command = print_something())
test_button.grid(row = 0, column = 0, padx = 20, pady = 20)


checkbox_1 = ctk.CTkCheckBox(master=general_app, text="checkbox 1")
checkbox_1.grid(row=2, column=2, padx=20, pady=(0, 20), sticky="w")
checkbox_2 = ctk.CTkCheckBox(master=general_app, text="checkbox 2")
# Aqui padY recibe tuplas. tiene sentido. Imagina una grid de css
# el primer argumento es pad superior, el segundo es pad inferior
checkbox_2.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")


general_app.mainloop()

# y esto se puede hacer una clase.