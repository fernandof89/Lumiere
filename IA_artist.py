import funciones_auxiliares
import random
import time
import datetime
import numpy as np
import cv2 as cv
import cv2 as cv_i
from deepface import DeepFace
import os
import sys
import keyboard
import tkinter as tk
import pyautogui as key
from tkinter import messagebox, ttk

def sel_idioma():
    # Obtener la opción seleccionada.
    selection = combo.get()
    # cerrando ventanas de seleccion de idioma
    main_window.destroy()
    #apuntando a las variables de texto
    global info1_lbl
    global info1
    global no_cam
    global no_vid
    global root_title
    global root_title1
    global opc1
    global opc2
    global opc3
    global opc4
    global opc5

    if selection == "Español":
        # textos en español
        info1_lbl= "Información"
        info1 = (
                    "Luego de haber minimizado todas las ventanas, Ud. verá una serie de imágenes, cada vez que cambie la imagen, por favor, háganos saber su reacción mediante el uso del siguiente menú:" + os.linesep + os.linesep
                    + "Tecla UP: Le gusta la imagen \n"
                    + "Tecla DOWN: No le gusta la imagen \n"
                    + "Tecla FLECHA IZQ: Ni le gusta ni le disgusta la imagen \n"
                    + "Tecla FLECHA DER: No le interesa la imagen \n"
                    + "Tecla ESC: Salir del programa \n")
        no_cam = "No se puede acceder a la cámara"
        no_vid = "No se recibe video. Saliendo..."
        root_title = "Escoja una reacción"
        root_title1 = "Opción escogida"
        opc1 = "Le gusta la imagen"
        opc2 = "No le gusta la imagen"
        opc3 = "Ni le gusta ni le disgusta la imagen"
        opc4 = "No le interesa la imagen"
        opc5 = "Saliendo del programa"
        funciones_auxiliares.cambiar_idioma(False)

    else:
        #Textos en inglés
        info1_lbl = "Information"
        info1 = (
                "After minimizing all windows, you will see a set of images, every time the image changes, please, let us know your reaction to the new image, by using the following menu:" + os.linesep + os.linesep
                + "UP Key: You like the image \n"
                + "DOWN Key: You don´t like the image \n"
                + "LEFT Key: You don´t like nor dislike the image \n"
                + "RIGHT Key: You don´t care about the image \n"
                + "ESC Key: Exit the program \n")
        no_cam = "Camera can not be accessed"
        no_vid = "Not video signal. Exiting..."
        root_title = "Please, choose a reaction"
        root_title1 = "Option selected"
        opc1 = "You like the image"
        opc2 = "You don´t like the image"
        opc3 = "You don´t like nor dislike the image"
        opc4 = "You don´t care about the image"
        opc5 = "Exit the program"
        funciones_auxiliares.cambiar_idioma(True)

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

# obteniendo directorio actual y creando carpeta con log
ruta = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# la nueva carpeta llevara un random para que si se ejecuta varias veces el programa, no se pisen las carpetas
identificador = str(random.randint(0,10000000))

#creo la carpeta en la ubicación donde se ejecuta el programa
directorio = os.path.join(ruta, "NuevaCarpeta" + identificador)
os.mkdir(directorio)

#creo el log
archivo= os.path.join(directorio, "Resultados"+ identificador+".txt")
log_datos = open (archivo,"w")
log_datos.write("timestamp,emotion,OPI_type,reaction_type,react_time,tipo_imagen \n")

#se minimizan todas las ventanas
key.hotkey('win','d')

#seleccionando idioma de visualización
main_window = tk.Tk()
main_window.config(width=500, height=200)
main_window.title("Idioma/Language")
main_window.eval('tk::PlaceWindow . center')
combo = ttk.Combobox(
    state="readonly",
    values=["Español", "English"]
)
combo.place(x=50, y=50)
combo.current(0)
button = ttk.Button(text="OK", command=sel_idioma)
button.place(x=50, y=100)
main_window.mainloop()

#mostrando mensaje informativo
key.alert(info1, info1_lbl)

