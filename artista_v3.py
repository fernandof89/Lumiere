import tkinter

import funciones_auxiliares
import random
import time
import datetime
import numpy as np
import cv2 as cv
import cv2 as cv_i
from deepface import DeepFace
from PIL import Image
import os
import keyboard
from tkinter import messagebox
import tkinter as tk

# matriz dinámica de asociación de OPIS con estado de ánimo
# la primera fila es la cabecera y son los estados de ánimos del sistema (números)
# las filas siguientes son las opis que corresponden (numero-letras), una columna serían todas las OPIS asociadas al estado de ánimo de la primera fila de esa columna
asociacion = np.array([[1, 2, 3, 4, 5],
                       ["fusiona_2_img", "fusiona_varias_imgs", "musica_amplitud_a_color", "func_cos_a_pix",
                        "func_log_a_pix"],
                       ["func_sin_a_pix", "hebb_RGB_ind", "hebb_RGB_per_pixel", "recorta_nxm_flipH",
                        "recorta_nxm_flipV"],
                       ["figura_collage", "difuminado_gaussiano_random", "difuminado_gaussiano_full", "apagado_pixel",
                        "efecto_zoom"]])

# inicializo las variables
height = 640
width = 640
imagen_actual = np.zeros((height, width, 3), np.uint8)
imagen_vieja = imagen_actual
pincel = 0
emocion = "neutral"
opcion = ""
salir = False
tecla_presionada = False

messagebox.showinfo("Información", "A continuación verá una serie de imágenes, cada vez que cambie la imagen, por favor, háganos saber su reacción mediante el uso del siguiente menú:" + os.linesep+ os.linesep
                    + "Tecla UP: Le gusta la imagen"+ os.linesep+ os.linesep
                    + "Tecla DOWN: No le gusta la imagen"+ os.linesep+ os.linesep
                    + "Tecla UP: Ni le gusta ni le disgusta la imagen"+ os.linesep+ os.linesep
                    + "Tecla UP: No le interesa la imagen"+ os.linesep+ os.linesep
                    + "Tecla ESC: Salir del programa")

