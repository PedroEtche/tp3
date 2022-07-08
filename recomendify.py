# Imports

from http.client import FORBIDDEN
from grafo import Grafo
import biblioteca_de_funciones
from sys import argv
import random

# Constantes

CAMINO = "camino"
MAS_IMPORTANTES = "mas_importantes"
RECOMENDACION = "recomendacion"
CICLO = "ciclo"
RANGO = "rango"
MAX = "-1"
FIN_ARCHIVO = [MAX,"","","","","",""]
CANCION = 0
ARTISTA = 1

# Lectura de archivo

def leer_linea(archivo):
    linea = archivo.readline()
    if linea:
        devolver = linea.rstrip("\n").split("\t")
    else:
        devolver = FIN_ARCHIVO
    return devolver

# Modelacion

def estructuras_basicas(archivo):
    """
    Me crea un grafo bi partito. Los vertices son usuarios y canciones.
    Las aristas que conectan un usuario con una cancion significan ese usuario tiene la cancion en
    su playlist. Tambien crea un diccionario de diccionario de diccionario en el que cada clave 
    (usuario) tiene como dato un diccionario, que a su vez, tiene como clave un diccionario 
    (nombre_de_la_playlist) y como dato la informacion de la cancion
    Crea un set con el nombre de todos los usuarios
    Crea un set con el nombre y artista/grupo que compuso cada cancion
    """
    set_de_usuarios = set()
    set_de_canciones = set()
    usuarios_canciones = Grafo()
    id, usuario, cancion, artista, playlist_id, playlist, generos = leer_linea(archivo)
    while id != MAX:
        usuarios_canciones.agregar_vertice(usuario)
        usuarios_canciones.agregar_vertice((cancion, artista))
        usuarios_canciones.agregar_arista(usuario, (cancion, artista))

        if usuario not in set_de_usuarios:
            set_de_usuarios.add(usuario)

        if cancion not in set_de_canciones:
            set_de_canciones.add((cancion, artista))

        id, usuario, cancion, artista, playlist_id, playlist, generos = leer_linea(archivo)

    #print(usuarios_canciones.adyacentes("sitevagalume"))
    #print(usuarios_canciones.adyacentes("fernandagi17"))
    #print(usuarios_canciones)
    return usuarios_canciones, set_de_canciones


def crear_diccionario_de_canciones_y_usuarios_que_la_escuchan(grafo_usuarios_canciones, canciones):
    """
    Apartir del grafo bi partito se crea un diccionario de listas en el que como clave se tienen
    las canciones y como datos listas con los usuarios que tienen esas canciones en us playlist
    La complejidad de esto es O((u + c + l) + c + (u + c + l)) siendo u los usuarios, c las canciones
    y l las listas de reproduccion o aristas
    el primer u + c + l es por el DFS, la c es por recorrer las canciones y agregarlas al diccionario
    y el segundo u + c + l es porque recorro el dicc de padres y cada vez que encuentro un usuario
    recorro sus adyacentes 
    Nota: Por como funciona la notacion O se puede decir que este algoritmo es O(u + c + l)
    """
    vertice_aleatorio = random.choice(canciones)
    dicc = {}
    padres, orden = biblioteca_de_funciones.dfs(grafo_usuarios_canciones, vertice_aleatorio)
    for can in canciones:
        if can not in dicc:
            dicc[can] = []
    for dato in padres:
        # Si el orden del vertice no es divisible por 2, significa que es un usuario,
        # porque el grafo es bi partito
        if orden[dato] % 2 != 0:
            for w in grafo_usuarios_canciones.adyacentes(dato):
                dicc[w].append(dato)
    return dicc

def unir_vertices(grafo, lista_de_vertices):
    """
    Se le pasa una lista de canciones y un grafo (que ya tiene cargados los vertices)
    y crea una arista entre todas las canciones de la lista
    El orden de complejidad de esto es O(n ** 2) siendo n el largo de la lista
    """
    longitud_lista = len(lista_de_vertices)
    if longitud_lista <= 1:
        return
    for i in range(longitud_lista):
        for j in range(0, longitud_lista - 1):
            if i == j:
                continue
            grafo.agregar_arista(lista_de_vertices[i], lista_de_vertices[j])

# NOTA IMPORTANTE: Revisar si esta complejidad puede ser mejorada
# en el grupo del wpp alguien dijo que lo hizo cuadratico. Siento que, o se confundio,
# o mi mente primigenia no esta preparada para entender como hacerlo tan rapido

