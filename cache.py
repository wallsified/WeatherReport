"""
Archivo de Manejo y Gestión del Caché

Author: @TheSinotec
Version 1.0

"""

# Libreria para lectura del dataset *.csv
import csv
# Libreria para la lectura y escritura del caché *.json
import json
# Libreria para manejo de fecha y hora del computador
import datetime
# Libreria para crear procesos en segundo plano
import threading
# Libreria para generar espacios de tiempo de ejecución
import time
# Se importan las clases del documento Weather.py
import weather

# Variables globales para el uso de procesos y subprocesos internos
act_runs = threading.Event()
timer_runs = threading.Event()

# Llaves, nombre del archivo caché y del dataset empleado, respectivamente
API_KEY = '5e31a7313683592fc55490ec53637486'
JSON_CACHE = 'cache.json'
DATA_SET = 'dataset2.csv'


def get_cache(*, reset: bool = False):
    '''
    Función que verifica el estado y/o crea el archivo de caché *.json

    Reinicia el caché según el parametro reset, además lee 
    y verifica la caducidad del caché en caso de existir un archivo de caché

    Parametros
    ----------
        * reset: bool
            De valor predeterminado False.
            Para True, borra el caché actual y deja un archivo de formato predeterminado.
            Para False, lee el archivo y lo retorna en un diccionario

    Retorna
    -------
        *json_data: dict
            La lectura de un archivo json en variable dic
                Formato predeterminado (vacío): {"flag": "fecha:str", "records": {}}

                La clave "records" del diccionario es un diccionario con las IATAS 
                como claves, y cada clave IATA es una lista formada por 24 horas obtenidas 
                de la API. Cada lista de hora contiene una lista con los parámetros 
                [clima:str, temperatura_min:int, temperatura_max:int, humedad: int, hora: int]
    '''
    if reset:
        json_data = None
    else:
        try:
            with open(file= JSON_CACHE, mode= 'r', encoding= "utf-8") as file:
                json_data = json.load(file)
                check_cache(json_data)
        except(FileNotFoundError, json.JSONDecodeError) as e:
            json_data = None
    if not json_data:
        json_data = {'flag': str(datetime.datetime.now()), 'records': {}}
        with open(file = JSON_CACHE, mode='w', encoding= "utf-8") as file:
            json.dump(json_data, file)
    return json_data


def check_cache(cache: dict):
    '''
    Verifica que el diccionario-caché tenga a lo más 3 horas de antiguedad, 
    si excede el tiempo, actualiza caché.

    Parametros
    ----------
        * cache: dict
            Diccionario del tipo predeterminado de caché
    '''
    date_cache = datetime.datetime.strptime(cache['flag'], "%Y-%m-%d %H:%M:%S.%f")
    actual_date = datetime.datetime.now()
    if (actual_date - date_cache) >= datetime.timedelta(hours=3):
        update_cache()


def timer():
    '''Función que ejecuta el subproceso analyzer()
        Emplea la variable global:
            timer_runs: Event

    Parametros:
        No
    Reorno:
        No
    '''
    timer_runs.set()
    t = threading.Thread(target=analyzer, args=(timer_runs,))
    t.start()


def analyzer(timer_runs):
    '''Si se llama la función timer() se verifica cada 3 horas el estado del caché.

        Mientras el programa funcione, se genera un subproceso que actualiza el caché cada 3 horas

    Parametros:
        timer_runs: Event
            Variable de tipo Global usada para generar el subproceso
    Retorno:
        No
    '''
    while timer_runs.is_set():
        time.sleep(10800)
        cache = get_cache(reset=False)
        check_cache(cache)


def iata_registration():
    '''
    Función que lee el dataset *.csv y regresa los codigos IATA con sus 
    (Latitud, Longitud) correspoindientes
    
    Almacena los IATA code junto con sus latitudes y longitudes (sea de 
    llegada o salida) sin repetir entradas del data set.
    
    Usa la variable Global dataset: str, que es el nombre del archivo csv

    Retorno
    -------
        * regs: dict
            Diccionario que contiene {'IATA0:str': [Lat0:float, Lon0:float],
            'IATA1:str': [Lat1:float, Lon1:float],...]} según lo obtenido 
            en el dataset
    '''
    regs = {}
    try:
        with open(file= DATA_SET, newline='', encoding= "utf-8") as file:
            data = csv.DictReader(file)
            for row in data:
                try:
                    if row['origin'] not in regs.keys():
                        regs[row['origin']] = []
                        regs[row['origin']].append(float(row['origin_latitude']))
                        regs[row['origin']].append(float(row['origin_longitude']))
                    if row['destination'] not in regs.keys():
                        regs[row['destination']] = []
                        regs[row['destination']].append(float(row['destination_latitude']))
                        regs[row['destination']].append(float(row['destination_longitude']))
                except ValueError:
                    #print("Error en valores")
                    pass
    except FileNotFoundError:
        #print("No se encontró " + dataset)
        pass
    return regs


def cacher():
    '''
    Si se llama la función update_cache() se actualiza 
    en segundo plano el contenido del archivo *.json

    Reinicia el caché actual y usa los registros no redundantes 
    de iata_registration() para hacer un diccionario/archivo *.json. 
    Se llama a la API para cada IATA segun sus coordenadas usando la 
    libreria Weather.py. Además que se ejecuta en segundo plano mientras 
    actualiza y evita más de 60 llamadas por minuto.
    
    '''
    iat = list(iata_registration().items())
    cache = get_cache(reset=True)
    with open(file= JSON_CACHE, mode= 'r', encoding= "utf-8") as file:
        data = json.load(file)
    for i in range(0, len(iat)):
        if (i + 1) % 60 == 0:
            time.sleep(60)
        data['records'][iat[i][0]] = []
        wter = weather.WeatherApi.get_weather_array(iat[i][1][0],
                                                  iat[i][1][1], API_KEY)
        if not isinstance(wter, list):
            break
        for k in range(24):
            try:
                data['records'][iat[i][0]].append(
                    [wter[k].climate, wter[k].temp_min, wter[k].temp_max, wter[k].humidity,
                     wter[k].hour])
            except AttributeError:
                data['records'][iat[i][0]].append(['NULL', 'NULL', 'NULL', 'NULL', 'NULL'])
        with open(file = JSON_CACHE, mode = 'w', encoding= "utf8") as file:
            json.dump(data, file)
    timer_runs.clear()
    act_runs.clear()
    timer()
    return None


def update_cache():
    '''
    Función que ejecuta el subproceso cacher()
    Emplea las variables globales:
        * act_runs: Event
    '''
    act_runs.set()
    act = threading.Thread(target=cacher)
    act.start()


def run_cache():
    '''
    Función que inicializa el proceso de cacheado de inicio del programa
    Evita conflictos al abrir y cerrar el programa
    Emplea las variables globales:
        * act_runs: Event
    '''
    act_runs.clear()
    cache = get_cache(reset=False)
    if len(cache['records']) == 0:
        update_cache()
    else:
        timer()
    return None


if __name__ == '__main__':
    # Esto es una prueba del funcionamiento SOLO LA PRIMERA LINEA ES ESCENCIAL
    run_cache()