# obteniendo directorio actual y creando carpeta con log
separador = os.path.sep   #da el separador del sistema, / para Linux, \ para Windows
ruta = os.path.dirname(os.path.abspath(__file__))
# la nueva carpeta llevara un random para que si se ejecuta varias veces el programa, no se pisen las carpetas
identificador = str(random.randint(0,10000000))
os.mkdir("NuevaCarpeta" + identificador)
#creo el log
log_datos = open (ruta+separador+"NuevaCarpeta"+ identificador+separador+"log"+ identificador+".txt","w")
log_datos.write("timestamp,emotion,OPI_type,reaction_type,react_time,tipo_imagen"+os.linesep)
# esto se repite cada 40s
while (1):
    # guardo imagen_vieja para hacer transicion con la nueva imagen
    imagen_vieja = imagen_actual

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("No se puede acceder a la cámara")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # si frame is read correctly ret is True
        if not ret:
            print("No se recibe video. Saliendo...")
            break

        # sistema difuso selecciona el estado de animo actual del observador
        resultFace = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        info = [[resultFace[0]['dominant_emotion']]]
        emocion = str(info[0])
        # sistema asimila el estado del animo del observador cambiando ESTADO DE ANIMO DEL SISTEMA
        if info == [['neutral']]:
            # When b is pressed videoChange is 1
            estado_animo_sistema = 0
            break
        if info == [['happy']]:
            # When b is pressed videoChange is 1
            style_name = "yellow"
            estado_animo_sistema = 1
            break
        if info == [['sad']]:
            # When b is pressed videoChange is 1
            style_name = "blue"
            estado_animo_sistema = 2
            break
        if info == [['surprise']]:
            # When b is pressed videoChange is 1
            style_name = "white"
            estado_animo_sistema = 3
            break
        if info == [['angry']]:
            # When b is pressed videoChange is 1
            style_name = "red"
            estado_animo_sistema = 4
            break
        if info == [['fear']]:
            # When b is pressed videoChange is 1
            style_name = "black"
            estado_animo_sistema = 5
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
    # elijo al azar una posición de columna
    ind1 = random.randint(1, 3)
    # abro la OPI correspondiente a esa columna y estado de ánimo
    OPI = asociacion[ind1][estado_animo_sistema - 1]

    # aqui el sistema decide si hace la obra de arte sobre una imagen o aplica un pincel al rostro de quien se analiza
    des = random.randint(0, 1)
    if (des == 0):  # si es cero, se aplica sobre una imagen
        pincel = "funciones_auxiliares." + OPI + "(111)"
    else:  # obtengo dirección de memoria para pasarla como cadena en la funcion
        dir_frame = id(frame)
        # pincel = "funciones_auxiliares.musica_amplitud_a_color(" + str(dir_frame) + ")"
        pincel = "funciones_auxiliares." + OPI + "(" + str(dir_frame) + ")"
    #aplico pincel a la imagen seleccionada
    imagen_actual = eval(pincel)
    #imagen_actual.show()
    # convirtiendo ambas imagenes a numpy arrays
    imagen_vieja = np.asarray(imagen_vieja)
    #cv_i.imshow("Vieja", imagen_vieja)
    imagen_actual = np.asarray(imagen_actual)
    #cv_i.imshow("Actual", imagen_actual)
    # cambio tamaño imagenes para cambiar tamaño ventana
    imagen_vieja = cv_i.resize(imagen_vieja, dsize=(height, width), interpolation=cv_i.INTER_CUBIC)
    imagen_actual = cv_i.resize(imagen_actual, dsize=(height, width), interpolation=cv_i.INTER_CUBIC)

    # haciendo la transición entre las dos imágenes (demora 0,1 seg = 1000 x 0.0001)
    for alpha in np.linspace(0, 1, 1000):
        beta = 1 - alpha
        pintura = cv_i.addWeighted(imagen_actual, alpha, imagen_vieja, beta, 0)
        cv_i.imshow('Pintura', pintura)
        time.sleep(0.0001)
        if cv_i.waitKey(1) == 27:
            break

    tecla_presionada = False
    tiempo=datetime.datetime.now().isoformat(timespec='microseconds')    #tomo el tiempo que sirve como identificador de la fila y además para calcular el tiempo de reacción
    #espero para capturar la tecla presionada
    while True:
        tecla_presionada = keyboard.read_key()
        if tecla_presionada != False:
            # asignando la opción segun la tecla
            if (tecla_presionada=='flecha arriba'):
                opcion = "Le gusta la imagen"
            elif (tecla_presionada=='flecha abajo'):
                opcion = "No le gusta la imagen"
            elif (tecla_presionada=='flecha derecha'):
                opcion = "Ni le gusta ni le disgusta la imagen"
            elif (tecla_presionada=='flecha izquierda'):
                opcion = "No le interesa la imagen"
            elif (tecla_presionada=='esc'):
                opcion = "Saliendo del programa"
            else:
                opcion = tecla_presionada
        # tomo datos y guardo en el log
        react_time = datetime.datetime.now().isoformat(timespec='microseconds')
        log_datos.write(tiempo + "," + emocion + "," + OPI + "," + opcion + "," + react_time + "," + str(des)+os.linesep)
        # mostrando la opción escogida
        root = tk.Tk()
        root.title("Opción escogida")
        tk.Label(root, text=opcion).pack()
        root.geometry("500x50")
        root.after(5000, lambda: root.destroy())  # time in ms
        root.mainloop()
        #comprobando si se quiere salir del programa
        if tecla_presionada == "esc":
            salir = True
        break # hay una tecla oprimida, salgo de este ciclo que hace esperar una tecla

    # con estos 29s de demora se cumplen los 40s de muestreo
    #time.sleep(9)  #ACTIVAR TEMPORIZADOR

    if salir:   #si se oprimio la tecla Esc, salgo de la ejecución del ciclo
        break
log_datos.close()
