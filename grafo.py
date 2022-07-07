from random import randint

class Grafo:
    """
    Reprensenta un grafo mediante un diccionario de diccionarios
    """

    def __init__(self, dirigido = False):
        self.grafo = {}
        self.dirigido = dirigido

    def __str__(self):
        print(self.grafo)
        return ""

    def agregar_vertice(self, v):
        if v not in self.grafo:
            self.grafo[v] = {}

    def borrar_vertice(self, v):
        self.grafo.pop(v)
        for w in self.grafo:
            if v in self.grafo[w]:
                self.grafo[w].pop(v)

    def agregar_arista(self, v, w, peso = 1):
        # El resultado sera v <---> w si el grafo es no dirigido
        # si es dirigido sera v ---> w
        self.grafo[v][w] = peso
        if not self.dirigido:
            self.grafo[w][v] = peso   

    def borrar_arista(self, v, w):
        self.grafo[v].pop(w)
        if not self.dirigido:  
            self.grafo[w].pop(v)
        
    def estan_unidos(self, v, w):
        if w in self.grafo[v] or v in self.grafo[w]:
            return True
        return False

    def peso_arista(self, v, w):
        peso = self.grafo[v][w]
        return peso

    def obtener_vertices(self):
        # Devuelve una lista con todos los vertices del grafo
        return list(self.grafo.keys())

    def vertice_aleatorio(self):
        vertices = list(self.grafo.keys())
        cantidad_de_vertices = len(vertices)
        if cantidad_de_vertices == 0:
            raise ValueError("Grafo vacio")
        indice_random = randint(0, cantidad_de_vertices- 1)
        return vertices[indice_random]

    def adyacentes(self, v):
        return list(self.grafo[v].keys())
