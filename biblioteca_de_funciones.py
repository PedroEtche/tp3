# Imports

from collections import deque
from random import randint
import grafo

# Recorridos

def bfs_completo(grafo):
    visitados = set()
    padres = {}
    orden = {}
    for v in grafo.obtener_vertices():
        if v not in visitados:
            _bfs(grafo, v, visitados, padres, orden)
    return padres, orden

def _bfs(grafo, origen, visitados, padres, orden):
    padres[origen] = None
    orden[origen] = 0
    visitados.add(origen)
    cola = deque()
    cola.append(origen)
    while len(cola) != 0:
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                padres[w] = v
                orden[w] = orden[v] + 1
                visitados.add(w)
                cola.append(w)
    return padres, orden

def bfs(grafo, origen):
    visitados = set()
    padres = {}
    orden = {}
    padres[origen] = None
    orden[origen] = 0
    visitados.add(origen)
    cola = deque()
    cola.append(origen)
    while len(cola) != 0:
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                padres[w] = v
                orden[w] = orden[v] + 1
                visitados.add(w)
                cola.append(w)
    return padres, orden

def dfs_completo(grafo):
    visitados = set()
    padres = {}
    orden = {}
    for v in grafo.obtener_vertices():
        visitados.add(v)
        padres[v] = None
        orden[v] = 0
        _dfs(grafo, v, visitados, padres, orden)
    return padres, orden

def _dfs(grafo, origen, visitados, padres, orden):
    for w in grafo.adyacentes(origen):
        if w not in visitados:
            visitados.add(w)
            padres[w] = origen
            orden[w] = orden[origen] + 1
            _dfs(grafo, w, visitados, padres, orden)

def dfs(grafo, origen):
    visitados = set()
    padres = {}
    orden = {}
    visitados.add(origen)
    padres[origen] = None
    orden[origen] = 0
    _dfs(grafo, origen, visitados, padres, orden)
    return padres, orden

# Backtracking

def _ciclio_hamiltoneano(grafo, camino):
    inicial = camino[0]
    ultimo = camino[len(camino) - 1]
    resultados = []
    for adyacente in grafo.adyacentes(ultimo):
        copia = camino[:]
        copia.append(adyacente)
        if (adyacente == inicial and len(camino) == len(grafo.obtener_vertices())):
            # Encontre un ciclo hamiltoneano
            resultados.append(copia)
        if (adyacente in camino):
            continue
        resultados = resultados + _ciclio_hamiltoneano(grafo, copia)
    return resultados

def ciclo_hamiltoneano(grafo, origen):
    return _ciclio_hamiltoneano(grafo, [origen])

# Page rank

def page_rank(grafo, iteraciones = 50, d = 0.85):
    lista_vertices = grafo.obtener_vertices()
    cantidad_de_vertices = len(lista_vertices)
    page_rank_vertices = {}
    regulador = (1 - d) / cantidad_de_vertices
    for vertice in lista_vertices:
        page_rank_vertices[vertice] = regulador
    i = 0
    convergio = False
    while not convergio and i != iteraciones:
        cantidad_de_convergidos = 0
        for vertice in lista_vertices:
            nuevo_rank = 0
            for w in grafo.adyacentes(vertice):
                nuevo_rank += page_rank_vertices[w] / len(grafo.adyacentes(w))
            nuevo_rank = (nuevo_rank * d)
            nuevo_rank += regulador

            x = page_rank_vertices.get(vertice)
            if (abs(x - nuevo_rank) <= (regulador)):
                cantidad_de_convergidos += 1
            page_rank_vertices[vertice] = nuevo_rank
            if cantidad_de_convergidos == cantidad_de_vertices:
                convergio = True
        i += 1
    return page_rank_vertices

def page_rank_personalizado(grafo, origen, largo_recorrido, iteraciones = 1000):
    pg_personalizado = {}
    adyacentes_origen = grafo.adyacentes(origen)
    len_adyacentes= len(adyacentes_origen)

    for _ in range(iteraciones):
        proximo_vertice = randint(0, len_adyacentes-1)
        vertice_actual = adyacentes_origen[proximo_vertice]
        valor_a_transmitir = 1 / len_adyacentes

        for _ in range(largo_recorrido):
            if vertice_actual not in pg_personalizado:
                pg_personalizado[vertice_actual] = valor_a_transmitir

            else:
                pg_personalizado[vertice_actual] += valor_a_transmitir

            valor_a_transmitir = valor_a_transmitir / len(grafo.adyacentes(vertice_actual))

            posibles_movimientos = grafo.adyacentes(vertice_actual)
            if(len(posibles_movimientos) == 0):
                #En el caso de un grafo dirigido llegue a un vertice que tiene grado de salida 0
                break
            proximo_vertice = randint(0, len(posibles_movimientos)-1)
            vertice_actual = posibles_movimientos[proximo_vertice]

        # La ultima iteracion no termino de calcular el page personalizado del ultimo vertice y ademas de tener en cuenta que
        # no acabe en un vertice sin adyacentes
        if(len(posibles_movimientos) != 0):
            if vertice_actual not in pg_personalizado:
                pg_personalizado[vertice_actual] = valor_a_transmitir
            else:
                pg_personalizado[vertice_actual] += valor_a_transmitir

    return pg_personalizado
