from PySimpleGUI import Text, Image, FileBrowse, Frame, Column, VSep, Button, HSep, Push, VPush, Table, Input, \
    FileSaveAs, Spin, Radio, Slider, TabGroup, Tab
import PySimpleGUI as sg


def window_principal():
    sg.theme('DarkGrey4')

    tipos_archivos_abrir = [("Archivos de imagen", "*.jpg *.jpeg *.jpe *.jp2 *.png *.bmp *.dib *.tiff *.tif *.webp "
                                                   "*.pbm *.pgm *.ppm *.pxm *.pnm *.pfm *.hdr *.pic *.exr *.sr *.ras"),
                            ("Todos los Archivos", "*.*")]

    tipos_archivos_guardar = [("Archivo JPG", "*.jpg")]

    tabla_datos_columnas = ['Proceso', 'Descripcion']

    # -------------------------------------------------------------------------------------------------------------------

    def columna_general(columna, expand_y=True, expand_x=True):
        columna = Column(columna, expand_y=expand_y, expand_x=expand_x, element_justification="c")
        return columna

    size = (20, 2)

    def boton_general(texto="", llave=""):
        boton = Button(button_text=texto, key=llave, enable_events=True, size=size)
        return boton

    def frame_general(texto="", layout=[]):
        frame = Frame(title=texto, layout=layout, expand_y=True)
        return frame

    def tab_general(texto="", layout=[], llave="", visible=False):
        tab = Tab(title=texto, layout=layout, key=llave, expand_y=True, visible=visible)
        return tab

    def slider_general(rango=(0, 100), llave="", orientacion="h",inicial=0,incremento=1):
        slider = Slider(range=rango, key=llave, orientation=orientacion,default_value=inicial,resolution=0.01)
        return slider

    def text_general(texto="", ):
        texto = Text(text=texto)
        return texto

    def tab_group_general(layout=[]):
        tab_group = TabGroup(layout=layout, expand_y=True)
        return tab_group

    def imagen_general(llave=""):
        imagen = Image(key=llave, size=(400, 300))
        return imagen

    def tabla_general(llave=""):
        tabla = Table(values=[], headings=tabla_datos_columnas, expand_x=True, key=llave, justification="l",
                      col_widths=[15, 45], auto_size_columns=False)
        return tabla

    def file_browse_general(texto="", llave=""):
        browse = FileBrowse(button_text=texto, file_types=tipos_archivos_abrir, key=llave, enable_events=True,
                            size=size)
        return browse

    def file_save_as_general(texto="", llave=""):
        save_as = FileSaveAs(button_text=texto, key=llave, enable_events=True,
                             file_types=tipos_archivos_guardar, size=size)
        return save_as

    def input_general(llave=""):
        input = Input(key=llave)
        return input

    def spin_general(llave=""):
        spin = Spin(values=[], key=llave)
        return spin

    # -------------------------------------------------------------------------------------------------------------------

    columna_imagen = [[VPush()], [imagen_general("-VER_IMAGEN-")], [VPush()]]
    columna_histograma = [[VPush()], [imagen_general("-VER_HISTOGRAMA-")], [VPush()]]
    columna_botones = [
        [file_browse_general("Abrir", "-ABRIR_ARCHIVO-")],
        [boton_general("Guardar", "-GUARDAR_ARCHIVO-")],
        [file_save_as_general("Guardar Como", "-GUARDAR_ARCHIVO_COMO-")],
        [boton_general("Generar Imagen", "-GENERAR_IMAGEN-")]
    ]

    columna_procesos = [
        [tabla_general("-TABLA_PROCESOS-")],
        [boton_general("Ejecutar Proceso", "-EJECUTAR_PROCESO-")]
    ]

    columna_propiedades = [
        [tab_group_general([
            [tab_general('Datos', [
                [frame_general("Informacion:", [
                    [text_general("Ruta:"), input_general("-RUTA-")],
                    [text_general("Resolucion:"), spin_general("-ANCHO_P-"), text_general("Ancho"),
                     spin_general("-ALTO_P-"), text_general("Alto")]
                ])]
            ]),

             tab_general("Propiedades", [
                 [frame_general("Color:", [
                     [text_general("Rojo"), Push(), text_general("(R)"), slider_general((0, 255), "-ROJO-")],
                     [text_general("Verde"), Push(), text_general("(G)"), slider_general((0, 255), "-VERDE-")],
                     [text_general("Azul"), Push(), text_general("(B)"), slider_general((0, 255), "-AZUL-")],
                     [boton_general("Aplicar", "-APLICAR_COLOR-")]
                 ])]
             ], "-PROPIEDADES_COLOR-"),

             tab_general("Propiedades", [
                 [frame_general("Desplazar:", [
                     [slider_general((0, 100), "-PIXELES-",incremento=1)],
                     [boton_general("▲", "-APLICAR_ARRIBA-")],
                     [boton_general("◀", "-APLICAR_IZQUIERDA-"),
                      boton_general("▶", "-APLICAR_DERECHA-")],
                     [boton_general("▼", "-APLICAR_ABAJO-")]
                 ])]
             ], "-PROPIEDADES_DESPLAZAR-"),

             tab_general("Propiedades", [
                 [frame_general("Rotar:", [
                     [slider_general((0, 360), "-GRADOS-",incremento=1)],
                     [boton_general("Aplicar", "-APLICAR_ROTAR-")]
                 ])]
             ], "-PROPIEDADES_ROTAR-"),

             tab_general("Propiedades", [
                 [frame_general("Transformacion logaritmica:", [
                     [slider_general((0, 50), "-CONSTANTE_LOG-")],
                     [boton_general("Aplicar", "-APLICAR_LOG-")]
                 ])]
             ], "-PROPIEDADES_LOG-"),

             tab_general("Propiedades", [
                 [frame_general("Transformacion potencia:", [
                     [slider_general((0, 0.1), "-CONSTANTE_POT-",incremento=0.01)],
                     [boton_general("Aplicar", "-APLICAR_POT-")]
                 ])]
             ], "-PROPIEDADES_POT-"),

             tab_general("Propiedades", [
                 [frame_general("Brillo:", [
                     [slider_general((0, 100), "-CONSTANTE_BRILLO-")],
                     [boton_general("Aplicar", "-APLICAR_BRILLO-")]
                 ])]
             ], "-PROPIEDADES_BRILLO-"),

             tab_general("Propiedades", [
                 [frame_general("Contraste:", [
                     [slider_general((0, 100), "-CONSTANTE_CONTRASTE-")],
                     [slider_general((1, 2), "-CONSTANTE_CONTRASTE2-")],
                     [boton_general("Aplicar", "-APLICAR_CONTRASTE-")]
                 ])]
             ], "-PROPIEDADES_CONTRASTE-"),

             tab_general("Propiedades", [
                 [frame_general("Shrink:", [
                     [slider_general((0, 255), "-CONSTANTE_SHRINK-")],
                     [slider_general((0, 255), "-CONSTANTE_SHRINK2-",inicial=255)],
                     [boton_general("Aplicar", "-APLICAR_SHRINK-")]
                 ])]
             ], "-PROPIEDADES_SHRINK-"),

             tab_general("Propiedades", [
                 [frame_general("Slide:", [
                     [slider_general(((-255), 255), "-CONSTANTE_SLIDE-")],
                     [boton_general("Aplicar", "-APLICAR_SLIDE-")]
                 ])]
             ], "-PROPIEDADES_SLIDE-"),

             tab_general("Propiedades", [
                 [frame_general("Thersholding:", [
                     [slider_general((0, 255), "-CONSTANTE_THERSHOLDING-")],
                     [boton_general("Aplicar", "-APLICAR_THERSHOLDING-")]
                 ])]
             ], "-PROPIEDADES_THERSHOLDING-"),
             ]],
        )]
    ]

    layout = [
        [VPush()],
        [columna_general(columna_imagen), VSep(), columna_general(columna_histograma)],
        [VPush()],
        [HSep()],
        [VPush()],
        [columna_general(columna_botones), VSep(), columna_general(columna_procesos), VSep(),
         columna_general(columna_propiedades)],
        [VPush()]
    ]
    window = sg.Window('Procesamineto Imagenes', layout, resizable=True, finalize=True)
    window.Maximize()
    return window


