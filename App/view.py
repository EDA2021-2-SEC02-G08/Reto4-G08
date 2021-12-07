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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información en el catálogo")
    print("3- Obtener aeropuertos de interconexión")
    print("4- Obtener clústeres y conexión entre aeropuertos")
    print("5- Obtener ruta de mínima distancia entre origen y destino")
    print("6- Obtener viaje con millas de viajero")
    print("7- Obtener afectación por aeropuerto cerrado")
    print("0- Salir")


catalog = None


airports_file = 'airports_full.csv'
routes_file = 'routes_full.csv'
cities_file = 'worldcities.csv'


"""
Funciones de impresión
"""


def printAirportData(airport):
    print('Nombre: {} Ciudad: {} País: {} Latitud: {} Longitud: {}'.format(
        airport['Name'], airport['City'], airport['Country'],
        airport['Latitude'], airport['Longitude']))


def printCityData(city):
    print('Nombre: {} Población: {} Latitud: {} Longitud: {}'.format(
        city['city_ascii'], city['population'], city['lat'],
        city['lng']))


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
        NAirportsD = controller.totalAirports(analyzer)
        NAirportsN = controller.totalAirportsBackAndForth(analyzer)
        NRoutesD = controller.totalRoutes(analyzer)
        NRoutesN = controller.totalBackAndForthRoutes(analyzer)
        NCities = controller.totalCities(analyzer)
        firstD, firstND = controller.getFirstLoadedAirport(analyzer)
        last = controller.getLastLoadedCity(analyzer)
        print('Total de aeropuertos: ' + str(NAirportsD))
        print('Total de aeropuertos ida y vuelta: ' + str(NAirportsN))
        print('Total de rutas: ' + str(NRoutesD))
        print('Total de rutas ida y vuelta: ' + str(NRoutesN))
        print('Total de ciudades: ' + str(NCities))
        print('Primer aeropuerto cargado en el grafo dirigido:')
        printAirportData(firstD)
        print('Primer aeropuerto cargado en el grafo no dirigido:')
        printAirportData(firstND)
        print('Última ciudad cargada:')
        printCityData(last)

    elif inputs == 3:
        pass

    elif inputs == 4:
        pass

    elif inputs == 5:
        pass

    elif inputs == 6:
        pass

    elif inputs == 7:
        pass

    else:
        sys.exit(0)
sys.exit(0)
