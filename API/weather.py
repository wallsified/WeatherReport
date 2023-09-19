""" Modulo de la API """
import datetime
import requests

class Weather():
    '''
    Estructura que contiene la informacion del clima en la hora X

    Parameters:
       clima(str):Codigo del clima, equivale a las variables 'main' de  
       https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2.
       temp_min(int):Temperatura minima arrojada por la API para las coordenadas dadas
       temp_max(int):Lo mismo, pero es la temperatura maxima
       humidity(int): % de humedad
       hour(int): el UNIX Timestamp de  la hora resultante.
    '''

    def __init__(self,climate,temp_min,temp_max,humidity,hour):
        self.climate=climate
        self.temp_min=temp_min
        self.temp_max=temp_max
        self.humidity=humidity
        self.hour=hour

class WeatherTimeException(Exception):
    '''
    Clase de excepcion del clima, se debería lanzar cuando hay 
    algo malo en la hora especificada
    '''
    #pass

class WeatherApi:
    '''
    Clase con metodos estaticos para llamar a la API
    '''
    def __init__(self):
        pass

    @staticmethod
    def get_weather_at_time(lat,lon,hour,key):
        '''
        Funcion de llamada a la API, Obtiene los datos de las coordenadas dadas a la 
        hora mas cercana posible a la que se ingresa.

        Parameters:
            lat(double):Latitud de la ubicacion
            lon(double):Longitud de la ubicacion
            hour(int):Hora dada
            key(str): la clave dada.
        
        Returns:
            climate(Weather): Un objeto Weather con la informacion necesaria
        
        '''

        if (int(datetime.datetime.now().strftime("%H"))<
            int(datetime.datetime.now().replace(hour=hour).strftime("%H"))):

            nearest_hour=(datetime.datetime.now().replace(
                hour=hour,minute=0,second=0,microsecond=0))

            try:
                Data=WeatherApi.__call_api(lat,lon,key)
            except:
                return "ErrorDeAPI"

            #Se obtiene la menor diferencia entre el tiempo solicitado y el estado
            # del tiempo en la hora solicitada
            nearest_forecast= min([abs(datetime.datetime.fromtimestamp(int(i["dt"]))
                                      -nearest_hour) for i in Data.json()["list"]])

            #Se vuelve a sumar la hora redondeada mas cercana para obtener el timestamp de linux
            #esto arregla un error aritmetico, no es la solucion mas bonita, pero funciona.
            nearest_forecast+=nearest_hour
            if hour%3==1:
                nearest_forecast+=datetime.timedelta(hours=1)

            for i in Data.json()["list"]:
                if i["dt"]==datetime.datetime.timestamp(nearest_forecast):
                    result= Weather(i["weather"][0]["main"],i["main"]["temp_min"],i["main"]
                                    ["temp_max"],i["main"]["humidity"],
                                    datetime.datetime.timestamp(nearest_forecast))
                    return result

        else:
            raise WeatherTimeException()

    @staticmethod
    def get_weather_array(lat,lon,key):
        '''
        Funcion de llamada a la API, Obtiene los datos de las 24 horas en forma de array, 
        donde el indice N equivale a la hora N, acotado en [0,23], las horas pasadas son None, 
        las horas actuales y futuras son objetos weather.

        Parameters:
            lat(double):Latitud de la ubicacion
            lon(double):Longitud de la ubicacion
            key(str): la clave dada.
 
        Returns:
            climate(Weather[]):Un array de Weather[], a excepcion de los None[] de las horas pasadas
        
        '''
        try:
            Data=WeatherApi.__call_api(lat,lon,key)
        except:
            return "ErrorDeAPI"
        result=[]

        for j in range(24):
            if int(datetime.datetime.now().strftime("%H"))< int(
                datetime.datetime.now().replace(hour=j).strftime("%H")):

                nearest_hour=(datetime.datetime.now().replace(hour=j,minute=0,second=0,
                                                              microsecond=0))
                nearest_forecast= min([abs(datetime.datetime.fromtimestamp(int(i["dt"]))
                                           -nearest_hour) for i in Data.json()["list"]])
                nearest_forecast+=nearest_hour

                #esto arregla un error aritmetico, no es la solucion mas bonita, pero funciona.
                if j%3==1:
                    nearest_forecast+=datetime.timedelta(hours=1)
                for i in Data.json()["list"]:
                    if i["dt"]==datetime.datetime.timestamp(nearest_forecast):
                        weather = Weather(i["weather"][0]["main"],i["main"]["temp_min"],
                                          i["main"]["temp_max"],i["main"]["humidity"],
                                          datetime.datetime.timestamp(nearest_forecast))
                        result.append(weather)
            else:
                result.append(None)
        return result

    @staticmethod
    def __call_api(lat,lon,key):
        try:
            raw_weather_data=requests.get(
                "https://api.openweathermap.org/data/2.5/forecast?lat="+str(lat)+"&lon="
                +str(lon)+"&appid="+key+"&units=metric")
        except:
            raise requests.exceptions.RequestException

        if raw_weather_data.json()["cod"]!='200':
            print(raw_weather_data.json())
            raise requests.exceptions.RequestException

        return raw_weather_data
