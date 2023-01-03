import soko
from pila import Pila

OESTE = (-1, 0)
ESTE = (1, 0)
NORTE = (0, -1)
SUR = (0, 1)
DIRECCIONES = [OESTE, ESTE, NORTE, SUR]

def convertir_a_cadena(estado_grilla):
    '''Convierte la grilla en una cadena.'''
    cadena = ''
    for fila in estado_grilla:
        cadena += ''.join(fila)

    return cadena

def buscar_solucion(estado_inicial):
    '''Retorna la solución obtenida.'''
    visitados = set()
    return backtrack(estado_inicial, visitados)

def backtrack(estado, visitados):
    '''Busca una solución.'''
    visitados.add(convertir_a_cadena(estado))

    if soko.juego_ganado(estado):
        return True, Pila()

    for direccion in DIRECCIONES:
        nuevo_estado = soko.mover(estado, direccion)
        if convertir_a_cadena(nuevo_estado) in visitados:
            continue

        solucion_encontrada, acciones = backtrack(nuevo_estado, visitados)

        if solucion_encontrada:
            acciones.apilar(direccion)
            return True, acciones

    return False, None