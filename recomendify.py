#!/usr/bin/python3

# Imports

from grafo import Grafo
import biblioteca_de_funciones
import sys

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
NO_FUE_CREADO = 0
CANCIONES = "canciones"
USUARIOS = "usuarios"
PLAYLIST_ID = 0
PLAYLIST_NOMBRE = 1

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
    Crea un diccionario de usuarios con sus playlist que se ve asi
    {usuario1:{(playlist_id_1, playlist_nombre_1):{(cancion1 - artista1), (cancion2 - artista2)}
    (playlist_id_2, playlist_nombre_2):{(cancion3 - artista3)}}, usuario2: .... }
    Crea un set con el nombre y artista/grupo que compuso cada cancion
    """
    set_de_canciones = set()
    diccionario_usuarios_playlist = {}
    usuarios_canciones = Grafo() 
    id, usuario, cancion, artista, playlist_id, playlist, generos = leer_linea(archivo)
    while id != MAX:
        usuarios_canciones.agregar_vertice(usuario)
        usuarios_canciones.agregar_vertice((cancion, artista))
        usuarios_canciones.agregar_arista(usuario, (cancion, artista))

        if usuario not in diccionario_usuarios_playlist:
            diccionario_usuarios_playlist[usuario] = {}
        
        if (playlist_id, playlist) not in diccionario_usuarios_playlist[usuario]:
            diccionario_usuarios_playlist[usuario][(playlist_id, playlist)] = set()

        diccionario_usuarios_playlist[usuario][(playlist_id, playlist)].add((cancion, artista))
        set_de_canciones.add((cancion, artista))

        id, usuario, cancion, artista, playlist_id, playlist, generos = leer_linea(archivo)

    return usuarios_canciones, set_de_canciones, diccionario_usuarios_playlist

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

def proyeccion_de_grafo(grafo_usuarios_canciones, canciones, usuarios):
    grafo_proyectado = Grafo()
    for cancion in canciones:
        grafo_proyectado.agregar_vertice(cancion)
    diccionario_aux = {}
    for usuario in usuarios:
        diccionario_aux[usuario] = []
    padres, _ = biblioteca_de_funciones.bfs_completo(grafo_usuarios_canciones)
    for vertice in padres:
        if padres[vertice] == None:
            continue
        elif vertice in diccionario_aux:
            diccionario_aux[vertice].append(padres[vertice])
        else:
            diccionario_aux[padres[vertice]].append(vertice)
    for lista in diccionario_aux:
        unir_vertices(grafo_proyectado, diccionario_aux[lista])
    return grafo_proyectado

# Camino

def reconstruir_camino(padre, inicio, fin):
  v = fin
  camino = []
  while v != inicio:
    camino.append(v)
    v = padre[v]
  return camino[::-1]

def camino(grafo_canciones_usuarios, origen, destino, diccionario_usuarios_playlist):
    padres, _ = biblioteca_de_funciones.bfs(grafo_canciones_usuarios, origen)
    if destino not in padres:
        print("No se encontro recorrido", file = sys.stdout)
    else:
        flecha = " --> "
        guion = " - "
        imprimir = ""
        camino_a_seguir = reconstruir_camino(padres, origen, destino)
        camino_a_seguir.insert(0, origen)
        for i in range(len(camino_a_seguir) - 1):
            if i % 2 == 0:
                imprimir += camino_a_seguir[i][CANCION] + guion + camino_a_seguir[i][ARTISTA]
                imprimir += flecha
            else:
                cancion_anterior = camino_a_seguir[i-1]
                usuario = camino_a_seguir[i]
                cancion_siguiente = camino_a_seguir[i+1]
                for playlist in diccionario_usuarios_playlist[usuario]:
                    if cancion_anterior in diccionario_usuarios_playlist[usuario][playlist]:
                        play_list_que_aparece_anterior = playlist[PLAYLIST_NOMBRE]
                    if cancion_siguiente in diccionario_usuarios_playlist[usuario][playlist]:
                        play_list_que_aparece_siguiente = playlist[PLAYLIST_NOMBRE]
          
                imprimir += "aparece en playlist" + flecha + play_list_que_aparece_anterior + flecha + "de" + flecha + usuario + flecha + "tiene una playlist" + flecha + play_list_que_aparece_siguiente + flecha + "donde aparece" + flecha
        i += 1
        imprimir += camino_a_seguir[i][CANCION] + guion + camino_a_seguir[i][ARTISTA]
        print(imprimir)   
    
# Mas importantes

def ordenar_lista_de_tuplas(lista_de_tuplas):
    return lista_de_tuplas.sort(reverse = True, key = lambda tupla: tupla[1])

def impresion(lista, cantidad_imprimir, lista_de_tuplas = True):
    i = 0
    if lista_de_tuplas:
        for i in range(cantidad_imprimir-1):
            print("{cancion} - {artista}; ".format(cancion = lista[i][CANCION], artista = lista[i][ARTISTA]), end = '')
        i += 1
        print("{cancion} - {artista}".format(cancion = lista[i][CANCION], artista = lista[i][ARTISTA]))
    else:
        while i != cantidad_imprimir-1:
            print("{usuario}; ".format(usuario = lista[i]), end = '')
            i += 1
        print("{usuario}".format(usuario = lista[i]))

def mas_importantes(grafo_usuarios_canciones, set_de_canciones):
    diccionario_ranking = biblioteca_de_funciones.page_rank(grafo_usuarios_canciones, 10)
    lista = list(diccionario_ranking.items())
    ordenar_lista_de_tuplas(lista)

    importantes = []
    for tupla in lista:
        if tupla[0] in set_de_canciones:
            importantes.append(tupla[0])

    return importantes

# Recomendacion

def recomendacion(grafo_usuarios_canciones, n, usuarios_canciones, lista, set_usuarios, set_canciones):
    recomendaciones = {}
    largo_recorrido = n * n

    for cancion in lista:
        pr_personalizado = biblioteca_de_funciones.page_rank_personalizado(grafo_usuarios_canciones, cancion, largo_recorrido, 1000)
        for clave in pr_personalizado:
            if clave not in recomendaciones:
                recomendaciones[clave] = pr_personalizado[clave]
            else:
                recomendaciones[clave] += pr_personalizado[clave]

    lista_recomendaciones = list(recomendaciones.items())
    ordenar_lista_de_tuplas(lista_recomendaciones)
    lista_imprimir = []
    if usuarios_canciones == CANCIONES:
        # Elimino las canciones que estaban en la lista, ya que recomendar una cancion que uno ya escuha no tiene mucho sentido
        for elemento in lista:
            if elemento in recomendaciones:
                recomendaciones.pop(elemento)
        for clave in recomendaciones:   
            if len(lista_imprimir) == n:
                break
            if clave in set_usuarios:
                continue
            lista_imprimir.append(clave)
        impresion(lista_imprimir, n)
    else:
        for clave in recomendaciones:   
            if len(lista_imprimir) == n:
                break
            if clave in set_canciones:
                continue
            lista_imprimir.append(clave)
        impresion(lista_imprimir, n, False)

# Ciclo de n canciones

def __ciclo(grafo, camino, n, resultado):
    if len(resultado) == 0:
        inicial = camino[0]
        ultimo = camino[len(camino) - 1]
        for adyacente in grafo.adyacentes(ultimo):
            copia = camino[:]
            copia.append(adyacente)
            if (adyacente == inicial and len(camino) == n):
                # Encontre un ciclo de largo n
                resultado.append(copia)
            if (adyacente in camino or len(camino) > n) :
                continue
            __ciclo(grafo, copia, n, resultado)
    return resultado

def _ciclo(grafo, origen, n):
    resultado = []
    return __ciclo(grafo, [origen], n, resultado)

def ciclo(grafo_relacion_canciones , n, cancion):
    if n <= 0:
        print("Ponele voluntad...", file = sys.stdout)
    elif n == 1:
        print("{cancion} - {artista}".format(cancion = cancion[CANCION], artista = cancion[ARTISTA]))
    else:
        lista_ciclos_hamiltonianos = _ciclo(grafo_relacion_canciones, cancion, n)
        posible_ciclo = lista_ciclos_hamiltonianos[0]
        if posible_ciclo == []:
            print("No se encontro recorrido")
        else:
            for i in range(len(posible_ciclo) - 1):
                print("{cancion} - {artista} --> ".format(cancion = posible_ciclo[i][CANCION], artista = posible_ciclo[i][ARTISTA]), end = '')
            i += 1
            print("{cancion} - {artista}".format(cancion = posible_ciclo[i][CANCION], artista = posible_ciclo[i][ARTISTA]))

# Todas en Rango

def rango(grafo, n, cancion):
    # El grafo que recibe esta funcion es el de relaciones de canciones
    # Se utiliza un bfs comun y no uno completo porque si una cancion se encuentra en
    # otra componente conexa es imposible que este a n saltos de la cancion que se pasa
    _, orden = biblioteca_de_funciones.bfs(grafo, cancion)
    canciones_a_n_saltos = 0
    for _cancion in orden:
        #print("La cancion ", _cancion, "tiene un orden", orden[_cancion])
        if orden[_cancion] == int(n):
            canciones_a_n_saltos += 1
    print(canciones_a_n_saltos)

# Funciones de parseo de comandos

def parseo_de_comando(comando_y_parametro, separador):
    comando = ""
    parametro = ""
    indice = 0
    freno = False
    while indice != len(comando_y_parametro) and not freno:
        if comando_y_parametro[indice] != separador:
            comando += comando_y_parametro[indice]
        else:
            freno = True
        indice += 1
    while indice != len(comando_y_parametro):
        parametro += comando_y_parametro[indice]
        indice += 1

    return comando, parametro

def parseo_de_parametro_camino(parametro):
    pseudo_origen, pseudo_final = parametro.split('>>>>')
    origen = pseudo_origen[:-1]
    final = pseudo_final [1:]
    can1, art1 = parseo_de_comando(origen, "-")
    can2, art2 = parseo_de_comando(final, "-")
    return (can1[:-1], art1[1:]), (can2[:-1], art2[1:])

def parseo_recomendacion(parametro):
    usuario_cancion = ""
    n = ""
    indice = 0
    freno = False
    while not freno:
        if parametro[indice] != " ":
            usuario_cancion += parametro[indice]
        else:
            freno = True
        indice += 1
    freno = False
    while not freno:
        if parametro[indice] != " ":
            n += parametro[indice]
        else:
            freno = True
        indice += 1
        
    _lista_canciones = parametro[indice:].split('>>>>')
    lista_canciones = []
    for i in range(len(_lista_canciones)):
        if i == 0 and len(_lista_canciones) == 1:
            lista_canciones.append(_lista_canciones[i][:])
        elif i == 0:
            lista_canciones.append(_lista_canciones[i][:-1])
        elif i == (len(_lista_canciones) - 1):
            lista_canciones.append(_lista_canciones[i][1:])
        else:
            lista_canciones.append(_lista_canciones[i][1:-1])

    lista_retornada = []
    for cancion in lista_canciones:
        can, artista = parseo_de_comando(cancion, "-")
        lista_retornada.append((can[:-1], artista[1:]))
    
    return usuario_cancion, n, lista_retornada

def parseo_de_parametro_ciclo_rango(parametro):
    distancia = ""
    cancion = ""
    autor = ""
    indice = 0
    freno = False
    while indice != len(parametro) and not freno:
        if parametro[indice] != " ":
            distancia += parametro[indice]
        else:
            freno = True
        indice += 1

    freno = False
    while indice != len(parametro) and not freno:
        if parametro[indice] != "-":
            cancion += parametro[indice]
        else:
            freno = True
        indice += 1

    while indice != len(parametro):
        autor += parametro[indice]
        indice += 1
    return distancia, cancion[:-1], autor[1:]

# Main

def main(archivo_spotify):
    archivo = open(archivo_spotify)
    grafo_usuarios_canciones, set_de_canciones, diccionario_usuarios_playlist = estructuras_basicas(archivo)
    # Observacion, el diccionario_usuarios_playlist depende la funcion, directamente se usa como si fuese un set que tiene los nombres
    # de los usuarios
    archivo.close()

    grafo_relaciones_canciones = NO_FUE_CREADO
    importantes = []

    usuario_input = ""
    while usuario_input != "\0":
        try:
            usuario_input = input()
        except EOFError:
            return

        comando, parametro = parseo_de_comando(usuario_input, " ")

        if comando == CAMINO:
            origen, destino = parseo_de_parametro_camino(parametro)
            if origen not in set_de_canciones or destino not in set_de_canciones:
                print("Tanto el origen como el destino deben ser canciones", file = sys.stdout)
            else:
                camino(grafo_usuarios_canciones, origen, destino, diccionario_usuarios_playlist)
        
        elif comando == MAS_IMPORTANTES:
            if not parametro.isdigit(): 
                print("Ponele voluntad...", file = sys.stdout)
            if importantes == NO_FUE_CREADO:
                importantes = mas_importantes(grafo_usuarios_canciones, set_de_canciones)
            impresion(importantes, int(parametro))

        elif comando == RECOMENDACION:
            usuarios_canciones, cantidad_a_recomendar, lista_retornada = parseo_recomendacion(parametro)
            voluntadad = True
            i = 0
            while i != len(lista_retornada)- 1 and voluntadad:
                if lista_retornada[i] not in set_de_canciones:
                    voluntadad = False
                i += 1
            if not cantidad_a_recomendar.isdigit() or usuarios_canciones not in (CANCIONES, USUARIOS) or not voluntadad:
                print("Ponele voluntad...", file = sys.stdout)
            else:
                recomendacion(grafo_usuarios_canciones, int(cantidad_a_recomendar), usuarios_canciones, lista_retornada, diccionario_usuarios_playlist, set_de_canciones)
        
        elif comando == CICLO or comando == RANGO:
            if grafo_relaciones_canciones == NO_FUE_CREADO:
                grafo_relaciones_canciones = proyeccion_de_grafo(grafo_usuarios_canciones, set_de_canciones, diccionario_usuarios_playlist)
            
            n, cancion, autor = parseo_de_parametro_ciclo_rango(parametro)
            if (cancion, autor) not in set_de_canciones:
                print("Ponele voluntad...", file = sys.stdout)
            elif comando == CICLO:
                ciclo(grafo_relaciones_canciones, int(n), (cancion, autor))
            else:
                rango(grafo_relaciones_canciones, n, (cancion, autor))
        
        else:
            print("Comando incorrecto", file = sys.stdout)


script, archivo_spotify = sys.argv
main(archivo_spotify)
