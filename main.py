import soko
import gamelib
from pila import Pila

TAMANIO_CELDA = 32
OESTE = (-1, 0)
ESTE = (1, 0)
NORTE = (0, -1)
SUR = (0, 1)
DIRECCIONES = { 'OESTE': OESTE, 'ESTE': ESTE, 'NORTE': NORTE, 'SUR': SUR }

GRILLA = 0
NIVEL = 1
MOVIMIENTOS_DESHACER = 2
MOVIMIENTOS_REHACER = 3
MOVIMIENTOS_PISTAS = 4

SOLUCION_ENCONTRADA = 0
SOLUCIONES = 1

ARCHIVO_NIVELES = 'texto/niveles.txt'
ARCHIVO_TECLAS = 'texto/teclas.txt'

SALIR, REINICIAR, REHACER, DESHACER, PISTAS = 'SALIR', 'REINICIAR', 'REHACER', 'DESHACER', 'PISTAS'
LEVEL_HEADER = 'Level'
JUEGO_TITULO = 'Sokoban'
GROUND = 'GROUND'
SPRITES = { soko.OBJETIVO: 'img/goal.gif', soko.PARED: 'img/wall.gif', soko.JUGADOR: 'img/player.gif', soko.CAJA: 'img/box.gif', GROUND: 'img/ground.gif'}

