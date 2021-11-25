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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
# from DISClib.ADT import map as mp
# from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
from DISClib.Utils import error as error
assert cf


# Construccion de modelos


def newAnalyzer():
    """
    Insertar mensaje
    """
    analyzer = {'directed_Graph': None,
                'undirected_Graph': None}

    analyzer['directed_Graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                             directed=True,
                                             size=14000,
                                             comparefunction=compareIATA)

    analyzer['undirected_Graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                               directed=False,
                                               size=14000,
                                               comparefunction=compareIATA)

    return analyzer


# Funciones para agregar informacion al catalogo


def directedGraph(analyzer, airport):
    origin = airport['IATA']
    addAirport(analyzer['directed_Graph'], origin)


def undirectedGraph(analyzer, airport):
    origin = airport['IATA']
    addAirport(analyzer['undirected_Graph'], origin)


def addAirport(analyzer, origin):
    """
    Esta función adiciona un aeropuerto como un vértice del grafo
    """
    try:
        if not gr.containsVertex(analyzer, origin):
            gr.insertVertex(analyzer, origin)
    except Exception as exp:
        error.reraise(exp, 'model:addAirport')


# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista


def compareIATA(code, airport):
    """
    Compara dos aeropuertos
    """
    code_IATA = airport['IATA']
    if code == code_IATA:
        return 0
    else:
        return -1


# Funciones de ordenamiento
