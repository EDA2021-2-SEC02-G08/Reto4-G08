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
Menu principal
"""
while True:
    printMenu()
    inputs = int(input('Seleccione una opción para continuar\n'))
    if inputs == 1:
        print("\nInicializando....")
        analyzer = controller.init()
        controller.loadAirports(analyzer, airports_file)

    elif inputs == 2:
        pass

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
