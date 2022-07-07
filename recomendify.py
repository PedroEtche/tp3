# Imports

from grafo import Grafo
import biblioteca_de_funciones
from sys import argv

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

def grafo_canciones_usuarios(archivo):
    """
    Me crea un grafo bi partito. Los vertices son usuarios y canciones.
    Las aristas que conectan un usuario con una cancion significan ese usuario tiene la cancion en
    su playlist. Tambien crea un diccionario de diccionario de diccionario en el que cada clave 
    (usuario) tiene como dato un diccionario, que a su vez, tiene como clave un diccionario 
    (nombre_de_la_playlist) y como dato la informacion de la cancion
    """
    set_de_canciones = set()
    diccionario_playlist_canciones = {}
    usuarios_canciones = Grafo()
    id, usuario, cancion, artista, playlist_id, playlist, generos = leer_linea(archivo)
    while id != MAX:
        usuarios_canciones.agregar_vertice(usuario)
        usuarios_canciones.agregar_vertice((cancion, artista))
        usuarios_canciones.agregar_arista(usuario, (cancion, artista))

        if cancion not in set_de_canciones:
            set_de_canciones.add(cancion)

        id, usuario, cancion, artista, playlist_id, playlist, generos = leer_linea(archivo)

    #print(usuarios_canciones.adyacentes("sitevagalume"))
    #print(usuarios_canciones.adyacentes("fernandagi17"))
    #print(usuarios_canciones)
    return usuarios_canciones, set_de_canciones

def relaciones_canciones(usuarios_canciones, origen):
    padres, orden = biblioteca_de_funciones.bfs(grafo_canciones_usuarios, origen)


    pass

# Camino

def camino(grafo_canciones_usuarios, origen, destino):
    if origen not in grafo_canciones_usuarios.obtener_vertices() or destino not in grafo_canciones_usuarios.obtener_vertices():
        print("Tanto el origen como el destino deben ser canciones")
        return
    padres, _ = biblioteca_de_funciones.bfs(grafo_canciones_usuarios, origen)
    print(padres)

# Mas importantes

def mas_importantes():
    biblioteca_de_funciones.page_rank()
    pass

# Recomendacion

def recomendacion():
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
    usuarios_canciones, _ = grafo_canciones_usuarios(archivo)
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


# Esto a para debuggear el programa
# archivo = open("spotify-mini.tsv")
# main(archivo)
# archivo.close()