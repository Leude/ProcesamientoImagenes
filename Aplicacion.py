import PySimpleGUI as sg
import cv2

from Vista import window_principal, datos_tabla
from Util import cambiar_dimension_cuadrado, generar_archivo, abrir_archivo, guardar_archivo, guardar_archivo_como
from Imagen import Imagen

window = window_principal()

lim_ancho = 400
lim_alto = 300

global imagen
global imagen_copia
global imagen_histograma
global ruta
global cordenadas
global region
global proceso
global imagen_objeto

ruta = ""
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-ABRIR_ARCHIVO-':
        ruta = values['-ABRIR_ARCHIVO-']
        imagen = abrir_archivo(ruta)
    if event == '-GUARDAR_ARCHIVO-':
        guardar_archivo(ruta, imagen)
    if event == '-GUARDAR_ARCHIVO_COMO-':
        ruta = values['-GUARDAR_ARCHIVO_COMO-']
        guardar_archivo_como(ruta, imagen)
    if event == '-GENERAR_IMAGEN-':
        imagen, ruta = generar_archivo()
    if event == '-EJECUTAR_PROCESO-':
        valor = values['-TABLA_PROCESOS-']
        if not valor:
            sg.popup_error("Seleciona Un Proceso")
        else:
            window["-PROPIEDADES_COLOR-"].update(visible=False)
            window["-PROPIEDADES_DESPLAZAR-"].update(visible=False)
            window["-PROPIEDADES_ROTAR-"].update(visible=False)
            window["-PROPIEDADES_LOG-"].update(visible=False)
            window["-PROPIEDADES_POT-"].update(visible=False)
            window["-PROPIEDADES_BRILLO-"].update(visible=False)
            window["-PROPIEDADES_CONTRASTE-"].update(visible=False)
            window["-PROPIEDADES_SHRINK-"].update(visible=False)
            window["-PROPIEDADES_SLIDE-"].update(visible=False)
            window["-PROPIEDADES_THERSHOLDING-"].update(visible=False)

            if valor == [0]:
                imagen = Imagen(imagen).zoom_region()
            if valor == [1]:
                imagen = Imagen(imagen).pixelear_region()
            if valor == [2]:
                imagen_objeto = Imagen(imagen)
                imagen = imagen_objeto.limpiar_imagen()
                window["-PROPIEDADES_COLOR-"].update(visible=True)
            if valor == [3]:
                imagen = Imagen(imagen).copiar_pegar_imagen()
            if valor == [4]:
                imagen = 255 - imagen
            if valor == [5]:
                imagen_objeto = Imagen(imagen)
                window["-PROPIEDADES_DESPLAZAR-"].update(visible=True)
            if valor == [6]:
                imagen_objeto = Imagen(imagen)
                window["-PROPIEDADES_ROTAR-"].update(visible=True)
            if valor == [7]:
                imagen = Imagen(imagen).espejo_imagen()
            if valor == [8]:
                imagen_objeto = Imagen(cv2.imread(ruta, 0))
                window["-PROPIEDADES_LOG-"].update(visible=True)
            if valor == [9]:
                imagen_objeto = Imagen(cv2.imread(ruta, 0))
                window["-PROPIEDADES_POT-"].update(visible=True)
            if valor == [10]:
                imagen_objeto = Imagen(cv2.imread(ruta, 0))
                window["-PROPIEDADES_BRILLO-"].update(visible=True)
            if valor == [11]:
                imagen_objeto = Imagen(cv2.imread(ruta, 0))
                window["-PROPIEDADES_CONTRASTE-"].update(visible=True)
            if valor == [12]:
                imagen = Imagen(cv2.imread(ruta, 0)).stretch()
            if valor == [13]:
                imagen_objeto = Imagen(cv2.imread(ruta, 0))
                window["-PROPIEDADES_SHRINK-"].update(visible=True)
            if valor == [14]:
                imagen_objeto = Imagen(cv2.imread(ruta, 0))
                window["-PROPIEDADES_SLIDE-"].update(visible=True)
            if valor == [15]:
                imagen = Imagen(cv2.imread(ruta, 0)).ecualizacion()
            if valor == [16]:
                imagen_objeto = Imagen(cv2.imread(ruta, 0))
                window["-PROPIEDADES_THERSHOLDING-"].update(visible=True)

    if event == "-APLICAR_COLOR-":
        imagen = imagen_objeto.limpiar_imagen_selecionada(values["-AZUL-"], values["-VERDE-"], values["-ROJO-"])
    if event == '-APLICAR_IZQUIERDA-':
        cantidad = values["-PIXELES-"] * (-1)
        imagen = imagen_objeto.desplazar_imagen(cantidad)
    if event == '-APLICAR_DERECHA-':
        cantidad = values["-PIXELES-"]
        imagen = imagen_objeto.desplazar_imagen(cantidad)
    if event == '-APLICAR_ARRIBA-':
        cantidad = values["-PIXELES-"] * (-1)
        imagen = imagen_objeto.desplazar_imagen(cantidad, horizontal=False)
    if event == '-APLICAR_ABAJO-':
        cantidad = values["-PIXELES-"]
        imagen = imagen_objeto.desplazar_imagen(cantidad, horizontal=False)
    if event == "-APLICAR_ROTAR-":
        grados = values["-GRADOS-"]
        imagen = imagen_objeto.rotar_imagen(grados)
    if event == "-APLICAR_LOG-":
        constante = values["-CONSTANTE_LOG-"]
        imagen = imagen_objeto.transformacion_logaritmica(constante)
    if event == "-APLICAR_POT-":
        constante = values["-CONSTANTE_POT-"]
        imagen = imagen_objeto.transformación_potencia(constante)
    if event == "-APLICAR_BRILLO-":
        constante = int(values["-CONSTANTE_BRILLO-"])
        imagen = imagen_objeto.brillo_imagen(constante)
    if event == "-APLICAR_CONTRASTE-":
        constante = values["-CONSTANTE_CONTRASTE-"]
        constante2 = values["-CONSTANTE_CONTRASTE2-"]
        imagen = imagen_objeto.contraste(constante2, constante)
    if event == "-APLICAR_SHRINK-":
        constante = values["-CONSTANTE_SHRINK-"]
        constante2 = values["-CONSTANTE_SHRINK2-"]
        imagen = imagen_objeto.shrink(constante, constante2)
    if event == "-APLICAR_SLIDE-":
        constante = values["-CONSTANTE_SLIDE-"]
        imagen = imagen_objeto.slide(constante)
    if event == "-APLICAR_THERSHOLDING-":
        constante = values["-CONSTANTE_THERSHOLDING-"]
        imagen = imagen_objeto.thersholding(constante)

    if event == "-ABRIR_ARCHIVO-" or event == "-GENERAR_IMAGEN-":
        window["-TABLA_PROCESOS-"].Update(values=datos_tabla())
        window["-PROPIEDADES_COLOR-"].update(visible=False)
        window["-PROPIEDADES_DESPLAZAR-"].update(visible=False)
        window["-PROPIEDADES_ROTAR-"].update(visible=False)
        window["-PROPIEDADES_LOG-"].update(visible=False)
        window["-PROPIEDADES_POT-"].update(visible=False)
        window["-PROPIEDADES_BRILLO-"].update(visible=False)
        window["-PROPIEDADES_CONTRASTE-"].update(visible=False)
        window["-PROPIEDADES_SHRINK-"].update(visible=False)
        window["-PROPIEDADES_SLIDE-"].update(visible=False)
        window["-PROPIEDADES_THERSHOLDING-"].update(visible=False)

    try:
        window["-RUTA-"].Update(value=ruta)
        window["-ALTO_P-"].Update(value=imagen.shape[0])
        window["-ANCHO_P-"].Update(value=imagen.shape[1])
        # Actualiza la imagen
        nueva_dimension = cambiar_dimension_cuadrado(lim_alto, lim_ancho, imagen.shape[0], imagen.shape[1])
        imagen_res = cv2.resize(imagen, nueva_dimension, interpolation=cv2.INTER_AREA)
        window["-VER_IMAGEN-"].Update(data=cv2.imencode('.png', imagen_res)[1].tobytes())
        # Actualiza el histograma
        imagen_histograma = Imagen(imagen).crear_histograma()
        nueva_dimension = cambiar_dimension_cuadrado(lim_alto, lim_ancho, imagen_histograma.shape[0],
                                                     imagen_histograma.shape[1])
        imagen_histograma_res = cv2.resize(imagen_histograma, nueva_dimension, interpolation=cv2.INTER_AREA)
        window["-VER_HISTOGRAMA-"].Update(data=cv2.imencode('.png', imagen_histograma_res)[1].tobytes())

    except:
        None

# --------------------------------- Close & Exit ---------------------------------
window.close()
