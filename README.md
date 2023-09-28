# Proyecto 01 (Beta): Reporte del Clima para Aeropuertos

<br>

| Alumnos                     | No. de Cuenta |
| --------------------------- | ------------- |  
| González Tamariz Santiago   | 423051416     |
| Paredes Zamudio Luis Daniel | 318159926     |
| Reyes Montelongo Edgar José | 319023275     | 
| Salgado Razo Jonatán        | 417091901     |


## Dependencias

Para instalar las dependecias se hace lo siguiente:

```
 pip install python-Levenshtein flet pyinstaller requests
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

De igual manera se incluyen versiones para IOs/MacOS, Windows y Linux en la carpeta [/dist](dist/)

## Proceso de solución del problema

### Análisis del Problema

Se requiere crear una aplicación para consultar el clima en el lugar de salida/destino de un vuelo de avión. 

El usuario debe poder realizar búsquedas dentro de la misma mediante número de ticket, ciudad o código IATA, por lo que se requiere una interfaz gráfica para su funcionamiento. 

Debido a la diversidad de usuarios, se busca que la aplicación este disponible en diferentes plataformas. 

### Datos Disponibles 

Se cuenta con un dataset de los vuelos el cual contiene el no. de ticket, códigos IATA de salida/destino y sus coordenadas (latitud, longitud).

Nos hacen falta los datos del clima, los cuales obtendremos mediante consultas un WebService.

### Herramientas Elegidas

Se eligió Python como lenguaje de programación para resolver el problema debido a su facilidad de comprender y mantener, su característica de ser multiparadigma y las librerías tanto gráficas como de funcionalidad que se pueden ocupar para resolver de forma más fácil la enconmienda.

Usaremos Flet como la librería gráfica principal, la cual, al estar basada en Flutter y los patrones de diseño Material Design de Google, nos permitirán crear una interfaz moderna a la vista y con estilos que la mayoría de usuarios ya están acostumbrados.

Se usará la API de OpenWeather para la obtención de los datos del clima, esto debido tanto a la gran cantidad de datos disponibles que se pueden obtener de la misma y a la posibilidad de consultar de la misma de manera gratuita hasta cierto extento. 

### Modelo de Datos

Los datos recibidos de la API se procesaran en formato JSON para su fácil comprensión y posterior manipulación.

Se implementará un sistema de cache de clima para agilizar el proceso y que el acceso de datos sea mucho
más rápido. El cache guardará los datos de clima de un lugar y a la hora de consultar el clima de un
lugar se checará primero el cache para evitar llamar a la api (que aparte de ser mucho más lento tiene un límite de llamadas por tiempo).

Se obtendrá la entrada del usuario la cuál podrá ser un no. de ticket, IATA o nombre de ciudad - aeropuerto. Una vez obtenida la información se obtendrán las coordenadas del lugar correspondiente para poder obtener el clima del lugar.

### Pseudocódigo

Este puede verse con más detalle en el [correspondiente](/Reports/Pseudocode.pdf).

## Presentación del Proyecto

De igual manera puede verse con más detalle en su archivo [correspondiente](/Reports/Weather%20Reporter%20Presentation%20(Beta).pdf).