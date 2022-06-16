import copy
import math

import cv2
import numpy as np
import PySimpleGUI as sg
from matplotlib import pyplot as plt

from Util import cambiar_dimension_cuadrado, eliminar_archivo


class Imagen:
    x_punto = 0
    y_punto = 0

    desplazado_x = 0
    desplazado_y = 0

    global region
    global cordenadas

    def __init__(self, imagen):
        self.imagen = imagen
        try:
            (self.alto_o, self.ancho_o, self.canales) = self.imagen.shape
        except:
            (self.alto_o, self.ancho_o) = self.imagen.shape
        self.centro = (self.ancho_o / 2, self.alto_o / 2)
        self.pixelmax = np.max(self.imagen)
        self.pixelmin = np.min(self.imagen)

    def crear_histograma(self):
        nombre = "Histograma"
        color = ('b', 'g', 'r')

        for i, col in enumerate(color):
            hist = cv2.calcHist([self.imagen], [i], None, [256], [0, 256])
            plt.plot(hist, color=col)
            plt.xlim([0, 256])

        plt.savefig(nombre)
        plt.cla()
        plt.clf()
        img_histograma = cv2.imread(nombre + ".png")
        eliminar_archivo(nombre + ".png")
        return img_histograma

    def selecionar_region(self):
        lim_ancho = 800
        lim_alto = 600
        nombre_window = "Selecciona una region"
        cv2.namedWindow(nombre_window, cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL)
        ancho_n, alto_n = cambiar_dimension_cuadrado(lim_alto, lim_ancho, self.alto_o, self.ancho_o)
        cv2.resizeWindow(nombre_window, ancho_n, alto_n)
        roi = cv2.selectROI(nombre_window, self.imagen)
        cv2.destroyWindow(nombre_window)
        x1 = int(roi[0])
        y1 = int(roi[1])
        x2 = int(roi[0] + roi[2])
        y2 = int(roi[1] + roi[3])
        roi_cropped = self.imagen[y1: y2, x1: x2]
        coordenadas = [(x1, y1), (x2, y2)]
        return roi_cropped, coordenadas

    def selecionar_punto(self):
        lim_ancho = 800
        lim_alto = 600
        nombre_window = "Selecciona un punto"
        cv2.namedWindow(nombre_window, cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL)
        ancho_n, alto_n = cambiar_dimension_cuadrado(lim_alto, lim_ancho, self.alto_o, self.ancho_o)
        cv2.resizeWindow(nombre_window, ancho_n, alto_n)
        cv2.setMouseCallback(nombre_window, self.mouse_click)
        cv2.imshow(nombre_window, self.imagen)
        cv2.waitKey()
        return self.x_punto, self.y_punto

    def mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse left button down condition
            self.x_punto = x
            self.y_punto = y
            cv2.destroyAllWindows()

    def zoom_region(self):
        try:
            roi, coordenadas = self.selecionar_region()
            imagen_copia = cv2.resize(roi, (self.ancho_o, self.alto_o))
            return imagen_copia
        except:
            sg.popup_error("No se puede hacer zoom en la region selecionada", no_titlebar=True, keep_on_top=True)
            return self.imagen

    def pixelear_region(self):
        region, coordenadas = self.selecionar_region()
        x, y = coordenadas[0]
        s, t = coordenadas[1]
        imagen = copy.deepcopy(self.imagen)
        imagen[0 + y:region.shape[0] + y, 0 + x:region.shape[1] + x] = cv2.blur(region,(region.shape[1],region.shape[0]))
        return imagen

    def limpiar_imagen(self, azul=0, verde=0, rojo=0):
        self.region, self.cordenadas = self.selecionar_region()
        imagen = copy.deepcopy(self.imagen)
        imagen[self.cordenadas[0][1]: self.cordenadas[1][1], self.cordenadas[0][0]: self.cordenadas[1][0]] = (
            azul, verde, rojo)
        return imagen

    def limpiar_imagen_selecionada(self, azul=0, verde=0, rojo=0):
        imagen = copy.deepcopy(self.imagen)
        imagen[self.cordenadas[0][1]: self.cordenadas[1][1], self.cordenadas[0][0]: self.cordenadas[1][0]] = (
            azul, verde, rojo)
        return imagen

    def desplazar_imagen(self, cantidad=0, horizontal=True):
        if horizontal == True:
            self.desplazado_x += cantidad
        else:
            self.desplazado_y += cantidad
        M = np.float32([[1, 0, self.desplazado_x], [0, 1, self.desplazado_y]])
        imagen = cv2.warpAffine(self.imagen, M, (self.ancho_o, self.alto_o))
        return imagen

    def copiar_pegar_imagen(self):
        try:
            imagen = copy.deepcopy(self.imagen)
            region, cordenadas = self.selecionar_region()
            x, y = self.selecionar_punto()
            imagen[0 + y:region.shape[0] + y, 0 + x:region.shape[1] + x] = region
            return imagen
        except:
            sg.popup_error("No se puede pegar esta imagen aqui", no_titlebar=True, keep_on_top=True)
            return self.imagen

    def rotar_imagen(self, grados=0):
        M = cv2.getRotationMatrix2D(self.centro, grados, 1)
        imagen = cv2.warpAffine(self.imagen, M, (self.ancho_o, self.alto_o))
        return imagen

    def espejo_imagen(self):
        imagen = cv2.flip(self.imagen, 1)
        return imagen

    def transformacion_logaritmica(self, c):
        np.seterr(divide='ignore')
        imagen = (c * np.log(1 + self.imagen)).astype(int)
        cv2.imwrite("../../Python/PruebaGUI/test.png", imagen)
        imagen = cv2.imread("../../Python/PruebaGUI/test.png")
        return imagen

    def transformación_potencia(self, c=0):
        imagen = (c * np.power(self.imagen, math.e)).astype(int)
        cv2.imwrite("../../Python/PruebaGUI/test.png", imagen)
        imagen = cv2.imread("../../Python/PruebaGUI/test.png")
        return imagen

    def brillo_imagen(self, beta=0):
        imagen = copy.deepcopy(self.imagen)
        imagen[imagen < 255 - beta] += beta
        cv2.imwrite("../../Python/PruebaGUI/test.png", imagen)
        imagen = cv2.imread("../../Python/PruebaGUI/test.png")
        return imagen

    def contraste(self, gamma=0, beta=0):
        imagen = (gamma * self.imagen) + beta
        cv2.imwrite("../../Python/PruebaGUI/test.png", imagen)
        imagen = cv2.imread("../../Python/PruebaGUI/test.png")
        return imagen

    def stretch(self):
        imagen = ((self.imagen - self.pixelmin) / (self.pixelmax - self.pixelmin)) * 255
        cv2.imwrite("../../Python/PruebaGUI/test.png", imagen)
        imagen = cv2.imread("../../Python/PruebaGUI/test.png")
        return imagen

    def shrink(self, shrink_min=0, shrink_max=0):
        imagen = ((shrink_max - shrink_min) / (self.pixelmax - self.pixelmin)) * (
                self.imagen - self.pixelmin) + shrink_min
        cv2.imwrite("../../Python/PruebaGUI/test.png", imagen)
        imagen = cv2.imread("../../Python/PruebaGUI/test.png")
        return imagen

    def slide(self, offset=0):
        imagen = self.imagen + offset
        cv2.imwrite("../../Python/PruebaGUI/test.png", imagen)
        imagen = cv2.imread("../../Python/PruebaGUI/test.png")
        return imagen

    def ecualizacion(self):
        imagen = cv2.equalizeHist(self.imagen)
        cv2.imwrite("../../Python/PruebaGUI/test.png", imagen)
        imagen = cv2.imread("../../Python/PruebaGUI/test.png")
        return imagen

    def thersholding(self, min):
        ret, imagen = cv2.threshold(self.imagen, min, 255, cv2.THRESH_BINARY)
        cv2.imwrite("../../Python/PruebaGUI/test.png", imagen)
        imagen = cv2.imread("../../Python/PruebaGUI/test.png")
        return imagen
