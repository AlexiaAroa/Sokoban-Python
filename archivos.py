import soko
from constantes import LEVEL_HEADER, DIRECCIONES

ARCHIVO_NIVELES = 'texto/niveles.txt'
ARCHIVO_TECLAS = 'texto/teclas.txt'

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