def relaciones_canciones(grafo_usuarios_canciones, canciones, usuarios):
    """
    A partir del grafo bi partito se crea un nuevo grafo que conecta a las canciones
    que comparten usuario. Crear el dicc es O(u + c + l), luego agregar los vertices al grafo
    es O(c). Ahora la parte de generar la lista es O(u * c), porque por cada usuario recorro todas 
    las canciones. Notar que la cantidad de usuarios es mucho menor que la cantida de canciones. 
    Por ultimo unir los vertices me cuesta O(n ** 2).
    La complejidad quedaria: O((u + c + l) + (u * c) * (n ** 2)) = O((u * c) * (n ** 2))
    Nota: Estoy muy tentado a decir que el n ** 2 casi es despreciable frente al u * c,
    ya que ese n son la cantidad de canciones que comparten usuario,
    que (creo) es menor a u * c
    """
    dicc = crear_diccionario_de_canciones_y_usuarios_que_la_escuchan(grafo_usuarios_canciones, canciones)
    grafo = Grafo()
    for cancion in canciones:
        grafo.agregar_vertice(cancion)
    for usuario in usuarios:
        lista_canciones_que_comparten_usuarios = []
        for clave in dicc:
            if usuario in dicc[clave]:
                lista_canciones_que_comparten_usuarios.append()
        unir_vertices(grafo, lista_canciones_que_comparten_usuarios) 
    return grafo           

# Camino

def camino(grafo_canciones_usuarios, origen, destino):
    if origen not in grafo_canciones_usuarios.obtener_vertices() or destino not in grafo_canciones_usuarios.obtener_vertices():
        print("Tanto el origen como el destino deben ser canciones")
        return
    padres, _ = biblioteca_de_funciones.bfs(grafo_canciones_usuarios, origen)
    print(padres)

# Mas importantes

def ordenar_lista_de_tuplas(lista_de_tuplas):
    return lista_de_tuplas.sort(reverse = True, key = lambda tupla: tupla[1])

def mas_importantes(relaciones_de_canciones, n):
    diccionario_ranking = biblioteca_de_funciones.page_rank(relaciones_de_canciones)
    lista = list(diccionario_ranking.items())
    ordenar_lista_de_tuplas(lista)

    for i in range(n):
        print(lista[i][1])

# Recomendacion

def recomendacion():
    # Se le paso el grafo bi partito 
    pass

# Ciclo de n canciones

def ciclo():
    pass

# Todas en Rango

def rango(grafo, n, cancion):
    # El grafo que recibe esta funcion es el de relaciones de canciones
    # Se utiliza un bfs comun y no uno completo porque si una cancion se encuentra en
    # otra componente conexa es imposible que este a n saltos de la cancion que se pasa
    _, orden = biblioteca_de_funciones.bfs(grafo, cancion)
    canciones_a_n_saltos = 0
    for _cancion in orden:
        if orden[_cancion] == n:
            canciones_a_n_saltos += 1
    return canciones_a_n_saltos

# Funciones auxiliares

def parseo_de_comando(comando_y_parametro):
    comando = ""
    parametro = ""
    indice = 0
    freno = False
    while indice != len(comando_y_parametro) and not freno:
        if comando_y_parametro[indice] != " ":
            comando += comando_y_parametro[indice]
        else:
            freno = True
        indice += 1
    while indice != len(comando_y_parametro):
        parametro += comando_y_parametro[indice]
        indice += 1

    return comando, parametro

# Main

def main(archivo_spotify):
    archivo = open(archivo_spotify)
    usuarios_canciones, _ = estructuras_basicas(archivo)
    archivo.close()

    usuario_input = ""
    while usuario_input != "\0":
        usuario_input = input()
        comando, parametro = parseo_de_comando(usuario_input)

        if comando == CAMINO:
            camino(usuarios_canciones, "Don't Go Away - Oasis", "Quitter - Eminem")
        elif comando == MAS_IMPORTANTES:
            mas_importantes()

        elif comando == RECOMENDACION:
            recomendacion()
        
        elif comando == CICLO:
            ciclo()

        elif comando == RANGO:
            n_y_cancion = parametro.split(" ")

            rango()
        
        else:
            print("Comando incorrecto")


script, archivo_spotify = argv
main(archivo_spotify)


# Esto es para debuggear el programa
# archivo = open("spotify-mini.tsv")
# main(archivo)
# archivo.close()
