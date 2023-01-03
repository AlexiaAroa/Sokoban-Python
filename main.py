import soko
import gamelib
import archivos
import interfaz
import estado_de_juego as estado

SALIR, REINICIAR, REHACER, DESHACER, PISTAS = 'SALIR', 'REINICIAR', 'REHACER', 'DESHACER', 'PISTAS'

def main():
    # Inicializar el estado del juego
    try:
        juego, ultimo_nivel = archivos.crear_juego()
        controles = archivos.obtener_controles()
    except FileNotFoundError:
        interfaz.mostrar_mensaje(interfaz.ERROR_1)
        return
    except ValueError:
        interfaz.mostrar_mensaje(interfaz.ERROR_2)
        return

    estado_de_juego = estado.obtener_grilla_nivel(juego,  1)
    interfaz.mostrar_titulo()
    interfaz.actualizar_tamanio_ventana(estado_de_juego[estado.GRILLA])

    while gamelib.is_alive():
        gamelib.draw_begin()
        # Dibujar la pantalla
        interfaz.mostrar_juego(estado_de_juego)

        gamelib.draw_end()

        if soko.juego_ganado(estado_de_juego[estado.GRILLA]):
            if estado_de_juego[estado.NIVEL] == ultimo_nivel:
                interfaz.mostrar_mensaje(interfaz.JUEGO_TERMINADO)
                break

            estado_de_juego = estado.obtener_grilla_nivel(juego, estado_de_juego[estado.NIVEL] + 1)
            interfaz.actualizar_tamanio_ventana(estado_de_juego[estado.GRILLA])
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
            estado_de_juego = estado.obtener_grilla_nivel(juego, estado_de_juego[estado.NIVEL])

        elif controles[tecla] == REHACER:
            if not estado_de_juego[estado.MOVIMIENTOS_REHACER].esta_vacia():
                estado.guardar_movimiento(estado_de_juego[estado.GRILLA], estado_de_juego[estado.MOVIMIENTOS_DESHACER])
                estado_de_juego = estado.recuperar_movimiento_pila(estado_de_juego, estado.MOVIMIENTOS_REHACER)
            
        elif controles[tecla] == DESHACER:
            if not estado_de_juego[estado.MOVIMIENTOS_DESHACER].esta_vacia():
                estado.guardar_movimiento(estado_de_juego[estado.GRILLA], estado_de_juego[estado.MOVIMIENTOS_REHACER])
                estado_de_juego = estado.recuperar_movimiento_pila(estado_de_juego, estado.MOVIMIENTOS_DESHACER)

        elif controles[tecla] == PISTAS:
            estado_de_juego = estado.obtener_pistas(estado_de_juego)

        else:
            estado_de_juego = estado.procesar_movimiento(estado_de_juego, controles[tecla], True)

gamelib.init(main)
