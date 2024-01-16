from constantes import CAJA, PARED, VACIO, JUGADOR, OBJETIVO, OBJETIVO_Y_CAJA, OBJETIVO_Y_JUGADOR

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador
    '''
    
    return [list(fila) for fila in desc]

def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    columnas = len(grilla[0])
    filas = len(grilla)
    return columnas, filas

def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    return grilla[f][c] == PARED

def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo (solo, con caja o con el jugador) en la columna y fila (c, f).'''
    return grilla[f][c] == OBJETIVO or grilla[f][c] == OBJETIVO_Y_CAJA or grilla[f][c] == OBJETIVO_Y_JUGADOR

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja (sola o con un objetivo) en la columna y fila (c, f).'''
    return grilla[f][c] == CAJA or grilla[f][c] == OBJETIVO_Y_CAJA

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador (solo o con un objetivo) está en la columna y fila (c, f).'''
    return grilla[f][c] == JUGADOR or grilla[f][c] == OBJETIVO_Y_JUGADOR

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for f in range(len(grilla)):
        for c in range(len(grilla[f])):
            if hay_objetivo(grilla, c, f) and not hay_caja(grilla, c, f):
                return False
    return True

def esta_dentro_de_grilla(grilla, c, f):
    '''Devuelve True si la celda de columna y fila (c, f) es parte de la grilla.'''
    cantidad_columnas, cantidad_filas = dimensiones(grilla)
    return 0 <= c <= cantidad_columnas - 1 and 0 <= f <= cantidad_filas - 1

def es_valido(grilla, c, f, direccion):
    '''Devuelve True si el movimiento es válido.'''
    if not esta_dentro_de_grilla(grilla, c, f) or hay_pared(grilla, c, f):
        return False
    if not hay_caja(grilla, c, f):
        return True
    if not esta_dentro_de_grilla(grilla, c + direccion[0], f + direccion[1]):
        return False
    return not hay_caja(grilla, c + direccion[0], f + direccion[1]) and not hay_pared(grilla, c + direccion[0], f + direccion[1])

def realizar_movimiento(grilla, c, f, direccion, jugadas):
    '''Se efectúa el movimiento correspondiente de acuerdo a una direccion y jugadas dadas'''
    for i in range(len(jugadas)):
        grilla[f + direccion[1] * i][c + direccion[0] * i] = jugadas[i]

def actualizar_grilla(grilla, c, f, direccion):
    '''Se actualiza la grilla con el movimiento correspondiente'''
    jugadas = []

    if hay_objetivo(grilla, c, f):
        jugadas.append(OBJETIVO)
    else:
        jugadas.append(VACIO)

    if hay_objetivo(grilla, c + direccion[0], f + direccion[1]):
        jugadas.append(OBJETIVO_Y_JUGADOR)
    else:
        jugadas.append(JUGADOR)

    if hay_caja(grilla, c + direccion[0], f + direccion[1]):
        if hay_objetivo(grilla, c + direccion[0] * 2, f + direccion[1] * 2):
            jugadas.append(OBJETIVO_Y_CAJA)
        else:
            jugadas.append(CAJA)

    realizar_movimiento(grilla, c, f, direccion, tuple(jugadas))

def duplicar_grilla(grilla):
    '''Realizo una copia de la grilla inicial'''
    return [fila.copy() for fila in grilla]

def obtener_posicion_jugador(grilla):
    '''Se obtiene la posición del jugador'''

    for f in range(len(grilla)):
        for c in range(len(grilla[f])):
            if hay_jugador(grilla, c, f):
                return c, f
    
def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''
    posicion_columna, posicion_fila = obtener_posicion_jugador(grilla)

    if not es_valido(grilla, posicion_columna + direccion[0], posicion_fila + direccion[1], direccion):
        return grilla

    grilla_actualizada = duplicar_grilla(grilla)
    actualizar_grilla(grilla_actualizada, posicion_columna, posicion_fila, direccion)
    return grilla_actualizada