def window_vista_requisito():
    layout = [[Text("Ingresa la resolucion de la imagen")],
              [Text("Ancho"), Spin([i for i in range(1, 5000)], key="-ANCHO-", size=(20, 1)), Text("Alto"),
               Spin([i for i in range(1, 5000)], key="-ALTO-", size=(20, 1))],
              [Button('Ok', key="-OK-", enable_events=True)]
              ]

    return sg.Window('Generar Imagen', layout)


def datos_tabla():
    tabla_datos = [("Region Zoom", "Seleciona una region para hacer zoom"),
                   ("Pixelear Rostro", "Seleciona uno o varios rostros para pixelear"),
                   ("Limpieza", "Seleciona una region para cambiar todos los pixeles a un valor fijo"),
                   ("Copia", "Seleciona una region para copiar y lo pegas en un lugar espesifico"),
                   ("Inversión", "Invierte las escalas de color"),
                   ("Desplazamiento", "Desplaza la imagen completa"),
                   ("Rotacion", "Rota la imagen completa"),
                   ("Espejo", "Procesa la imagen en modo espejo"),
                   ("Transformacion Logarítmica", "Transforma la imagen de niveles de gris"),
                   ("Transformación potencia", "Transforma la imagen de niveles de gris"),
                   ("brillo", "Aumenta el brillo de la imagen"),
                   ("contraste", "Aumento de contraste"),
                   ("Stretch", "Modifica el histograma con el metodo expansión lineal"),
                   ("Shrink", "Modifica el histograma con el metodo compresión"),
                   ("Slide", "Modifica el histograma con el metodo desplazamiento"),
                   ("Ecualización", "Busca producir una imagen con un histograma uniforme"),
                   ("Thersholding", "Es el método mas simple de segmentación")
                   ]
    return tabla_datos
