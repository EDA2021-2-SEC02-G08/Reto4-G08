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
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT.graph import gr
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
                'components': None}

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


def addConnectionToGraph(graph, origin, destination, distance):
    """
    Adiciona un arco entre dos aeropuertos a un grafo.
    """
    edge = gr.getEdge(graph, origin, destination)
    if edge is None:
        gr.addEdge(graph, origin, destination, distance)


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona las rutas a los grafos dirigido y no dirigido.
    """
    digraph = analyzer['directed']
    addConnectionToGraph(digraph, origin, destination, distance)
    come = gr.getEdge(digraph, origin, destination)
    go = gr.getEdge(digraph, destination, origin)
    comeNgo = (come is not None) and (go is not None)
    if comeNgo:
        graph = analyzer['no_directed']
        addConnectionToGraph(graph, origin, destination, distance)


def addCity(analyzer, city):
    cities = analyzer['cities']
    cityName = city['city_ascii'].lower()
    mp.put(cities, cityName, city)


def getSCCs(analyzer):
    """
    Guarda el número de clusters en la red de aeropuertos.
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['directed'])


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


def getHubs(analyzer):
    """
    Retorna los 5 aeropuertos más interconectados y el total de aeropuertos 
    en la red.
    """
    digraph = analyzer['directed']
    IATAs = analyzer['IATAcodes']
    airports = gr.vertices(digraph)
    mostCnctd = lt.subList(mp.valueSet(IATAs), 1, 5)
    mostCnctd = ins.sort(mostCnctd, cmpConnections)
    for airport in lt.iterator(airports):
        last = lt.lastElement(mostCnctd)
        Nlast = getAirportConnections(analyzer, last['IATA'])
        N_comp = getAirportConnections(analyzer, airport)
        if N_comp > Nlast:
            pair = mp.get(IATAs, airport)
            info = me.getValue(pair)
            lt.removeLast(mostCnctd)
            lt.addLast(mostCnctd, info)
            mostCnctd = ins.sort(mostCnctd, cmpConnections)

    return mostCnctd


def getClusters(analyzer):
    return analyzer['components']['components']


def hasPathBetween(analyzer, origin, destination):
    comps = analyzer['components']
    return scc.stronglyConnected(comps, origin, destination)


def getRouteWithMiles(analyzer, miles):
    digraph = analyzer['dirigido']
    search = prim.PrimMST(digraph)



def getClosedAirport(analyzer, airport):
    default = None
    if mp.contains(analyzer['IATAcodes'], airport):
        default = gr.adjacents(analyzer['directed'], airport)
    return default


# Funciones auxiliares

def getAirportConnections(analyzer, airport):
    digraph = analyzer['dirigido']
    N = gr.indegree(digraph, airport) + gr.outdegree(digraph, airport)
    return N

# Funciones utilizadas para comparar elementos dentro de una lista


def compareIATA(code, airport):
    """
    Compara dos aeropuertos
    """
    if code == airport['key']:
        return 0
    else:
        return -1


def cmpConnections(analyzer, airport1, airport2):
    digraph = analyzer['dirigido']
    adj1 = getAirportConnections(analyzer, airport1['IATA'])
    adj2 = getAirportConnections(analyzer, airport2['IATA'])
    if adj1 > adj2:
        return True
    else:
        return False

# Funciones de ordenamiento
