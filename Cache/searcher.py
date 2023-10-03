"""
Archivo que implementa el Algoritmo
de Levenstein para poder buscar en
el caché

Author: @TheSinotec
Version: 1.1

"""

# Libreria para lectura del dataset *.csv
import csv
# Libreria para manejo de fecha y hora del computador
import datetime
# Libreria para generar espacios de tiempo de ejecución
import time
# Libreria del método levenshtein
from Levenshtein import distance
# Se importan los métodos del documento cache.py
import Cache.cache as cache
# Se importan los métodos del documento dataset.py
from Cache.dataset import DatasetManager

# Variable global, nombre del dataset definido en el cache
DTS = cache.DATA_SET


def ticket_management():
    '''
    Función que genera un diccionario con los tickets y
    los iatas asociados en lista [origin, destination] según el dataset

    Retorna
    -------
        *reg: dict
            La lectura del dataset
            Formato predeterminado: {"num_ticket0": ["iata_origin0", "iata_destination0"]
            ,"num_ticket1": ["iata_origin1", "iata_destination1"],...}
    '''
    reg = {}
    try:
        with open(file= DTS, newline='', encoding= "utf-8") as file:
            data = csv.DictReader(file)
            for row in data:
                reg[row['num_ticket']] = [row['origin'], row['destination']]
    except FileNotFoundError:
        pass
    return reg


def take_from_cache(regs: dict, cach: dict, origin: str = '', destination: str = ''):
    '''
    Función que genera una lista con los datos
    necesarios para mostrar en los registros de la busqueda

    Toma los registros del dataset y el cache de la API para
    conglomerar los climas con cada origen y destino

    Parametros:
        *regs: dict
            De valor predeterminado {}.
            Recibe la lectura del dataset según el retorno de la
            función iata_registration() del cache, si no, manda
            registros NULL (error en el diccionario)
        *cach: dict
            De valor predeterminado {}.
            Recibe la lectura del cache según el retorno de la función
            get_cache(reset=False) del cache, si no, manda registros NULL
            (error en el diccionario)
        *origin: str
            De valor predeterminado ''.
            Recibe un código IATA origin, si no, manda registros NULL (error en el IATA)
        *destination: str
            De valor predeterminado ''.
            Recibe un código IATA destination, si no, manda registros NULL (error en el IATA)

    Retorna
    -------
        *datalist: list
            Manda una lista de formato [iata_origin:str, lat_origin:float,
            lon_origin:float, weather_origin:str, range_temperature_origin:str,
                humidity_origin:str, iata_destination:str,
               lat_destination:float, lon_destination:float, weather_destination:str,
                range_temperature_destination:str,
            humidity_destination:str]
    '''
    datalist = []
    hour = datetime.datetime.now().hour
    if cach == regs or origin == destination:
        datalist.extend(['NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'])
    else:
        for i in range(hour, 24):
            if cach['records'][origin][i] != ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']:
                hour = i
                break
        tempe = str(cach['records'][origin][hour][1]) + " / " + str(cach['records']
            [origin][hour][2])
        datalist.extend([origin, regs[origin][0], regs[origin][1],
                         cach['records'][origin][hour][0], tempe, cach['records'][origin][hour][3]])
        if hour < 22:
            tempe = str(cach['records'][origin][hour + 2][1]) + " / " + str(
                cach['records'][origin][hour + 2][2])
            datalist.extend([destination, regs[destination][0], regs[destination][1],
                             cach['records'][destination][hour + 2][0], tempe, cach['records']
                             [origin][hour + 2][3]])
        else:
            datalist.extend(['NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'])
    return datalist


def search_cache(txt: str = ''):
    '''
    Función que genera una lista de listas del formato de la
    función take_from_cache() según un texto de busqueda

    Toma un string buscado y genera una busqueda por iata, por
    ticket o por el método levenshtein, regresa una lista de listas
    con todas las busquedas coincidentes. En caso que el caché no se
    haya generado espera a que este termine de procesar.

    Parametros
    ----------
        *txt: str
            De valor predeterminado ''.

    Retorna
    -------
        *result: list
            Manda una lista de listas con el formato del método take_from_cache()
    '''
    while cache.act_runs.is_set():
        time.sleep(1)
    regs = cache.iata_registration()
    tickets = ticket_management()
    cach = cache.get_cache(reset=False)
    result = []
    if txt in tickets.keys():
        result.append(take_from_cache(regs, cach, tickets[txt][0], tickets[txt][1]))
    elif txt in regs.keys():
        reglist = []
        for i in tickets.values():
            if i not in reglist:
                if txt == i[0]:
                    reglist.append(i)
                    result.append(take_from_cache(regs, cach, i[0], i[1]))
                elif txt == i[1]:
                    reglist.append(i)
                    result.append(take_from_cache(regs, cach, i[0], i[1]))
    else:
        mngr = DatasetManager()
        valid_names = mngr.get_valid_names_list()
        names_sorted = sorted(valid_names, key = lambda n: distance(txt.lower(),
                                                                    n.lower(), weights=(1, 2, 3)))
        for i in range(3):
            iat = mngr.get_iata(names_sorted[i])
            lst = search_cache(iat)
            result.extend(lst)
    return result
