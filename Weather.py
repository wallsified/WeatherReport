import requests
import json
import datetime
class Weather():
    '''
    Estructura que contiene la informacion del clima en la hora X

    Parameters:
       clima(str):Codigo del clima, equivale a las variables 'main' de  https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2.
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
    '''Clase de excepcion del clima, se debería lanzar cuando hay algo malo en la hora especificada'''
    pass

class WeatherApi:
    '''
    Clase con metodos estaticos para llamar a la API
    '''
    def __init__(self):
        pass
    @staticmethod
    def GetWeatherAtTime(lat,lon,hour):
        '''
        Funcion de llamada a la API, Obtiene los datos de las coordenadas dadas a la hora mas cercana posible a la que se ingresa.

        Parameters:
            lat(double):Latitud de la ubicacion
            lon(double):Longitud de la ubicacion
            hour(int):Hora dada
        Returns:
            climate(Weather): Un objeto Weather con la informacion necesaria
        
        '''
        if (int(datetime.datetime.now().strftime("%H"))< int(datetime.datetime.now().replace(hour=hour).strftime("%H"))):
        
            nearestHour=(datetime.datetime.now().replace(hour=hour,minute=0,second=0,microsecond=0))
            try:
                Data=WeatherApi.__CallApi(lat,lon)
            except:
                return "ErrorDeAPI"
            #Se obtiene la menor diferencia entre el tiempo solicitado y el estado del tiempo en la hora solicitada
            nearestForecast= min([abs(datetime.datetime.fromtimestamp(int(i["dt"]))-nearestHour) for i in Data.json()["list"]])
            #Se vuelve a sumar la hora redondeada mas cercana para obtener el timestamp de linux
            nearestForecast+=nearestHour
            for i in Data.json()["list"]:
                if (i["dt"]==datetime.datetime.timestamp(nearestForecast)):
                    resultado= Weather(i["weather"][0]["main"],i["main"]["temp_min"],i["main"]["temp_max"],i["main"]["humidity"],datetime.datetime.timestamp(nearestForecast))
                    return resultado
            
        else:
            raise WeatherTimeException()
    @staticmethod
    def __CallApi(lat,lon):
            try:
                rawWeatherData=requests.get("https://api.openweathermap.org/data/2.5/forecast?lat="+str(lat)+"&lon="+str(lon)+"&appid=9565343fefb88530783ccaba0f469e39&units=metric")
            except:
                raise requests.exceptions.RequestException
            if(rawWeatherData.json()["cod"]!='200'):
                print(rawWeatherData.json())
                raise requests.exceptions.RequestException
            return rawWeatherData


