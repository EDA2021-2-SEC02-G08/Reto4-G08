"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Sorting import mergesort as mg
assert cf


# Construccion de modelos


def newAnalyzer():
    """
    Crea la estructura de datos para modelar el problema.
    """
    analyzer = {'directed': None,
                'no_directed': None,
                'cities': None,
                'IATAcodes': None,
                'GraphRoutes': 0,
                'DiGraphRoutes': 0}

    analyzer['directed'] = gr.newGraph(datastructure='ADJ_LIST',
                                       directed=True,
                                       size=10000,
                                       comparefunction=compareIATA)

    analyzer['no_directed'] = gr.newGraph(datastructure='ADJ_LIST',
                                          directed=False,
                                          size=10000,
                                          comparefunction=compareIATA)

    analyzer['cities'] = mp.newMap(numelements=41000,
                                   maptype='PROBING')

    analyzer['IATAcodes'] = mp.newMap(numelements=10000,
                                      maptype='PROBING')

    return analyzer


# Funciones para agregar informacion al catalogo


def addAirport(analyzer, airport):
    """
    Agrega el vértice que representa un aeropuerto al grafo y agrega
    al mapa de códigos IATA la información del aeropuerto.
    """
    vertex = airport['IATA']
    addAirportToGraph(analyzer['directed'], vertex)
    addAirportToGraph(analyzer['no_directed'], vertex)
    mp.put(analyzer['IATAcodes'], vertex, airport)


def addAirportToGraph(graph, airport):
    """
    Esta función adiciona un aeropuerto como un vértice del grafo
    """
    if not gr.containsVertex(graph, airport):
        gr.insertVertex(graph, airport)


def addConnectionToGraph(graph, origin, destination, weight):
    """
    Adiciona un arco entre dos aeropuertos a un grafo.
    """
    edge = gr.getEdge(graph, origin, destination)
    if edge is None:
        gr.addEdge(graph, origin, destination, weight)


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona las rutas a los grafos dirigido y no dirigido.
    """

    # Adiciona las rutas al grafo dirigido
    digraph = analyzer['directed']
    addConnectionToGraph(digraph, origin, destination, distance)
    analyzer['DiGraphRoutes'] += 1

    # Adiciona las rutas al grafo no dirigido
    go = gr.getEdge(digraph, origin, destination)
    come = gr.getEdge(digraph, destination, origin)
    if (go is not None) and (come is not None):
        graph = analyzer['no_directed']
        addConnectionToGraph(graph, origin, destination, distance)
        analyzer['GraphRoutes'] += 1


def addCity(analyzer, city):
    cities = analyzer['cities']
    cityName = city['city_ascii'].lower()
    mp.put(cities, cityName, city)


# Funciones de consulta


def getLoadedDiGraph(analyzer):
    airports = analyzer['IATAcodes']
    digraph = analyzer['directed']
    first = lt.firstElement(gr.vertices(digraph))
    last = lt.lastElement(gr.vertices(digraph))
    pair = mp.get(airports, first)
    pair1 = mp.get(airports, last)
    return me.getValue(pair), me.getValue(pair1)


def getLoadedGraph(analyzer):
    airports = analyzer['IATAcodes']
    graph = analyzer['no_directed']
    first = lt.firstElement(gr.vertices(graph))
    last = lt.lastElement(gr.vertices(graph))
    pair = mp.get(airports, first)
    pair1 = mp.get(airports, last)
    return me.getValue(pair), me.getValue(pair1)


def getClosedAirport(analyzer, airport):
    default = None
    if mp.contains(analyzer['IATAcodes'], airport):
        default = gr.adjacents(analyzer['directed'], airport)
        mg.sort(default, cmpSort)
    return default

# Funciones utilizadas para comparar elementos dentro de una lista


def compareIATA(code, airport):
    """
    Compara dos aeropuertos
    """
    if code == airport['key']:
        return 0
    else:
        return -1


def cmpSort(iata1, iata2):
    return iata1[0] < iata2[0]
