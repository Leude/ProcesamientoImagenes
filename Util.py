import os

import cv2
import numpy as np
import PySimpleGUI as sg

from Vista import window_vista_requisito


def eliminar_archivo(archivo):
    if os.path.exists(archivo):
        os.remove(archivo)


def imagen_aleatoria(alto, ancho):
    archivo = "random.pgm"
    matriz = np.random.randint(256, size=(alto, ancho))
    np.savetxt(archivo, matriz, header="P2\n" + str(ancho) + "\t" + str(alto) + "\n255\n", fmt="%d", comments="")
    imagen = cv2.imread(archivo)
    return imagen,archivo

def cambiar_dimension_cuadrado(lim_alto, lim_ancho, ini_alto, ini_ancho):
    escala_alto = int(lim_alto * 100 / ini_alto)
    escala_ancho = int(lim_ancho * 100 / ini_ancho)
    if escala_ancho < escala_alto:
        porcentaje = escala_ancho
    else:
        porcentaje = escala_alto
    escala = porcentaje / 100
    new_alto = int(ini_alto * escala)
    new_ancho = int(ini_ancho * escala)
    nueva_dimension = (new_ancho, new_alto)

    return nueva_dimension

def abrir_archivo(ruta):
    try:

        imagen = cv2.imread(ruta)
        return imagen
    except:
        sg.popup_error("Tipo de archivo no valido", no_titlebar=True, keep_on_top=True)

def guardar_archivo(ruta,imagen):
    try:
        if ruta != "":
            cv2.imwrite(ruta, imagen)
    except:
        sg.popup_error("Abre o Genera una Imagen", no_titlebar=True, keep_on_top=True)

def guardar_archivo_como(ruta,imagen):
    cv2.imwrite(ruta, imagen)

def generar_archivo():
    ruta = ""
    global imagen
    try:
        window_requisito = window_vista_requisito()
        while True:
            evento_requisito, valores_requisito = window_requisito.read()
            if evento_requisito == sg.WIN_CLOSED:
                break
            if evento_requisito == '-OK-':
                ancho = int(valores_requisito['-ANCHO-'])
                alto = int(valores_requisito['-ALTO-'])
                imagen,ruta = imagen_aleatoria(alto, ancho)
                break
        window_requisito.close()
        return imagen,ruta
    except:
        sg.popup_error("Ingresa Valores Correctos", no_titlebar=True, keep_on_top=True)