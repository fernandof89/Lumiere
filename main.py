from __future__ import print_function
import cv2
from deepface import DeepFace
import time
import functools
import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
# from ffpyplayer.player import MediaPlayer

#### DEEPFACE
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Probar si la webcam está disponible.
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

t_end = time.time() + 4

info = [['neutral']]
style_name = "yellow"

videoChange = 0
videoAlter = 0

# song = r'C:\Users\R\Desktop\Tesis\Musica\neutral.mp3'
# songYellow = r'C:\Users\R\Desktop\Tesis\Musica\neutral.mp3'
# songBlue = r'C:\Users\R\Desktop\Tesis\Musica\neutral.mp3'
# songWhite = r'C:\Users\R\Desktop\Tesis\Musica\neutral.mp3'
# songRed = r'C:\Users\R\Desktop\Tesis\Musica\neutral.mp3'
# songBlack = r'C:\Users\R\Desktop\Tesis\Musica\neutral.mp3'

# music = song

while True:
    ret, frame = cap.read()
    resultFace = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

    # This is to check whether to break the first loop
    isclosed = 0

    capVid1 = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\01\01 b1.mp4')
    capVid1yellow = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\Expresiones\01 yellow.mp4')
    capVid1blue = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\Expresiones\01 blue.mp4')
    capVid1white = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\Expresiones\01 white.mp4')
    capVid1red = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\Expresiones\01 red.mp4')
    capVid1black = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\Expresiones\01 black.mp4')
    capVid2 = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\02\02 b1.mp4')
    capVid2yellow = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\Expresiones\02 yellow.mp4')
    capVid2blue = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\Expresiones\02 blue.mp4')
    capVid2white = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\Expresiones\02 white.mp4')
    capVid2red = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\Expresiones\02 red.mp4')
    capVid2black = cv2.VideoCapture(r'C:\Users\R\Desktop\Tesis\Expresiones\02 black.mp4')

    # capSound1 = MediaPlayer(r'C:\Users\R\Desktop\Tesis\01\01 b.mp4')
    # capSound1yellow = MediaPlayer(r'C:\Users\R\Desktop\Tesis\Expresiones\01 yellow.mp4')
    # capSound1blue = MediaPlayer(r'C:\Users\R\Desktop\Tesis\Expresiones\01 blue.mp4')
    # capSound1white = MediaPlayer(r'C:\Users\R\Desktop\Tesis\Expresiones\01 white.mp4')
    # capSound1red = MediaPlayer(r'C:\Users\R\Desktop\Tesis\Expresiones\01 red.mp4')
    # capSound1black = MediaPlayer(r'C:\Users\R\Desktop\Tesis\Expresiones\01 black.mp4')
    # capSound2 = MediaPlayer(r'C:\Users\R\Desktop\Tesis\02\02 b.mp4')
    # capSound2yellow = MediaPlayer(r'C:\Users\R\Desktop\Tesis\Expresiones\02 yellow.mp4')
    # capSound2blue = MediaPlayer(r'C:\Users\R\Desktop\Tesis\Expresiones\02 blue.mp4')
    # capSound2white = MediaPlayer(r'C:\Users\R\Desktop\Tesis\Expresiones\02 white.mp4')
    # capSound2red = MediaPlayer(r'C:\Users\R\Desktop\Tesis\Expresiones\02 red.mp4')
    # capSound2black = MediaPlayer(r'C:\Users\R\Desktop\Tesis\Expresiones\02 black.mp4')

    # capSound1 = MediaPlayer(song)
    # capSound1yellow = MediaPlayer(song)
    # capSound1blue = MediaPlayer(song)
    # capSound1white = MediaPlayer(song)
    # capSound1red = MediaPlayer(song)
    # capSound1black = MediaPlayer(song)
    # capSound2 = MediaPlayer(song)
    # capSound2yellow = MediaPlayer(song)
    # capSound2blue = MediaPlayer(song)
    # capSound2white = MediaPlayer(song)
    # capSound2red = MediaPlayer(song)
    # capSound2black = MediaPlayer(song)

    while True:
        if not videoChange:
            if videoAlter == 0:
                retVid, frameVid = capVid1.read()
                # retSound, frameSound = capSound1.get_frame()
            if videoAlter == 1:
                retVid, frameVid = capVid1yellow.read()
                # retSound, frameSound = capSound1yellow.get_frame()
            if videoAlter == 2:
                retVid, frameVid = capVid1blue.read()
                # retSound, frameSound = capSound1blue.get_frame()
            if videoAlter == 3:
                retVid, frameVid = capVid1white.read()
                # retSound, frameSound = capSound1white.get_frame()
            if videoAlter == 4:
                retVid, frameVid = capVid1red.read()
                # retSound, frameSound = capSound1red.get_frame()
            if videoAlter == 5:
                retVid, frameVid = capVid1black.read()
                # retSound, frameSound = capSound1black.get_frame()
        if videoChange:
            if videoAlter == 0:
                retVid, frameVid = capVid2.read()
                # retSound, frameSound = capSound2.get_frame()
            if videoAlter == 1:
                retVid, frameVid = capVid2yellow.read()
                # retSound, frameSound = capSound2yellow.get_frame()
            if videoAlter == 2:
                retVid, frameVid = capVid2blue.read()
                # retSound, frameSound = capSound2blue.get_frame()
            if videoAlter == 3:
                retVid, frameVid = capVid2white.read()
                # retSound, frameSound = capSound2white.get_frame()
            if videoAlter == 4:
                retVid, frameVid = capVid2red.read()
                # retSound, frameSound = capSound2red.get_frame()
            if videoAlter == 5:
                retVid, frameVid = capVid2black.read()
                # retSound, frameSound = capSound2black.get_frame()
        # It should only show the frame when the ret is true
        if retVid:
            cv2.imshow('frame', frameVid)
            # if frameSound != 'eof' and retSound is not None:
            #     img, t = retSound
            time.sleep(.025)

            if time.time() > t_end:
                ret, frame = cap.read()
                resultFace = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                info = [[resultFace['dominant_emotion']]]
                print([[resultFace['dominant_emotion']]])

                if info == [['neutral']]:
                    # When b is pressed videoChange is 1
                    videoAlter = 0
                if info == [['happy']]:
                    # When b is pressed videoChange is 1
                    style_name = "yellow"
                    videoAlter = 1
                if info == [['sad']]:
                    # When b is pressed videoChange is 1
                    style_name = "blue"
                    videoAlter = 2
                if info == [['surprise']]:
                    # When b is pressed videoChange is 1
                    style_name = "white"
                    videoAlter = 3
                if info == [['angry']]:
                    # When b is pressed videoChange is 1
                    style_name = "red"
                    videoAlter = 4
                if info == [['fear']]:
                    # When b is pressed videoChange is 1
                    style_name = "black"
                    videoAlter = 5

                t_end = time.time() + 4

            pressedKey = cv2.waitKey(10) & 0xFF

            if pressedKey == ord('a'):
                # When a is pressed videoChange is 0
                videoChange = 0
            if pressedKey == ord('b'):
                # When b is pressed videoChange is 1
                videoChange = 1

            if pressedKey == ord('q'):
                # When q is pressed isclosed is 1
                isclosed = 1
                break
        else:
            break
    # To break the loop if it is closed manually
    if isclosed:
        break

cap.release()
capVid1.release()
capVid2.release()
cv2.destroyAllWindows()