while (1):  # esto se repite cada 40s
    # guardo imagen_vieja para hacer transicion con la nueva imagen
    imagen_vieja = imagen_actual

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print(no_cam)
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # si frame is read correctly ret is True
        if not ret:
            print(no_vid)
            break

        # sistema difuso obtiene el estado de animo actual del observador
        resultFace = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        info = [[resultFace[0]['dominant_emotion']]]
        emocion = str(info[0])
        # sistema asimila el estado del animo del observador cambiando ESTADO DE ANIMO DEL SISTEMA
        if info == [['neutral']]:
            estado_animo_sistema = 0
            break
        if info == [['happy']]:
            estado_animo_sistema = 1
            break
        if info == [['sad']]:
            estado_animo_sistema = 2
            break
        if info == [['surprise']]:
            estado_animo_sistema = 3
            break
        if info == [['angry']]:
            estado_animo_sistema = 4
            break
        if info == [['fear']]:
            estado_animo_sistema = 5
            break

    # When everything done, release the capture
    cap.release()

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
        pincel = "funciones_auxiliares." + OPI + "(" + str(dir_frame) + ")"

    #aplico pincel a la imagen seleccionada
    imagen_actual = eval(pincel)

    # convirtiendo ambas imagenes a numpy arrays
    imagen_vieja = np.asarray(imagen_vieja)
    imagen_actual = np.asarray(imagen_actual)

    # cambio tamaño imagenes para cambiar tamaño ventana
    imagen_vieja = cv_i.resize(imagen_vieja, dsize=(height, width), interpolation=cv_i.INTER_CUBIC)
    imagen_actual = cv_i.resize(imagen_actual, dsize=(height, width), interpolation=cv_i.INTER_CUBIC)

    # haciendo la transición entre las dos imágenes (demora 0,1 seg = 1000 x 0.0001)
    cv_i.namedWindow("Pintura", cv_i.WINDOW_NORMAL)
    cv_i.setWindowProperty("Pintura", cv_i.WND_PROP_FULLSCREEN, cv_i.WINDOW_FULLSCREEN)
    for alpha in np.linspace(0, 1, 1000):
        beta = 1 - alpha
        pintura = cv_i.addWeighted(imagen_actual, alpha, imagen_vieja, beta, 0)
        cv_i.imshow("Pintura", pintura)
        time.sleep(0.0001)
        if cv_i.waitKey(1) == 27:
            break

    #avisando que puede escoger reaccion
    root = tk.Tk()
    root.title(root_title)
    root['bg'] = 'grey'
    root.overrideredirect()
    root.attributes('-transparentcolor', 'grey')

    canvas_width = 90
    canvas_height = 90

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='grey')
    canvas.pack()

    # Calculate the position of the root window
    x = root.winfo_screenwidth() - canvas_width - int(0.038*root.winfo_screenheight())
    # y = root.winfo_screenheight() - canvas_height - 50
    y = root.winfo_screenheight() - canvas_height - int(0.038*root.winfo_screenheight())
    # Position the root window in the bottom right corner of the screen
    root.geometry(f"+{x}+{y}")

    # Calculate the center coordinates of the canvas
    center_x = canvas_width / 2
    center_y = canvas_height / 2

    # Set the radius of the circle
    radius = 40

    # Calculate the coordinates of the bounding box of the circle
    left = center_x - radius
    top = center_y - radius
    right = center_x + radius
    bottom = center_y + radius

    # Draw the circle using create_oval method
    canvas.create_oval(left, top, right, bottom, fill="red")
    root.after(5000, lambda: root.destroy())  # time in ms
    root.mainloop()

    #
    tecla_presionada = False
    tiempo=datetime.datetime.now().isoformat(timespec='microseconds')    #tomo el tiempo que sirve como identificador de la fila y además para calcular el tiempo de reacción
    #espero para capturar la tecla presionada
    while True:
        tecla_presionada = keyboard.read_key()
        if tecla_presionada != False:
            # asignando la opción segun la tecla
            if (tecla_presionada=='flecha arriba'):
                opcion = opc1
            elif (tecla_presionada=='flecha abajo'):
                opcion = opc2
            elif (tecla_presionada=='flecha derecha'):
                opcion = opc3
            elif (tecla_presionada=='flecha izquierda'):
                opcion = opc4
            elif (tecla_presionada=='esc'):
                opcion = opc5
            else:
                opcion = tecla_presionada
        # tomo datos y guardo en el log
        react_time = datetime.datetime.now().isoformat(timespec='microseconds')
        log_datos.write(tiempo + "," + emocion + "," + OPI + "," + opcion + "," + react_time + "," + str(des)+"\n")

        # mostrando la opción escogida
        root = tk.Tk()
        root.geometry("500x50")
        root.title(root_title1)
        tk.Label(root, text=opcion).pack()
        root.eval('tk::PlaceWindow . center')
        root.after(3000, lambda: root.destroy())  # time in ms
        root.mainloop()

        #comprobando si se quiere salir del programa
        if tecla_presionada == "esc":
            salir = True
        break # hay una tecla oprimida, salgo de este ciclo que hace esperar una tecla

    if salir:   #si se oprimio la tecla Esc, salgo de la ejecución del ciclo
        break

    # con estos 29s de demora se cumplen los 40s de muestreo
    time.sleep(29)  #ACTIVAR TEMPORIZADOR

log_datos.close()
#llamo a funcion para enviar el archivo
funciones_auxiliares.sending_mail(archivo, identificador, directorio)




