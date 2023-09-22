""" 
Archivo de Manejo del Caché 
Author: @TheSinotec
Version: 1.0
"""
# Libreria para lectura del DATA_SET *.csv
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
global TIMER_RUNS, THREAD, API_KEY, JSON_CACHE, DATA_SET, ACT

# Subprocesos definidos
act = threading.Event()
TIMER_RUNS = threading.Event()

# Llaves, nombre del archivo caché y del DATA_SET empleado, respectivamente
API_KEY = '5e31a7313683592fc55490ec53637486'
JSON_CACHE = 'Results/cache.json'
DATA_SET = 'Resources/dataset.csv'


def cache_flag(*, reiniciar: bool = False):
    '''
    Función que verifica el estado y/o crea el archivo de caché *.json.
    Reinicia el caché según el parametro reiniciar, además lee y verifica
    la caducidad del caché en caso de existir un archivo de caché

    Parametros
    ----------
        * reiniciar: bool
            De valor predeterminado False.
            Para True, borra el caché actual y deja un archivo de formato predeterminado.
            Para False, lee el archivo y lo retorna en un diccionario

    Regresa
    -----
        * json_data: dict
            La lectura de un archivo json en variable dic
            Formato predeterminado (vacío): {"flag": "fecha:str", "Registros": {}}
            La clave "Registros" del diccionario es un diccionario con las IATAS como
            claves, y cada clave IATA es una lista formada por 24 horas obtenidas de la API.
            Cada lista de hora contiene una lista con los parámetros
            [clima:str, temperatura_min:int, temperatura_max:int, humedad: int, hora: int]
    '''

    if reiniciar:
        json_data = None
    else:
        try:
            with open(JSON_CACHE, mode = 'r', encoding= "utf-8") as file:
                json_data = json.load(file)
                print('Caché habil')
                cache_check(json_data)
        except (FileNotFoundError, json.JSONDecodeError) as error:
            print(f'Cache no encontrado..({error})')
            json_data = None

    if not json_data:
        json_data = {}
        json_data['flag'] = str(datetime.datetime.now())
        json_data['Registros'] = {}
        print('Se creó el cache')
        with open(JSON_CACHE, mode = 'w', encoding= "utf-8") as file:
            json.dump(json_data, file)
    return json_data


def cache_check(flag: dict):
    '''
    Verifica que el diccionario-caché tenga a lo más 3 horas de antiguedad, 
    si excede el tiempo, actualiza caché

    Parametros
    ----------
        * flag: dict
            Diccionario del tipo predeterminado de caché
    '''
    
    tiempo_cache = datetime.datetime.strptime(flag['flag'], "%Y-%m-%d %H:%M:%S.%f")
    tiempo_act = datetime.datetime.now()

    if (tiempo_act - tiempo_cache) >= datetime.timedelta(hours=3):
        cache_update()
    else:
        print("Cache actualizado")


def timer():
    '''
    Función que ejecuta el subproceso analizer() Emplea las variables globales 
    Thread y TIMER_RUNS
    '''
    TIMER_RUNS.set()
    #global THREAD
    THREAD = threading.Thread(target=analizer, args=(TIMER_RUNS,))
    THREAD.start()


def analizer(TIMER_RUNS):
    '''
    Si se llama la función timer() se verifica cada 3 horas el estado del caché.

    Mientras el programa funcione, se genera un subproceso que actualiza el caché cada 3 horas

    Parametros
    ----------
        TIMER_RUNS: Event
            Variable de tipo Global usada para generar el subproceso
    '''

    while TIMER_RUNS.is_set():
        print("Corre el tiempo")
        time.sleep(10800)
        flag = cache_flag(reiniciar=False)
        cache_check(flag)


def iata_registry():
    '''
    Función que lee el DATA_SET *.csv y regresa los codigos IATA con
    sus (Latitud, Longitud) correspoindientes

    Almacena los IATA code junto con sus latitudes y longitudes (sea de llegada o salida)
    sin repetir entradas del data set.

    Usa la variable Global DATA_SET: str, que es el nombre del archivo csv

    Regresa
    -------
        regs: dict
            Diccionario que contiene
            {'Registros': [[IATA0:str, Lat0:float, Lon0:float],
            [IATA1:str, Lat1:float, Lon1:float],...]}
            según lo obtenido en el DATA_SET
    '''
    regs = {}
    regs['Registros'] = []

    try:
        with open(DATA_SET, newline='', encoding= "utf-8") as file:
            data = csv.DictReader(file)
            for row in data:
                try:
                    if [row['origin'], float(row['origin_latitude']),
                        float(row['origin_longitude'])] not in regs['Registros']:
                        regs['Registros'].append([row['origin'], float(row['origin_latitude']),
                            float(row['origin_longitude'])])
                    if [row['destination'], float(row['destination_latitude']),
                        float(row['destination_longitude'])] not in regs['Registros']:
                        regs['Registros'].append([row['destination'],
                            float(row['destination_latitude']),float(row['destination_longitude'])])
                except ValueError:
                    print("Error en valores")
    except FileNotFoundError:
        print("No se encontró " + DATA_SET)

    return regs


def recache():
    '''
    Si se llama la función cache_update() se actualiza en segundo plano
    el contenido del archivo *.json

    Reinicia el caché actual y usa los registros no redundantes de iata_registry()
    para hacer un diccionario/archivo *.json. Se llama a la API para cada IATA
    segun sus coordenadas usando la libreria Weather.py. Además que se ejecuta en
    segundo plano mientras actualiza y evita más de 60 llamadas por minuto.

    '''
    regs = iata_registry()
    flag = cache_flag(reiniciar=True)
    with open(JSON_CACHE, mode = 'r', encoding= "utf-8") as file:
        data = json.load(file)
    for i in range(0, len(regs['Registros'])):
        if (i + 1) % 60 == 0:
            print("Actualizando")
            time.sleep(60)
        data['Registros'][str(regs['Registros'][i][0])] = []
        wter = weather.WeatherApi.get_weather_array(regs['Registros'][i][1],
                                                  regs['Registros'][i][2], API_KEY)
        if isinstance(wter, list) is False:
            print("Error al llamar a la API")
            break
        for k in range(23):
            try:
                data['Registros'][str(regs['Registros'][i][0])].append(
                    [wter[k].climate, wter[k].temp_min, wter[k].temp_max, wter[k].humidity,
                     wter[k].hour])
            except AttributeError:
                data['Registros'][str(regs['Registros'][i][0])].append(
                    ['NULL', 'NULL', 'NULL', 'NULL', 'NULL'])
        with open(JSON_CACHE, mode = 'w', encoding= "utf-8") as file:
            json.dump(data, file)

    print("Cache actualizado:", flag['flag'])
    TIMER_RUNS.clear()
    timer()
    return None


def cache_update():
    '''
    Función que ejecuta el subproceso recache(). Emplea la variable global act.
    '''
    #global ACT
    ACT = threading.Thread(target=recache)
    ACT.start()


def cache_initiate():
    '''
    Función que inicializa el proceso de cacheado de inicio del programa.
    Evita conflictos al abrir y cerrar el programa.
    Emplea las variabñe global act.
    
    '''
    act.clear()
    flag = cache_flag(reiniciar=False)
    if len(flag['Registros']) == 0:
        cache_update()
    else:
        timer()
    return None

if __name__ == '__main__':
    cache_initiate()
