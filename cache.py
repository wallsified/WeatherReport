#Libreria para lectura del dataset *.csv
import csv
#Libreria para la lectura y escritura del caché *.json
import json
#Libreria para manejo de fecha y hora del computador
import datetime
#Libreria para crear procesos en segundo plano
import threading
#Libreria para generar espacios de tiempo de ejecución
import time

#Se importan las clases del documento Weather.py
import Weather

#Variables globales para el uso de procesos y subprocesos internos
global timer_runs, t, apikey, json_cache, dataset, act
#Subprocesos definidos
act = threading.Event()
timer_runs = threading.Event()
#Llaves, nombre del archivo caché y del dataset empleado, respectivamente
apikey='INCERTE APLIKEY VALIDA'
json_cache='cache.json'
dataset='dataset2.csv'


def BanderaCache(*, reiniciar: bool = False):
    '''Función que verifica el estado y/o crea el archivo de caché *.json

        Reinicia el caché según el parametro reiniciar, además lee y verifica la caducidad del caché en caso de existir un archivo de caché

    Parametros:
        reiniciar: bool
            De valor predeterminado False.
            Para True, borra el caché actual y deja un archivo de formato predeterminado.
            Para False, lee el archivo y lo retorna en un diccionario

    Retorna:
        json_data: dict
            La lectura de un archivo json en variable dic
                Formato predeterminado (vacío): {"Bandera": "fecha:str", "Registros": {}}
                La clave "Registros" del diccionario es un diccionario con las IATAS como claves, y cada clave IATA es una lista formada por 24 horas obtenidas de la API. Cada lista de hora contiene una lista con los parámetros [clima:str, temperatura_min:int, temperatura_max:int, humedad: int, hora: int]
    '''
    if reiniciar:
        json_data=None
    else:
        try:
            with open(json_cache,'r') as file:
                json_data=json.load(file)
                print('Caché habil')
                VerificaCache(json_data)
        except(FileNotFoundError,json.JSONDecodeError) as e:
            print(f'Cache no encontrado..({e})')
            json_data=None
    if not json_data:
        json_data = {}
        json_data['Bandera'] = str(datetime.datetime.now())
        json_data['Registros'] = {}
        print('Se creó el cache')
        with open(json_cache,'w') as file:
            json.dump(json_data,file)
    return json_data

def VerificaCache(Bandera: dict):
    '''Verifica que el diccionario-caché tenga a lo más 3 horas de antiguedad, si excede el tiempo, actualiza caché

    Parametros:
        Bandera: dict
            Diccionario del tipo predeterminado de caché

    Retorno:
        No
    '''
    tiempo_cache=datetime.datetime.strptime(Bandera['Bandera'], "%Y-%m-%d %H:%M:%S.%f")
    tiempo_act=datetime.datetime.now()
    if (tiempo_act-tiempo_cache)>=datetime.timedelta(hours=3):
        ActualizarCache()
    else:
        print("Cache actualizado")

def Temporizador():
    '''Función que ejecuta el subproceso Analizador()
        Emplea las variables globales:
            t: Thread

            timer_runs: Event

    Parametros:
        No
    Reorno:
        No
    '''
    timer_runs.set()
    global t
    t = threading.Thread(target=Analizador, args=(timer_runs,))
    t.start()

def Analizador(timer_runs):
    '''Si se llama la función Temporizador() se verifica cada 3 horas el estado del caché.

        Mientras el programa funcione, se genera un subproceso que actualiza el caché cada 3 horas

    Parametros:
        timer_runs: Event
            Variable de tipo Global usada para generar el subproceso
    Retorno:
        No
    '''
    while timer_runs.is_set():
        print("Corre el tiempo")
        time.sleep(10800)
        Bandera=BanderaCache(reiniciar=False)
        VerificaCache(Bandera)

