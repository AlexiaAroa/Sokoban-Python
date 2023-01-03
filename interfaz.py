import soko
import gamelib

GROUND = 'GROUND'
SPRITES = { soko.OBJETIVO: 'img/goal.gif', soko.PARED: 'img/wall.gif', soko.JUGADOR: 'img/player.gif', soko.CAJA: 'img/box.gif', GROUND: 'img/ground.gif'}
GRILLA = 0
MOVIMIENTOS_PISTAS = 4
TAMANIO_CELDA = 32
JUEGO_TITULO = 'Sokoban'

ERROR_1, ERROR_2, ERROR_3, JUEGO_TERMINADO = 'ERROR_1', 'ERROR_2', 'ERROR_3','JUEGO_TERMINADO'
MENSAJES = { ERROR_1: 'Error: faltan archivos necesarios para el juego',
             ERROR_2: 'Error: el formato del archivo de teclas/niveles es incorrecto',
             ERROR_3: 'No se encontraron pistas',
             JUEGO_TERMINADO: '¡FELICIDADES! GANO EL JUEGO' }

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

def mostrar_juego(estado_de_juego):
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

def mostrar_titulo():
    '''Mostrar título del juego.'''
    gamelib.title(JUEGO_TITULO)

def mostrar_mensaje(mensaje):
    '''Mostrar el mensaje indicado.'''
    gamelib.say(MENSAJES[mensaje])
