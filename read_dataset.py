import csv

def read_tickets():
    coords = dict()
    tickets = dict()

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
        tickets[ticket_number] = (iata_orig, iata_dest)

        if coords.get(iata_orig) == None:
            lat_orig = float(line[3])
            long_orig = float(line[4])
            coords[iata_orig] = (lat_orig, long_orig)

        if coords.get(iata_dest) == None:
            lat_dest = float(line[5])
            long_dest = float(line[6])
            coords[iata_dest] = (lat_dest, long_dest)

    return coords, tickets

def read_names():
    names = dict()
    names_list = list()

    file = open("name-iata.csv")
    reader = csv.reader(file)

    i = 0
    for line in reader:
        if i == 0:
            i += 1
            continue

        names[line[0]] = line[2]
        names[line[1]] = line[2]

        names_list.append(line[0])
        names_list.append(line[1])

    return names, names_list
