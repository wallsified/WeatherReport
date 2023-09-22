import csv

class DatasetManager():

    def __init__(self):
        self.coords = dict()
        self.iatas = dict()
        self.read_tickets()

        self.names = dict()
        self.names_list = list()
        self.read_names()

        def valid_name(name):
            if self.coords.get(name):
                return True

            if self.coords.get(self.names.get(name)):
                return True

            return False

        self.valid_names = filter(valid_name, self.names_list)


    def read_tickets(self):
        file = open("dataset.csv")
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

            if self.coords.get(iata_orig) == None:
                lat_orig = float(line[3])
                long_orig = float(line[4])
                self.coords[iata_orig] = (lat_orig, long_orig)

            if self.coords.get(iata_dest) == None:
                lat_dest = float(line[5])
                long_dest = float(line[6])
                self.coords[iata_dest] = (lat_dest, long_dest)

        file.close()

    def read_names(self):
        file = open("name-iata.csv")
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
        return self.coords.get(iata)

    def get_iatas(self, ticket):
        return self.iatas.get(ticket)

    def is_valid_iata(self, iata):
        if self.coords.get(iata):
            return True
        else:
            return False

    def get_names_list(self):
        return self.names_list

    def get_iata(self, name):
        return self.names.get(name)

    def get_valid_names_list(self):
        return self.valid_names
