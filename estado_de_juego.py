from pila import Pila
import backtracking
import soko
import interfaz

GRILLA = 0
NIVEL = 1
MOVIMIENTOS_DESHACER = 2
MOVIMIENTOS_REHACER = 3
MOVIMIENTOS_PISTAS = 4

SOLUCION_ENCONTRADA = 0
SOLUCIONES = 1

LEVEL_HEADER = 'Level'

def obtener_grilla_nivel(juego, nivel):
    '''Devuelve la grilla y el nivel indicados.'''
    movimientos = Pila()
    movimientos_rehacer = Pila()
    pistas = Pila()
    nivel_titulo = f'{LEVEL_HEADER} {nivel}'
    return juego[nivel_titulo], nivel, movimientos, movimientos_rehacer, pistas

def guardar_movimiento(grilla, pila):
    '''Guardo el movimiento (grilla) en la pila indicada.'''
    if pila.esta_vacia() or pila.ver_tope() != grilla:
        pila.apilar(grilla)

def recuperar_movimiento_pila(estado_de_juego, pila_a_modificar):
    '''Recupera el movimiento de la pila indicada.'''
    estado_de_juego = list(estado_de_juego)
    estado_de_juego[GRILLA] = estado_de_juego[pila_a_modificar].desapilar()
    estado_de_juego[MOVIMIENTOS_PISTAS] = Pila()
    return tuple(estado_de_juego)

def procesar_movimiento(estado_de_juego, direccion, actualizar = False):
    '''Procesa el movimiento realizado.'''
    estado_de_juego = list(estado_de_juego)
    guardar_movimiento(estado_de_juego[GRILLA], estado_de_juego[MOVIMIENTOS_DESHACER])
    estado_de_juego[GRILLA] = soko.mover(estado_de_juego[GRILLA], direccion)
    estado_de_juego[MOVIMIENTOS_REHACER] = Pila()
    
    if actualizar:
        estado_de_juego[MOVIMIENTOS_PISTAS] = Pila()

    return tuple(estado_de_juego)

def obtener_pistas(estado_de_juego):
    '''Se obtienen las pistas del nivel actual.'''
    estado_de_juego = list(estado_de_juego)

    if not estado_de_juego[MOVIMIENTOS_PISTAS].esta_vacia():
        direccion = estado_de_juego[MOVIMIENTOS_PISTAS].desapilar()
        return procesar_movimiento(estado_de_juego, direccion)

    try:
        solucion = backtracking.buscar_solucion(estado_de_juego[GRILLA])

        if solucion[SOLUCION_ENCONTRADA]:
            estado_de_juego[MOVIMIENTOS_PISTAS] = solucion[SOLUCIONES]
        else:
            interfaz.mostrar_mensaje(interfaz.ERROR_3)
        
    except RecursionError:
        interfaz.mostrar_mensaje(interfaz.ERROR_3)
    
    return tuple(estado_de_juego)