import random
import time

import librosa
import math
import pyautogui as key
from PIL import Image, ImageOps, ImageFilter
import ctypes
import numpy as np
import os
import sys
import smtplib
from smtplib import *
from email.message import EmailMessage
import clipboard as c


def cambiar_idioma(opc):
    global msg_txt_1
    global msg_txt_2
    global msg_txt_3
    global msg_txt_4

    if opc == False:
        msg_txt_1 = ("Cuando acepte este mensaje, se abrirá una ventana, por favor, envienos el archivo Resultados")
        msg_txt_2 = (".txt que se encuentra ahí a la siguiente dirección de correo: lumiereproyect@gmail.com" + "\n" + "(También se ha copiado al portapapeles la dirección de correo)" +
                     "\n" + "Por favor, tenga en cuenta que dispone de 1 minuto para envir el archivo o copiarlo en otra ruta antes que sea eliminado")
        msg_txt_3 = ("Gracias!")
        msg_txt_4 = ("Ruta donde se encuentra el archivo")
    else:
        msg_txt_1 = ("When you accept this message, a new window will be opened, please, send us the file Resultados")
        msg_txt_2 = (".txt located there to the following email address: lumiereproyect@gmail.com" + "\n" + "(The email address has also been copied to the clipboard)"+
                     "\n" + "Please, be aware that you have 1 minute to send the file or to copy the file to another path before the log is deleted")
        msg_txt_3 = ("Thanks!")
        msg_txt_4 = ("Path where is located the log file")

def sending_mail(ruta, id, dir):

    msg = EmailMessage()

    my_address = "lumiereproyect@gmail.com"  # sender address

    app_generated_password = "vxugqorxdalgykzg"  # gmail generated password

    msg["Subject"] = "Resultados simulación"  # email subject

    msg["From"] = my_address  # sender address

    msg["To"] = my_address  # reciver address

    msg.set_content("Resultados simulación \n" + ruta)  # message body

    with open(ruta, 'rb') as f:
        file_data = f.read()
    msg.add_attachment(file_data, maintype='text', subtype='plain', filename = "Resultados"+id)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(my_address, app_generated_password)
            server.send_message(msg)
    except Exception as err:
        error = err
        tipo_err = type(err)
        key.alert(msg_txt_1 + id + msg_txt_2 + os.linesep + msg_txt_3,
                  msg_txt_4)
        # copio la direccion de correo al portapapeles
        c.copy("lumiereproyect@gmail.com")
        # abro la ventana donde está el archivo
        os.startfile(dir)
        #demoro la ejecucion un minuto para que pueda copiar
        time.sleep(60)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def trae_imagen():
    # cadena que almacena las imágenes
    nombre_imagenes = ["ondas.jpg", "mountain.jpg", "fuego.jpg", "lamparas.jpg", "nubes.jpg", "skyline.jpg",
                       "globos.jpg", "tiger-jpg.jpg", "field-jpg.jpg", "bosque.jpg", "girasol.jpg", "cielo.jpg"]
    # cargo aleatoriamente la imagen de base"
    ind1 = random.randint(0, len(nombre_imagenes) - 1)
    imagen1 = Image.open(os.path.join(resource_path("img"), nombre_imagenes[ind1]))
    return imagen1

def iguala_dim_imgs(imagen1, imagen2):
    # sacando mayor ancho
    if (imagen1.size[0] < imagen2.size[0]):
        ancho_min = imagen1.size[0]
    else:
        ancho_min = imagen2.size[0]

        # sacando mayor altura
    if (imagen1.size[1] < imagen2.size[1]):
        altura_min = imagen1.size[1]
    else:
        altura_min = imagen2.size[1]

    img_mod1 = ImageOps.fit(imagen1, (ancho_min, altura_min))
    img_mod2 = ImageOps.fit(imagen2, (ancho_min, altura_min))

    return img_mod1, img_mod2


def fusiona_2_img(par):

    if par==111:  #es una imagen de la base de datos
        imagen1 = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen1 = Image.fromarray(frame)

    imagen2 = trae_imagen()

    # llamo a funcion para igualar dimensiones imagenes
    imagen1, imagen2 = iguala_dim_imgs(imagen1, imagen2)

    # Do an alpha composite of image4 over image3
    Blend = Image.blend(imagen1, imagen2, 0.5)

    # Display the alpha composited image
    return Blend