ERROR_1, ERROR_2, ERROR_3, JUEGO_TERMINADO = 'ERROR_1', 'ERROR_2', 'ERROR_3','JUEGO_TERMINADO'
MENSAJES = { ERROR_1: 'Error: faltan archivos necesarios para el juego',
             ERROR_2: 'Error: el formato del archivo de teclas/niveles es incorrecto',
             ERROR_3: 'No se encontraron pistas',
             JUEGO_TERMINADO: '¡FELICIDADES! GANO EL JUEGO' }

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.'''
    maxima_longitud = len(max(desc, key = len))
    for i in range(len(desc)):
        desc[i] = desc[i].ljust(maxima_longitud)
    
    return soko.crear_grilla(desc)

def crear_juego():
    '''Crea un juego basado en un diccionario con el nivel como clave y su grilla como valor.'''
    juego = {}
    desc = []
    nivel = ''
    with open(ARCHIVO_NIVELES) as f:
        for linea in f:
            linea = linea.rstrip('\n')

            if LEVEL_HEADER in linea:
                nivel = linea
            elif soko.PARED in linea:
                desc.append(linea)
            elif not linea:
                juego[nivel] = crear_grilla(desc)
                desc = []

        juego[nivel] = crear_grilla(desc)
    
    ultimo_nivel = int(nivel.split(' ')[1])

    return juego, ultimo_nivel

def obtener_controles():
    '''Se obtienen los controles del juego de acuerdo a un archivo de texto.'''
    controles = {}

    with open(ARCHIVO_TECLAS) as f:
        for linea in f:
            linea = linea.rstrip('\n').split(' = ')
            if not linea[0]:
                continue

            tecla, direccion = linea
            controles[tecla] = DIRECCIONES.get(direccion, direccion)

    return controles

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

    for direccion in DIRECCIONES.values():
        nuevo_estado = soko.mover(estado, direccion)
        if convertir_a_cadena(nuevo_estado) in visitados:
            continue

        solucion_encontrada, acciones = backtrack(nuevo_estado, visitados)

        if solucion_encontrada:
            acciones.apilar(direccion)
            return True, acciones

    return False, None

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
        solucion = buscar_solucion(estado_de_juego[GRILLA])

        if solucion[SOLUCION_ENCONTRADA]:
            estado_de_juego[MOVIMIENTOS_PISTAS] = solucion[SOLUCIONES]
        else:
            gamelib.say(MENSAJES[ERROR_3])
        
    except RecursionError:
        gamelib.say(MENSAJES[ERROR_3])
    
    return tuple(estado_de_juego)

def obtener_sprites_de_casilla(grilla, c, f):
    '''Devuelve una tupla con los sprites de una celda.'''
    sprites = [GROUND]
    if soko.hay_caja(grilla, c, f):
        sprites.append(soko.CAJA)
    if soko.hay_objetivo(grilla, c, f):
        sprites.append(soko.OBJETIVO)
    if soko.hay_jugador(grilla, c, f):
        sprites.append(soko.JUGADOR)
    if soko.hay_pared(grilla, c, f):
        sprites.append(soko.PARED)

    return tuple(sprites)

def juego_mostrar(estado_de_juego):
    '''Actualizar la ventana.'''
    for f in range(len(estado_de_juego[GRILLA])):
        for c in range(len(estado_de_juego[GRILLA][f])):
            sprites = obtener_sprites_de_casilla(estado_de_juego[GRILLA], c, f)
            for sprite in sprites:
                gamelib.draw_image(SPRITES[sprite], c * TAMANIO_CELDA, f * TAMANIO_CELDA)

    if not estado_de_juego[MOVIMIENTOS_PISTAS].esta_vacia():
        gamelib.draw_text('Pista disponible', 70, 20, bold=True, italic=True)
    else:
        gamelib.draw_text('', 70, 20)

def actualizar_tamanio_ventana(grilla):
    '''Actualizar tamaño de la ventana.'''
    ancho_ventana, alto_ventana = len(grilla[0]) * TAMANIO_CELDA, len(grilla) * TAMANIO_CELDA
    gamelib.resize(ancho_ventana, alto_ventana)

def main():
    # Inicializar el estado del juego
    try:
        juego, ultimo_nivel = crear_juego()
        controles = obtener_controles()
    except FileNotFoundError:
        gamelib.say(MENSAJES[ERROR_1])
        return
    except ValueError:
        gamelib.say(MENSAJES[ERROR_2])
        return

    estado_de_juego = obtener_grilla_nivel(juego,  1)
    gamelib.title(JUEGO_TITULO)
    actualizar_tamanio_ventana(estado_de_juego[GRILLA])

    while gamelib.is_alive():
        gamelib.draw_begin()
        # Dibujar la pantalla
        juego_mostrar(estado_de_juego)
        
        gamelib.draw_end()

        if soko.juego_ganado(estado_de_juego[GRILLA]):
            if estado_de_juego[NIVEL] == ultimo_nivel:
                gamelib.say(MENSAJES[JUEGO_TERMINADO])
                break

            estado_de_juego = obtener_grilla_nivel(juego, estado_de_juego[NIVEL] + 1)
            actualizar_tamanio_ventana(estado_de_juego[GRILLA])
            continue

        ev = gamelib.wait(gamelib.EventType.KeyPress)

        if not ev:
            break

        tecla = ev.key
        # Actualizar el estado del juego, según la `tecla` presionada
        if tecla not in controles:
            continue
        
        if controles[tecla] == SALIR:
            break
            
        elif controles[tecla] == REINICIAR:
            estado_de_juego = obtener_grilla_nivel(juego, estado_de_juego[NIVEL])

        elif controles[tecla] == REHACER:
            if not estado_de_juego[MOVIMIENTOS_REHACER].esta_vacia():
                guardar_movimiento(estado_de_juego[GRILLA], estado_de_juego[MOVIMIENTOS_DESHACER])
                estado_de_juego = recuperar_movimiento_pila(estado_de_juego, MOVIMIENTOS_REHACER)
            
        elif controles[tecla] == DESHACER:
            if not estado_de_juego[MOVIMIENTOS_DESHACER].esta_vacia():
                guardar_movimiento(estado_de_juego[GRILLA], estado_de_juego[MOVIMIENTOS_REHACER])
                estado_de_juego = recuperar_movimiento_pila(estado_de_juego, MOVIMIENTOS_DESHACER)

        elif controles[tecla] == PISTAS:
            estado_de_juego = obtener_pistas(estado_de_juego)

        else:
            estado_de_juego = procesar_movimiento(estado_de_juego, controles[tecla], True)

gamelib.init(main)
