"""
Archivo de Gestión del DataSet

Author @Santi24Yt
Version 1.0

"""

import csv
from Cache import cache

class DatasetManager():

    """
    Clase de Manejo del Dataset
    
    Métodos
    ------
        *__init__ : Iniciación de la clase.
        * read_tickets : Lectura de Tickets del dataset
        * read_names: Lectura la base de Datos de IATA Codes
        * get_coords: Obtención de Coordenadas
        * get_iatas: Obtención de códigos IATA
        * is_valid_iata: Verificación de Códigos IATA 
        * get_names_lista: Obtención de Lista de Nombres
        * get_iata: Obtención de Código IATA
        * get_valid_names_list: Obtención de Lista de Códigos IATA válidos.
    """

    def __init__(self):
        self.coords = {}
        self.iatas = {}
        self.read_tickets()

        self.names = {}
        self.names_list = []
        self.read_names()

        def valid_name(name):
            if self.coords.get(name):
                return True

            if self.coords.get(self.names.get(name)):
                return True

            return False

        self.valid_names = filter(valid_name, self.names_list)


    def read_tickets(self):
        """
        Lectura de Tickets del dataset
        """
        file = open(file= cache.DATA_SET, encoding= "utf-8")
        reader = csv.reader(file)

        i = 0
        for line in reader:
            if i == 0:
                i += 1
                continue

            ticket_number = line[0]
            iata_orig = line[1]
            iata_dest = line[2]
            self.iatas[ticket_number] = (iata_orig, iata_dest)

            if self.coords.get(iata_orig) is None:
                lat_orig = float(line[3])
                long_orig = float(line[4])
                self.coords[iata_orig] = (lat_orig, long_orig)

            if self.coords.get(iata_dest) is None:
                lat_dest = float(line[5])
                long_dest = float(line[6])
                self.coords[iata_dest] = (lat_dest, long_dest)

        file.close()

    def read_names(self):
        """
        Lectura la base de Datos de IATA Codes
        """
        file = open(file = "Resources/name-iata.csv", encoding= "utf-8")
        reader = csv.reader(file)

        i = 0
        for line in reader:
            if i == 0:
                i += 1
                continue

            self.names[line[0]] = line[2]
            self.names[line[1]] = line[2]
            self.names[line[2]] = line[2]

            self.names_list.append(line[0])
            self.names_list.append(line[1])
            self.names_list.append(line[2])

        file.close()

    def get_coords(self, iata):
        """
        Obtención de Coordenadas por Código IATa
        
        Regresa
        -------
        Coordenadas
        """
        return self.coords.get(iata)

    def get_iatas(self, ticket):
        """
        Obtención de códigos IATA por Ticket
        
        Regresa
        -------
        Codigo IATA de un Ticket

        """
        return self.iatas.get(ticket)

    def is_valid_iata(self, iata):
        """
        Verificación de Códigos IATA 
        
        Regresa
        ------
        True: El IATA es válido
        False: Caso Contrario
        """
        return bool(self.coords.get(iata))

    def get_names_list(self):
        """
        Obtención de Lista de Nombres
        
        Regresa
        -------
        Lista de Nombres
        """
        return self.names_list

    def get_iata(self, name):
        """
        Obtención de Código IATA
        
        Regresa
        -------
        Código IATA
        """
        return self.names.get(name)

    def get_valid_names_list(self):
        """
        Obtención de Lista de Códigos IATA válidos.
        
        Regreso
        ------
        Lista de Códigos IATA válidos.
        """
        return self.valid_names
