import flet as ft

import os
import sys
import time
import traceback

from read_dataset import *
from weather import get_weather

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

    try:
        coords, tickets = read_tickets()
        names, names_list = read_names()
    except:
        traceback.print_exc()
        popup_repeat("Error al leer el dataset")
        return

    def search(e):
        if not txt_search.value:
            print("no hay texto")
            return

        if btn_search.disabled:
            return

        btn_search.disabled = True
        page.update()
        
        text = txt_search.value
        ticket = tickets.get(text)
        if ticket:
            iata_dest = ticket[1]
            lat, long = coords[iata_dest]
            data = get_weather(lat, long)
            print("done")
            # print(data)
            btn_search.disabled = False
            page.update()
            return

        coordenadas = coords.get(text)
        if coordenadas:
            data = get_weather(coordenadas[0], coordenadas[1])
            print("done")
            # print(data)
            btn_search.disabled = False
            page.update()
            return;

        
        names_sorted = sorted(names_list, key=lambda n: distance(text, n))
        iata = names[names_sorted[0]]
        print(iata)
        coordenadas = coords.get(iata)
        if coordenadas == None:
            btn_search.disabled = False
            return
        data = get_weather(coordenadas[0], coordenadas[1])
        print("done")
        # print(data)
        btn_search.disabled = False
        page.update()
        return

    txt_search = ft.TextField(label="Ciudad")
    page.add(txt_search)
    btn_search = ft.ElevatedButton("Buscar", on_click=search)
    page.add(btn_search)


    return
