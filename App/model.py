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
# from DISClib.ADT import map as mp
# from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
assert cf


# Construccion de modelos


def newAnalyzer():
    """
    Insertar mensaje
    """
    analyzer = {'directed': None,
                'no_directed': None,
                'components': None,
                'paths': None}

    analyzer['directed'] = gr.newGraph(datastructure='ADJ_LIST',
                                       directed=True,
                                       size=14000,
                                       comparefunction=compareIATA)

    analyzer['no_directed'] = gr.newGraph(datastructure='ADJ_LIST',
                                          directed=False,
                                          size=14000,
                                          comparefunction=compareIATA)

    return analyzer


def graphDirected(analyzer, airport):
    origin = airport['IATA']
    addAirport(analyzer['directed'], origin)


def graphNoDirected(analyzer, airport):
    origin = airport['IATA']
    addAirport(analyzer['no_directed'], origin)


def addAirport(analyzer, origin):
    """
    Adiciona un aeropuerto, por su código IATA, como un vertice del grafo
    """
    if not gr.containsVertex(analyzer, origin):
        gr.insertVertex(analyzer, origin)

    return analyzer


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos aeropuertos
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)

    return analyzer

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista


def compareIATA():
    pass


# Funciones de ordenamiento