def RegIATA():
    '''Función que lee el dataset *.csv y regresa los codigos IATA con sus (Latitud, Longitud) correspoindientes

        Almacena los IATA code junto con sus latitudes y longitudes (sea de llegada o salida) sin repetir entradas del data set.
        Usa la variable Global dataset: str, que es el nombre del archivo csv

    Parametros:
        No
    Retorno:
        regs: dict
            Diccionario que contiene {'Registros': [[IATA0:str, Lat0:float, Lon0:float],[IATA1:str, Lat1:float, Lon1:float],...]} según lo obtenido en el dataset
    '''
    regs = {}
    regs['Registros'] = []
    try:
        with open(dataset, newline='') as file:
            data=csv.DictReader(file)
            for row in data:
                try:
                    if [row['origin'],float(row['origin_latitude']),float(row['origin_longitude'])] not in regs['Registros']:
                        regs['Registros'].append([row['origin'],float(row['origin_latitude']),float(row['origin_longitude'])])
                    if [row['destination'],float(row['destination_latitude']),float(row['destination_longitude'])] not in regs['Registros']:
                        regs['Registros'].append([row['destination'],float(row['destination_latitude']),float(row['destination_longitude'])])
                except ValueError:
                    print("Error en valores")
    except FileNotFoundError:
        print("No se encontró "+dataset)
    return regs

def Cachear():
    '''Si se llama la función ActualizarCache() se actualiza en segundo plano el contenido del archivo *.json

        Reinicia el caché actual y usa los registros no redundantes de RegIATA() para hacer un diccionario/archivo *.json. Se llama a la API para cada IATA segun sus coordenadas usando la libreria Weather.py. Además que se ejecuta en segundo plano mientras actualiza y evita más de 60 llamadas por minuto.

    Parametros:
        No

    Retorno:
        No
    '''
    regs=RegIATA()
    Bandera=BanderaCache(reiniciar=True)
    with open(json_cache,'r') as file:
        data=json.load(file)
    for i in range(0,len(regs['Registros'])):
        if (i+1)%60==0:
            print("Actualizando")
            time.sleep(60)
        data['Registros'][str(regs['Registros'][i][0])]=[]
        wter=Weather.WeatherApi.GetWeatherArray(regs['Registros'][i][1], regs['Registros'][i][2], apikey)
        if isinstance(wter,list)==False:
            print("Error al llamar a la API")
            break
        for k in range(24):
            try:
                data['Registros'][str(regs['Registros'][i][0])].append([wter[k].climate,wter[k].temp_min,wter[k].temp_max,wter[k].humidity,wter[k].hour])
            except AttributeError:
                data['Registros'][str(regs['Registros'][i][0])].append(['NULL','NULL','NULL','NULL','NULL'])
        with open(json_cache,'w') as file:
            json.dump(data,file)
    print("Cache actualizado:", Bandera['Bandera'])
    timer_runs.clear()
    Temporizador()
    return None

def ActualizarCache():
    '''Función que ejecuta el subproceso Cachear()
        Emplea las variables globales:
            act: Event

    Parametros:
        No
    Reorno:
        No
    '''
    global act
    act = threading.Thread(target=Cachear)
    act.start()

def IniciarCache():
    '''Función que inicializa el proceso de cacheado de inicio del programa
        Evita conflictos al abrir y cerrar el programa
        Emplea las variables globales:
            act: Event

    Parametros:
        No
    Reorno:
        No
    '''
    act.clear()
    Bandera=BanderaCache(reiniciar=False)
    if len(Bandera['Registros'])==0:
        ActualizarCache()
    else:
        Temporizador()
    return None


if __name__ == '__main__':
    '''IMPORTANTE: Todos los print() deben ser reemplazados por ventanas emergentes en la GUI NO PUEDEN HABER PRINTS
    '''
    #Esto es una prueba del funcionamiento SOLO LA PRIMERA LINEA ES ESCENCIAL
    IniciarCache()
    '''
    Bandera=BanderaCache(reiniciar=False)
    print(len(Bandera['Registros']))
    print(" ")
    print("Este mesaje no deberia esperar")
    time.sleep(2)
    print("Esto se corre de manera simultanea")
    print("UWU")
    '''
