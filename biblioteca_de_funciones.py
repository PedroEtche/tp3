# Imports

from collections import deque
from grafo import Grafo
import heapq

# Recorridos

def bfs_completo(grafo):
    visitados = set()
    padres = {}
    orden = {}
    for v in grafo.obtener_vertices():
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

# Camino minimos

def camino_minimo_dijkstra(grafo, origen):
    dist = {}
    padre = {}
    for v in grafo:
        dist[v] = float("inf")
    dist[origen] = 0
    padre[origen] = None
    h = [] 
    heapq.heappush(h, (0, origen))
    while len(h) != 0:
        _, v = heapq.heappop(h)
        for w in grafo.adyacentes(v):
            distancia_por_aca = dist[v] + grafo.peso_arista(v, w)
            if distancia_por_aca < dist[w]:
                dist[w] = dist[v] + grafo.peso_arista(v, w)
                padre[w] = v
                heapq.heappush(h, (dist[w], w))
    return padre, dist

# Arbol de tendido minimo

def mst_prim(grafo):
    v = grafo.vertice_aleatorio()
    visitados = set()
    visitados.agregar(v)
    h = []
    for w in grafo.adyacentes(v):
        heapq.heappush(h, ((v, w) , grafo.peso_arista(v, w)))
    arbol = Grafo()
    for vertice in grafo:
        arbol.agregar_vertice(vertice)
    while len(h) != 0:
        (v, w), peso = heapq.heappop(h )
        if w in visitados:
            continue
        arbol.agregar_arista(v, w, peso)
        visitados.agregar(w)
        # for x in grafo.adyacentes(w):
        #     if x not in visitados: heapq.heappush(h, ((w, x), grafo.peso(w, u)))
    return arbol

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
    return _ciclio_hamiltoneano(grafo, origen)

# Page rank

def page_rank(grafo, iteraciones = 100, d = 0.8):
    lista_vertices = grafo.obtener_vertices()
    cantidad_de_vertices = len(lista_vertices)
    page_rank_vertices = {}
    for vertice in lista_vertices:
        page_rank_vertices[vertice] = (1 - d) / cantidad_de_vertices
    
    for _ in range(iteraciones):
        for vertice in lista_vertices:
            nuevo_rank = 0
            for w in grafo.adyacentes(vertice):
                nuevo_rank += page_rank_vertices[w] / len(grafo.adyacentes(w))
            page_rank_vertices[vertice] = d * nuevo_rank
    return page_rank_vertices
