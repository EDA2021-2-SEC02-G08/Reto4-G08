﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del catalogo


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    analyzer = model.newAnalyzer()

    return analyzer


# Funciones para la carga de datos


def loadData(analyzer, airports_file, routes_file, cities_file):
    loadAirports(analyzer, airports_file)
    loadRoutes(analyzer, routes_file)
    loadCities(analyzer, cities_file)


def loadAirports(analyzer, airports_file):
    airports_file = cf.data_dir + airports_file
    input_file = csv.DictReader(open(airports_file, encoding="utf-8"),
                                delimiter=",")

    for airport in input_file:
        model.addAirport(analyzer, airport)


def loadRoutes(analyzer, routes_file):
    routes_file = cf.data_dir + routes_file
    input_file = csv.DictReader(open(routes_file, encoding="utf-8"),
                                delimiter=",")

    for route in input_file:
        model.addConnection(analyzer, route['Departure'],
                            route['Destination'], route['distance_km'])
    for route in input_file:
        model.undirectedGraph(analyzer, route['Departure'],
                              route['Destination'], route['distance_km'])


def loadCities(analyzer, cities_file):
    cities_file = cf.data_dir + cities_file
    input_file = csv.DictReader(open(cities_file, encoding="utf-8"),
                                delimiter=",")

    for city in input_file:
        model.addCity(analyzer, city)


# Funciones de consulta sobre el catálogo

def totalAirports(analyzer):
    return model.totalAirports(analyzer)


def totalRoutes(analyzer):
    return model.totalRoutes(analyzer)


def totalAirportsBackAndForth(analyzer):
    return model.totalAirportsBackAndForth(analyzer)


def totalBackAndForthRoutes(analyzer):
    return model.totalBackAndForthRoutes(analyzer)


def totalCities(analyzer):
    return model.totalCities(analyzer)


def getFirstLoadedAirport(analyzer):
    return model.getFirstLoadedAirport(analyzer)


def getLastLoadedCity(analyzer):
    return model.getLastLoadedCity(analyzer)
