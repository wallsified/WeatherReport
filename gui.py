import flet as ft

import os
import sys
import time
import traceback

from weather import WeatherManager
from dataset import DatasetManager

from Levenshtein import distance

def main(page: ft.Page):

    page.title = "Titulo"
    page.add(ft.Text("Contenido"))

    time.sleep(0.1)
    
    def popup_repeat(text):
        dlg = ft.AlertDialog(
            title=ft.Text(text),
            on_dismiss=lambda e: popup_repeat(text)
        )
        page.show_dialog(dlg)
    

    apikey = os.environ.get("API_KEY")

    if apikey == None or apikey == "":
        print("No hay API_KEY en las variables de entorno")
        popup_repeat("No hay apikey")
        return


    if os.path.exists("dataset.csv") == False:
        print("El archivo dataset.csv no existe/no fue encontrado")
        popup_repeat("No hay dataset")
        return

    data = DatasetManager()
    weather = WeatherManager(data)

    def search(e, data):
        if not txt_search.value:
            print("no hay texto")
            return

        if btn_search.disabled:
            return

        btn_search.disabled = True
        page.update()
        
        text = txt_search.value
        iatas = data.get_iatas(text)
        if iatas:
            iata_dest = iatas[1]
            data = weather.get(iata_dest)
            print("done")
            # print(data)
            btn_search.disabled = False
            page.update()
            return

        if data.is_valid_iata(text):
            data = weather.get(text)
            print("done")
            # print(data)
            btn_search.disabled = False
            page.update()
            return;

        
        names_sorted = sorted(data.get_names_list(), key=lambda n: distance(text, n))
        iata = data.get_iata(names_sorted[0])
        print(iata)
        if not data.is_valid_iata(iata):
            btn_search.disabled = False
            return
        data = weather.get(iata)
        print("done")
        # print(data)
        btn_search.disabled = False
        page.update()
        return

    txt_search = ft.TextField(label="Ciudad")
    page.add(txt_search)
    btn_search = ft.ElevatedButton("Buscar", on_click=lambda e: search(e, data))
    page.add(btn_search)


    return
