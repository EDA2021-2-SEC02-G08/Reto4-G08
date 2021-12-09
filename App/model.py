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
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Sorting import mergesort as mg
from math import radians, cos, sin, asin, sqrt
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
                'components': None,
                'connections': None,
                'hubs': None}

    analyzer['directed'] = gr.newGraph(datastructure='ADJ_LIST',
                                       directed=True,
                                       size=10000,
                                       comparefunction=compareIATA)

    analyzer['no_directed'] = gr.newGraph(datastructure='ADJ_LIST',
                                          directed=False,
                                          size=10000,
                                          comparefunction=compareIATA)

    analyzer['cities'] = lt.newList(datastructure='ARRAY_LIST')

    analyzer['IATAcodes'] = mp.newMap(numelements=10000,
                                      maptype='PROBING')

    analyzer['connections'] = mp.newMap(numelements=10000,
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
    data = {'connections': 0, 'inbound': 0, 'outbound': 0}
    mp.put(analyzer['IATAcodes'], vertex, airport)
    mp.put(analyzer['connections'], vertex, data)


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

    # Cuenta las conexiones de los aeropuertos
    connections = analyzer['connections']
    pair1 = mp.get(connections, origin)
    pair2 = mp.get(connections, destination)
    value1 = me.getValue(pair1)
    value2 = me.getValue(pair2)

    # Actualizar el mapa
    value1['connections'] += 1
    value2['connections'] += 1
    value1['outbound'] += 1
    value2['inbound'] += 1

    # Adiciona las rutas al grafo no dirigido
    go = gr.getEdge(digraph, origin, destination)
    come = gr.getEdge(digraph, destination, origin)
    if (go is not None) and (come is not None):
        graph = analyzer['no_directed']
        addConnectionToGraph(graph, origin, destination, distance)


def addCity(analyzer, city):
    lt.addLast(analyzer['cities'], city)


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
    pair = mp.get(airports, first)['value']
    pair1 = mp.get(airports, last)['value']
    return pair, pair1


def getLoadedGraph(analyzer):
    airports = analyzer['IATAcodes']
    graph = analyzer['no_directed']
    first = lt.firstElement(gr.vertices(graph))
    last = lt.lastElement(gr.vertices(graph))
    pair = mp.get(airports, first)['value']
    pair1 = mp.get(airports, last)['value']
    return pair, pair1


def getHubs(analyzer):
    """
    Retorna los 5 aeropuertos más interconectados y el total de aeropuertos
    en la red.
    """
    connections = analyzer['connections']
    hubs = lt.newList('ARRAY_LIST')
    for key in lt.iterator(mp.keySet(connections)):
        pair = mp.get(connections, key)
        value = me.getValue(pair)
        if lt.size(hubs) < 5:
            map = {'IATA': key, 'connections': value['connections'],
                   'outbound': value['outbound'], 'inbound': value['inbound']}
            lt.addLast(hubs, map)
            ins.sort(hubs, cmpConnections)
        else:
            last = lt.lastElement(hubs)
            pair = mp.get(connections, last['IATA'])
            N_last = me.getValue(pair)['connections']
            if value['connections'] >= N_last:
                lt.removeLast(hubs)
                map = {'IATA': key, 'connections': value['connections'],
                       'outbound': value['outbound'], 'inbound': value['inbound']}
                lt.addLast(hubs, map)
                ins.sort(hubs, cmpConnections)

    mostCncted = lt.newList('SINGLE_LINKED')
    for hub in lt.iterator(hubs):
        info = getAirportDataFromIATA(analyzer, hub['IATA'])
        info['connections'] = hub['connections']
        info['inbound'] = hub['inbound']
        info['outbound'] = hub['outbound']
        lt.addLast(mostCncted, info)

    return mostCncted


def getAirportDataFromIATA(analyzer, IATA):
    airports = analyzer['IATAcodes']
    isPresent = mp.contains(airports, IATA)
    if isPresent:
        pair = mp.get(airports, IATA)
        return me.getValue(pair)
    else:
        return None


def getClusters(analyzer):
    return analyzer['components']['components']


def hasPathBetween(analyzer, origin, destination):
    comps = analyzer['components']
    return scc.stronglyConnected(comps, origin, destination)


def getRouteWithMiles(analyzer, miles):
    graph = analyzer['no_directed']
    search = prim.PrimMST(graph)
    distKM = miles*0.621
    distanciaMax = prim.weightMST(graph, search)
    return distanciaMax, distKM, search['mst']

    return search


def getNearestAirport(analyzer, salida, llegada):
    airports = mp.valueSet(analyzer['IATAcodes'])
    list1 = lt.newList(datastructure='ARRAY_LIST')
    list2 = lt.newList(datastructure='ARRAY_LIST')
    for element in lt.iterator(airports):
        lat2 = float(element['Latitude'])
        lng2 = float(element['Longitude'])
        distance1 = haversine(float(salida['lng']), float(salida['lat']), lng2, lat2)
        distance2 = haversine(float(llegada['lng']), float(llegada['lat']), lng2, lat2)
        lt.addLast(list1, [element, distance1])
        mg.sort(list1, cmpdistance)
        lt.addLast(list2, [element, distance2])
        mg.sort(list2, cmpdistance)

    return lt.firstElement(list1), lt.firstElement(list2)


def requer3(analyzer, airport1, airport2):
    estructura = djk.Dijkstra(analyzer['directed'], airport1[0]['IATA'])
    distance = djk.distTo(estructura, airport2[0]['IATA'])
    camino = djk.pathTo(estructura, airport2[0]['IATA'])

    return distance, camino


def getClosedAirport(analyzer, airport):
    default = None
    if mp.contains(analyzer['IATAcodes'], airport):
        default = gr.adjacents(analyzer['directed'], airport)
        mg.sort(default, cmpSort)
    return default


# Funciones auxiliares
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles.

    return c * r


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


def cmpConnections(airport1, airport2):
    n1 = airport1['connections']
    n2 = airport2['connections']
    if n1 > n2:
        return True
    else:
        return False


def cmpdistance(distance1, distance2):
    return distance1[1] < distance2[1]

# Funciones de ordenamiento