def fusiona_varias_imgs(par):
    # cantidad de imágenes a mezclar
    ctdad_img = 4

    if par==111:  #es una imagen de la base de datos
        imagen1 = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen1 = Image.fromarray(frame)

    # establezco ancho y altura mínimos"
    ancho_min = imagen1.size[0]
    altura_min = imagen1.size[1]

    # escogiendo i-1 random imagenes"
    for i in range(0, ctdad_img - 1):
        imagen_i = trae_imagen()
        # saco las dimensiones"
        ancho_i = imagen_i.size[0]
        altura_i = imagen_i.size[1]
        # busco la menor dimensión"
        if (ancho_i < ancho_min):
            ancho_min = ancho_i
        if (altura_i < altura_min):
            altura_min = altura_i
        # igualando los tamaños de las imágenes
        imagen1 = imagen1.resize((ancho_min, altura_min))
        imagen_i = imagen_i.resize((ancho_min, altura_min))
        # Haciendo el Blend
        img_blend = Image.blend(imagen1, imagen_i, 0.5)
        # guardo el blend en imagen1, para reutilizarlo en caso de ser necesario
        imagen1 = img_blend
        # mostrando el blend
    return imagen1


def musica_amplitud_a_color(par):
    # Paquetes necesarios para la exploración de datos
    audio = os.path.join(resource_path("sound"),'la-vida-es-un-carnaval-ringtones-.mp3')

    # decodifica el archivo de audio en un arreglo unidimensional y, sample_rates guarda la frecuencia de muestreo
    y, sampling_rate = librosa.load(audio)

    T = y.size / sampling_rate  # tiempo total audio
    dt = 1 / sampling_rate  # diferencial de tiempo
    t = np.r_[0:T:dt]  # arreglo numpy que de 0 a T en intervalos dt

    X = librosa.stft(y)
    X_dB = librosa.amplitude_to_db(np.abs(X))

    dim_DB = X_dB.size

    if par==111:  #es una imagen de la base de datos
        im = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        im = Image.fromarray(frame)

    im_modif = im.copy()  # imagen que se modificará

    # calculando cantidad total de pixeles
    ctdad_pixeles = im.size[0] * im.size[1]

    if (dim_DB > ctdad_pixeles): # hay más muestras que pixeles

        #a cada pixel le corresponde una muestra (sobraran muestras).
        #de ese pixel, el color rojo será la primera muestra de ese rango, el color verde sera la muestra del medio y el color azul la última muestra de ese rango

        for i in range(0, im.size[0] - 3):
            for j in range(0, im.size[1] - 3):
                # asigno valores de pixeles
                rojo = X_dB[i, j]
                verde = X_dB[i, j] + 1
                azul = X_dB[i, j] + 2

                rojo = int(rojo)
                verde = int(verde)
                azul = int(azul)
                pix = im.getpixel((i, j))
                rojo = rojo + pix[0]
                verde = verde + pix[1]
                azul = azul + pix[2]

                im_modif.putpixel((i, j), (rojo, verde, azul))
    else:   #hay más pixeles que muestras
            #se cambian pixeles hasta que terminen las muestras de audio
        for i in range(0, X_dB.size[0] - 3):
            for j in range(0, X_dB.size[1] - 3):
                # asigno valores de pixeles
                rojo = X_dB[i, j]
                verde = X_dB[i, j] + 1
                azul = X_dB[i, j] + 2

                rojo = int(rojo)
                verde = int(verde)
                azul = int(azul)
                pix = im.getpixel((i, j))
                rojo = rojo + pix[0]
                verde = verde + pix[1]
                azul = azul + pix[2]

                im_modif.putpixel((i, j), (rojo, verde, azul))

    return im_modif


def func_cos_a_pix(par):
    # transformacion coseno de una imagen

    if par==111:  #es una imagen de la base de datos
        imagen1 = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen1 = Image.fromarray(frame)

    for i in range(0, imagen1.size[0] - 1):

        for j in range(0, imagen1.size[1] - 1):
            pixel = imagen1.getpixel((i, j))  # Extraigo el pixel
            p_rojo = pixel[0]  # Extraigo valor color rojo
            p_verde = pixel[1]  # Extraigo valor color verde
            p_azul = pixel[2]  # Extraigo valor color azul

            # aplico funcion seno a todos los colores (la función sin usa como argumento el radian y es flotante)
            # convierto a flotante los enteros para pasarlo a la funcion seno
            rojo = float(p_rojo)
            verde = float(p_verde)
            azul = float(p_azul)
            # aplico funcion coseno
            rojo = math.cos(rojo)
            verde = math.cos(verde)
            azul = math.cos(azul)
            # normalizo a 255 y lo hago positivo
            rojo = abs(rojo) * 255
            verde = abs(verde) * 255
            azul = abs(azul) * 255
            # convierto a entero
            rojo = int(rojo)
            verde = int(verde)
            azul = int(azul)

            # Modifico la imagen con el nuevo valor del pixel
            imagen1.putpixel((i, j), (rojo, verde, azul))

    # Muestro la imagen transformada
    return imagen1


