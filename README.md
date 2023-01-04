# SOKOBAN

Sokoban es un clásico puzzle realizado como proyecto final para la materia **Algoritmos y Programación I** en la Universidad de Buenos Aires.

Este juego está desarrollado en Python, utilizando la librería [Gamelib](https://dessaya.github.io/python-gamelib/ "Gamelib").

![](https://github.com/AlexiaAroa/Sokoban-Python/blob/master/img/sokoban.png)

## Niveles
El juego está compuesto por 155 niveles, los cuales se obtienen mediante la lectura de un archivo (niveles.txt).

Caracteres que representan los elementos del juego:


| Elemento  | Caracter  |
| ------------ |:------------:|
| Pared  | #  |
| Caja  | $  |
| Jugador  | @  |
| Objetivo  | .  |
| Objetivo con Caja  | *  |
| Objetivo con Jugador  | +  |

## Comandos
Los comandos, al igual que los niveles, se obtienen mediante la lectura de un archivo (teclas.txt). Por defecto, contiene los siguientes:

| Teclas  | Dirección  |
|:------------:|:------------:|
| ↑ or "w" | Arriba  |
| ↓ or "s"  | Abajo  |
| → or "d"  | Derecha  |
| ← or "a"  | Izquierda |
| "r"  | Reiniciar  |
| "Escape"  | Salir  |
| "z"  | Deshacer  |
| "y"  | Rehacer  |
| "p"  | Pistas  |
