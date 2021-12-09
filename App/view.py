"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("\nBienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información en el catálogo")
    print("3- Obtener aeropuertos de interconexión")
    print("4- Obtener clústeres y conexión entre aeropuertos")
    print("5- Obtener ruta de mínima distancia entre origen y destino")
    print("6- Obtener viaje con millas de viajero")
    print("7- Obtener afectación por aeropuerto cerrado")
    print("0- Salir")


catalog = None


airports_file = 'airports-utf8-small.csv'
routes_file = 'routes-utf8-small.csv'
cities_file = 'worldcities-utf8.csv'


"""
Funciones de impresión
"""


def printAirportData(airport):
    print('Nombre:{}, Ciudad: {}, País: {}, Latitud: {}, Longitud: {}'.format(
          airport['Name'], airport['City'], airport['Country'],
          airport['Latitude'], airport['Longitude']))


def printAirportDataWithConnections(airport):
    print('Nombre: ' + airport['Name'] + ', Ciudad: ' + airport['City'] + 
          ', País: ' + airport['Country'] + ', Latitud: ' + airport['Latitude']
          + ', Longitud: ' + airport['Longitude'] + ', Conexiones: ' +
          str(airport['connections']) + ', Llegadas: ' + 
          str(airport['inbound']) + ', Salidas: ' + str(airport['outbound'])
         )


def printAirportDataWithIATA(airport):
    print('IATA: ' + airport['IATA'] + ', Nombre: ' + airport['Name']
          + ', Ciudad: ' + airport['City'] + 'País: ' + airport['Country']
          + ', Latitud: ' + airport['Latitude'] + ', Longitud: '
          + airport['Longitude']
         )


def printCityData(city):
    print('Name: {}, Country: {}, Latitude: {}, Longitude: {}'.format(
          city['city_ascii'], city['country'], city['lat'], city['lng']))


def printDiGraph(analyzer):
    nodes = gr.numVertices(analyzer['directed'])
    edges = gr.numEdges(analyzer['directed'])
    first, last = controller.getLoadedDiGraph(analyzer)
    print('\n=== Airports-Routes DiGraph ===')
    print('Nodes: ' + str(nodes))
    print('Edges: ' + str(edges))
    print('First and last airport loaded in the DiGraph:')
    printAirportData(first)
    printAirportData(last)


def printGraph(analyzer):
    nodes = gr.numVertices(analyzer['no_directed'])
    edges = gr.numEdges(analyzer['no_directed'])
    first, last = controller.getLoadedGraph(analyzer)
    print('\n=== Airports-Routes Graph ===')
    print('Nodes: ' + str(nodes))
    print('Edges: ' + str(edges))
    print('First and last airport loaded in the Graph:')
    printAirportData(first)
    printAirportData(last)


def printCity(analyzer):
    cities = analyzer['cities']
    total = lt.size(analyzer['cities'])
    print('\n=== City Network ===')
    print('The number of cities are: ' + str(total))
    print('First and last city loaded in data structure:')
    printCityData(lt.firstElement(cities))
    printCityData(lt.lastElement(cities))


def ciudadesRepetidas(analyzer, salida, llegada):
    list1 = lt.newList(datastructure='ARRAY_LIST')
    list2 = lt.newList(datastructure='ARRAY_LIST')
    for city in lt.iterator(analyzer['cities']):
        if city['city'].lower() == salida:
            lt.addLast(list1, city)
        if city['city'].lower() == llegada:
            lt.addLast(list2, city)
    if lt.size(list1) > 1:
        count = 1
        for element in lt.iterator(list1):
            print(str(count))
            printCityData(element)
            count += 1
        num = int(input('\nIngrese la ciudad: \n'))
        salida = lt.getElement(list1, num)
    elif lt.size(list1) == 1:
        salida = lt.getElement(list1, 1)
    else:
        salida = None
    if lt.size(list2) > 1:
        count = 1
        for element in lt.iterator(list2):
            print(str(count))
            printCityData(element)
            count += 1
        num = int(input('\nIngrese la ciudad: \n'))
        llegada = lt.getElement(list2, num)
    elif lt.size(list2) == 1:
        llegada = lt.getElement(list2, 1)
    else:
        llegada = None
    return salida, llegada


def printClosed(analyzer, adjacents, airport):
    total = lt.size(adjacents)
    print('There are ' + str(total) + ' airports affected by ' + str(airport))
    print('The first and last 3 airports affected are:')
    if total >= 6:
        first = lt.subList(adjacents, 1, 3)
        last = lt.subList(adjacents, (total-2), 3)
        for element in lt.iterator(first):
            info = mp.get(analyzer['IATAcodes'], element)['value']
            printAirportData(info)
        for element in lt.iterator(last):
            info = mp.get(analyzer['IATAcodes'], element)['value']
            printAirportData(info)
    else:
        for element in lt.iterator(adjacents):
            info = mp.get(analyzer['IATAcodes'], element)['value']
            printAirportData(info)


"""
Menu principal
"""


while True:
    printMenu()
    inputs = int(input('Seleccione una opción para continuar\n'))
    if inputs == 1:
        print("\nInicializando....")
        analyzer = controller.init()

    elif inputs == 2:
        controller.loadData(analyzer, airports_file, routes_file, cities_file)
        printDiGraph(analyzer)
        printGraph(analyzer)
        printCity(analyzer)

    elif inputs == 3:
        hubs = controller.getHubs(analyzer)
        print('Los 5 aeropuertos más conectados son:')
        for hub in lt.iterator(hubs):
            printAirportDataWithConnections(hub)
        

    elif inputs == 4:
        nClusters = controller.getClusters(analyzer)
        print('Hay ' + str(nClusters) + ' en la red.')
        departure = str(input('Ingrese código IATA del aeropuerto de partida: ')).upper()
        printAirportDataWithIATA(controller.getAirportDataFromIATA(analyzer, departure))
        arrival = str(input('Ingrese código IATA del aeropuerto de llegada: ')).upper()
        printAirportDataWithIATA(controller.getAirportDataFromIATA(analyzer, arrival))
        same = controller.hasPathBetween(analyzer, departure, arrival)
        print('¿Estos aeropuertos pertenecen al mismo clúster? ' + str(same))


    elif inputs == 5:
        Departure = str(input('Ingrese la ciudad de partida: ')).lower()
        Arrival = str(input('Ingrese la ciudad de llegada: ')).lower()
        salida, llegada = ciudadesRepetidas(analyzer, Departure, Arrival)
        aero1, aero2 = controller.getNearestAirport(analyzer, salida, llegada)
        distance, path = controller.requer3(analyzer, aero1, aero2)
        print('Total distance: ' + str(distance) + ' km')
        print('Trip path:')
        for element in lt.iterator(path):
            print(element)

    elif inputs == 6:
        miles = int(input('Available travel miles: '))
        controller.reque4(analyzer, miles)

    elif inputs == 7:
        airport = str(input('Closing the airport with IATA code: ')).upper()
        adjacents = controller.getClosedAirport(analyzer, airport)
        printClosed(analyzer, adjacents, airport)

    else:
        sys.exit(0)
sys.exit(0)