def func_log_a_pix(par):
    def logTransform(c, f):
        g = c * math.log(float(1 + f), 10)
        return g

    # Apply logarithmic transformation for an image

    def logTransformImage(image, outputMax=255, inputMax=255):
        c = outputMax / math.log(inputMax + 1, 10)

        # Read pixels and apply logarithmic transformation

        for i in range(0, img.size[0] - 1):

            for j in range(0, img.size[1] - 1):
                # Get pixel value at (x,y) position of the image

                f = img.getpixel((i, j))

                # Do log transformation of the pixel

                redPixel = round(logTransform(c, f[0]))

                greenPixel = round(logTransform(c, f[1]))

                bluePixel = round(logTransform(c, f[2]))

                # Modify the image with the transformed pixel values

                img.putpixel((i, j), (redPixel, greenPixel, bluePixel))

        return image

    # Display the image after applying the logarithmic transformation

    if par==111:  #es una imagen de la base de datos
        img = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        img = Image.fromarray(frame)

    # muestra la imagen
    logTransformedImage = logTransformImage(img)
    return logTransformedImage


def func_sin_a_pix(par):
    # transformacion seno de una imagen
    if par == 111:  # es una imagen de la base de datos
        imagen1 = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen1 = Image.fromarray(frame)

    for i in range(0, imagen1.size[0] - 1):

        for j in range(0, imagen1.size[1] - 1):
            pixel = imagen1.getpixel((i, j))  # Extraigo el pixel
            p_rojo = pixel[0]  # Extraigo valor color rojo
            p_verde = pixel[1]  # Extraigo valor color verde
            p_azul = pixel[2]  # Extraigo valor color azul

            # aplico funcion seno a todos los colores (la función sin usa como argumento el radian y es flotante)
            # convierto a flotante los enteros para pasarlo a la funcion seno
            rojo = float(p_rojo)
            verde = float(p_verde)
            azul = float(p_azul)
            # aplico funcion seno
            rojo = math.sin(rojo)
            verde = math.sin(verde)
            azul = math.sin(azul)
            # normalizo a 255 y lo hago positivo
            rojo = abs(rojo) * 255
            verde = abs(verde) * 255
            azul = abs(azul) * 255
            # convierto a entero
            rojo = int(rojo)
            verde = int(verde)
            azul = int(azul)

            # Modifico la imagen con el nuevo valor del pixel
            imagen1.putpixel((i, j), (rojo, verde, azul))

    # Muestro la imagen transformada
    return imagen1


def hebb_RGB_ind(par):

    if par==111:  #es una imagen de la base de datos
        imagen1 = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen1 = Image.fromarray(frame)

    imagen2 = trae_imagen()

    p_rojo_n = 0
    p_verde_n = 0
    p_azul_n = 0

    # hago iguales las dimensiones
    imagen1, imagen2 = iguala_dim_imgs(imagen1, imagen2)

    # escojo valor random de L entre 0 y 1
    L = random.random()

    # recorro imágenes
    for i in range(0, imagen1.size[0] - 1):
        for j in range(0, imagen1.size[1] - 1):

            pixel_img1 = imagen1.getpixel((i, j))  # Extraigo el pixel (i,j) de la imagen1
            p_rojo_1 = pixel_img1[0]  # Extraigo valor color rojo
            p_verde_1 = pixel_img1[1]  # Extraigo valor color verde
            p_azul_1 = pixel_img1[2]  # Extraigo valor color azul

            D_rojo = random.randint(0, int(p_rojo_1 / 10))
            D_verde = random.randint(0, int(p_verde_1 / 10))
            D_azul = random.randint(0, int(p_azul_1 / 10))

            pixel_img2 = imagen2.getpixel((i, j))  # Extraigo el pixel (i,j) de la imagen2
            p_rojo_2 = pixel_img2[0]  # Extraigo valor color rojo
            p_verde_2 = pixel_img2[1]  # Extraigo valor color verde
            p_azul_2 = pixel_img2[2]  # Extraigo valor color azul

            # detectando "aprendizaje hebbiana", considero cada integrante del color del pixel como una celula, si las dos celulas son iguales se activan simultáneamente con la funcion definida que será la componente de color resultante
            if (p_rojo_1 == p_rojo_2):
                p_rojo_n = p_rojo_1 * L + D_rojo
                # normalizo en caso de ser necesario
                if (p_rojo_n > 255):
                    p_rojo_n = p_rojo_n / 255
            if (p_verde_1 == p_verde_2):
                p_verde_n = p_verde_1 * L + D_verde
                # normalizo en caso de ser necesario
                if (p_verde_n > 255):
                    p_verde_n = p_verde_n / 255
            if (p_azul_1 == p_azul_2):
                p_azul_n = p_azul_1 * L + D_azul
                # normalizo en caso de ser necesario
                if (p_azul_n > 255):
                    p_azul_n = p_azul_n / 255

            # Modifico la imagen con el nuevo valor del pixel
            imagen1.putpixel((i, j), (int(p_rojo_n), int(p_verde_n), int(p_azul_n)))

    # Muestro la imagen transformada
    return imagen1


