## Proyecto 01 (Beta): Reporte del Clima para Aeropuertos

<br>

| Alumnos                     | No. de Cuenta |
| --------------------------- | ------------- |
| Edgar José Reyes Montelongo | 319023275     |  
| González Tamariz Santiago   | 423051416     |
| Paredes Zamudio Luis Daniel | 318159926     |
| Salgado Razo Jonatán        | 417091901     |

<br>

## Dependencias

Para instalar las dependecias se hace lo siguiente:

```
 pip install python-Levenshtein
 pip install flet
 pip install pyinstaller
```

## Ejecución del Programa

En la carpeta del proyecto se abre la terminal y se ejecutan los siguientes comandos:

```
flet run search.py
```

Para tener un ejecutable para su sistema operativo se hace:
```
flet pack search_window.py --name WeatherReporter --icon Assets/images/appIcon.icoc --add-data "Assets:Assets"
```

De igual manera se incluyen versiones para IOs/MacOS, Windows y Linux en la carpeta /dist

<br>

## Proceso de solución del problema

Se requiere crear una aplicación para consultar el clima en el lugar de salida/destino de un vuelo de avión.

Se cuenta con un dataset de los vuelos el cual contiene el no. de ticket, códigos iata de salida/destino y sus coordenadas (latitud, longitud).

Nos hacen falta los datos del clima, los cuales obtendremos mediante un webservice (openweather api).
<br>

Se eligió Python como lenguaje de programación debido a su facilidad de comprender y mantener, y su característica de ser multiparadigma. Se usará la API de OpenWeather debido a su gran cantidad de datos disponibles. 

Los datos se procesaran en formato csv/json para su fácil comprensión.
<br>

Se obtendrá la entrada del usuario la cuál podrá ser un no. de ticket, iata o nombre de ciudad - aeropuerto. Una vez obtenido eso se obtendrán las coordenadas del lugar correspondiente para poder obtener el clima del lugar.

Se implementará un sistema de cache de clima para agilizar el proceso y que el acceso de datos sea mucho
más rápido. El cache guardará los datos de clima de un lugar y a la hora de consultar el clima de un
lugar se checará primero el cache para evitar llamar a la api (que aparte de ser mucho más lento tiene un límite de llamadas por tiempo).

<br>

Una vez obtenido esto, se mostraran los datos de manera amigable, usando una interfaz gráfica
que cuenta con el estilo material ui de google al cuál muchos usuarios ya deberían de estar
familiarizados.

## Notas

<!-- flet pack search_window.py --name WeatherReporter --icon Assets/images/plane.png -->
<!-- search_window es temporalmente el main.py -->

> _Hecho en VsCode por que Vim da miedo..._
