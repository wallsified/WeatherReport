import customtkinter

from CTkTable import CTkTable

class Frame(customtkinter.CTkFrame):
    def __init__(self):
        super().__init__(self)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

value = [[1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5]]

app = customtkinter.CTk()
app.frame = Frame()
table = CTkTable(master=app, row=5, column=5, values=value)
table.pack(expand=True, fill="both", padx=20, pady=20)
app.mainloop()