def hebb_RGB_per_pixel(par):

    if par==111:  #es una imagen de la base de datos
        imagen1 = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen1 = Image.fromarray(frame)

    imagen2 = trae_imagen()

    # hago iguales las dimensiones
    imagen1, imagen2 = iguala_dim_imgs(imagen1, imagen2)

    # escojo valor random de L entre 0 y 1
    L = random.random()

    # recorro imágenes
    for i in range(0, imagen1.size[0] - 1):
        for j in range(0, imagen1.size[1] - 1):

            pixel_img1 = imagen1.getpixel((i, j))  # Extraigo el pixel (i,j) de la imagen1
            dist_pix_1 = (pixel_img1[0] ** 2 + pixel_img1[1] ** 2 + pixel_img1[
                2] ** 2)  # calculo la "distancia al cuadrado" de ese pixel

            pixel_img2 = imagen2.getpixel((i, j))  # Extraigo el pixel (i,j) de la imagen1
            dist_pix_2 = (pixel_img2[0] ** 2 + pixel_img2[1] ** 2 + pixel_img2[
                2] ** 2)  # calculo la "distancia al cuadrado" de ese pixel

            # detectando "activación hebbiana", considero cada distancia de pixel como una celula,
            # si las dos celulas son aprox iguales se activan simultáneamente con la funcion definida que será la componente de color resultante
            if (int(dist_pix_1 / 10) == int(dist_pix_2 / 10)):
                # aqui voy a modificar las distancias con la formula
                D_pix = random.randint(0, int(dist_pix_1 / 10))
                Dist_heb = dist_pix_1 * L + D_pix
                # descompongo esta distancia al cuadrado, escojo una componente de color aleatoria, que será dependiente de la nueva dist  y del promedio por color de los otros dos colores de la primera imagen
                # escojo un color aleatorio
                ind_pix = random.randint(0, 2)
                match ind_pix:
                    case 0:
                        prom_verde = (pixel_img1[1] + pixel_img2[1]) / 2
                        prom_azul = (pixel_img1[2] + pixel_img2[2]) / 2
                        p_rojo_n = math.sqrt(abs(Dist_heb - prom_verde ** 2 - prom_azul ** 2))
                        # Modifico la imagen con el nuevo valor del pixel
                        imagen1.putpixel((i, j), (int(p_rojo_n), int(prom_verde), int(prom_azul)))
                    case 1:
                        prom_rojo = (pixel_img1[0] + pixel_img2[0]) / 2
                        prom_azul = (pixel_img1[2] + pixel_img2[2]) / 2
                        p_verde_n = math.sqrt(abs(Dist_heb - prom_rojo ** 2 - prom_azul ** 2))
                        # Modifico la imagen con el nuevo valor del pixel
                        imagen1.putpixel((i, j), (int(prom_rojo), int(p_verde_n), int(prom_azul)))
                    case 2:
                        prom_verde = (pixel_img1[1] + pixel_img2[1]) / 2
                        prom_rojo = (pixel_img1[0] + pixel_img2[0]) / 2
                        p_azul_n = math.sqrt(abs(Dist_heb - prom_verde ** 2 - prom_rojo ** 2))
                        # Modifico la imagen con el nuevo valor del pixel
                        imagen1.putpixel((i, j), (int(prom_rojo), int(prom_verde), int(p_azul_n)))
            else:
                # intercambio los valores de los pixeles aleatoriamente (así "modifico" un poco más la imagen)
                # tomara el valor del pixel de la derecha, si es el R, el valor de R será el de G, el de G será B y el de B será R
                imagen1.putpixel((i, j), (pixel_img1[1], pixel_img1[2], pixel_img1[0]))
    # Muestro la imagen transformada
    return imagen1


def recorta_nxm_flipH(par):

    if par==111:  #es una imagen de la base de datos
        imagen1 = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen1 = Image.fromarray(frame)

    # sacando el tamaño de la imagen
    ancho, alto = imagen1.size

    # pixeles de seleccion del área
    n = 100
    m = 200

    if n > ancho:
        n = ancho
    if m > alto:
        m = alto

    area = (0, 0, n, m)
    region = imagen1.crop(area)
    img_flip_H = region.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    imagen1.paste(img_flip_H, area)
    return imagen1


def recorta_nxm_flipV(par):

    if par==111:  #es una imagen de la base de datos
        imagen1 = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen1 = Image.fromarray(frame)

    # sacando el tamaño de la imagen
    ancho, alto = imagen1.size

    # pixeles de seleccion del área
    n = 100
    m = 200

    if n > ancho:
        n = ancho
    if m > alto:
        m = alto

    area = (0, 0, n, m)
    region = imagen1.crop(area)
    img_flip_H = region.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    imagen1.paste(img_flip_H, area)
    return imagen1


def figura_collage(par):
    rango_pix = 300

    if par==111:  #es una imagen de la base de datos
        nueva_img = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        nueva_img = Image.fromarray(frame)

    for i in range(0, 600, rango_pix):
        for j in range(0, 600, rango_pix):
            imagen = trae_imagen()
            img_mod = ImageOps.fit(imagen, (rango_pix, rango_pix))
            nueva_img.paste(img_mod, (i, j))
    return nueva_img


def difuminado_gaussiano_random(par):

    if par==111:  #es una imagen de la base de datos
        imagen1 = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen1 = Image.fromarray(frame)

    # sacando el tamaño de la imagen
    ancho, alto = imagen1.size
    # seleccionar 10 areas
    d = 5
    for i in range(1, 5000):
        # pixeles de seleccion del área
        n = random.randint(0, 255)
        m = random.randint(0, 255)
        fin_n = n + d
        fin_m = m + d
        if fin_n > ancho:
            fin_n = ancho
        if fin_m > alto:
            fin_m = alto
        area = (n, m, fin_n, fin_m)
        region = imagen1.crop(area)
        gaus_reg = region.filter(ImageFilter.GaussianBlur(radius=3))
        imagen1.paste(gaus_reg, area)
    return imagen1


def difuminado_gaussiano_full(par):

    if par==111:  #es una imagen de la base de datos
        imagen = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen = Image.fromarray(frame)

    imagen = imagen.filter(ImageFilter.GaussianBlur(radius=10))
    return imagen


def apagado_pixel(par):

    if par==111:  #es una imagen de la base de datos
        imagen1 = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen1 = Image.fromarray(frame)

    for i in range(0, imagen1.size[0] - 1):

        for j in range(0, imagen1.size[1] - 1):

            pixel = imagen1.getpixel((i, j))  # Extraigo el pixel
            rojo = pixel[0]  # Extraigo valor color rojo
            verde = pixel[1]  # Extraigo valor color verde
            azul = pixel[2]  # Extraigo valor color azul
            # Si el pixel rojo es menor de 150, lo apago
            if (rojo <= 150):
                rojo = 0
            # Modifico la imagen con el nuevo valor del pixel
            imagen1.putpixel((i, j), (rojo, verde, azul))

    # Muestro la imagen transformada
    return imagen1


def efecto_zoom(par):
    if par == 111:  # es una imagen de la base de datos
        imagen1 = trae_imagen()
    else:
        frame = ctypes.cast(par, ctypes.py_object).value
        imagen1 = Image.fromarray(frame)

    factor_red = 8

    # sacando dimensiones de imagen original
    height, width = imagen1.size

    # resizing image
    new_image = imagen1.resize((int(height / factor_red), int(width / factor_red)), resample=Image.BILINEAR)

    # Perform the zoom
    imagen2 = new_image.resize((imagen1.size), Image.NEAREST)

    return imagen2

