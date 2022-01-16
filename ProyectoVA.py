from kivy.uix.button import Button
from kivy.app import App
import kivy
import pyttsx3
import numpy as np
import cv2
import pytesseract
import sys
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

''' ***********************Lógica de la lectura del texto*************************************'''
def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))


def quitarSaltos(texto):
    lst = []
    for pos, char in enumerate(texto):
        if(char == '\n'):
            lst.append(' ')
        else:
            lst.append(char)

    txt = "".join(lst)
    return txt


def textoAaudio(texto):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 135)
    engine.say(texto)
    engine.runAndWait()


def obtenerTexto():
    img = cv2.imread('prueba.PNG')
    img = rotate_bound(img, 90) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    config = '--oem 3 --psm 11'
    txt = pytesseract.image_to_string(img, config=config, lang='eng')
    print(txt)
    return txt


def leer():
    txt = obtenerTexto()
    txt = quitarSaltos(txt)
    textoAaudio(txt)


'''******************************Interfaz gráfica*********************************************'''

import kivy
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button 
from kivy.uix.camera import Camera
from kivy.app import App
import time


class Aplicacion(App):
    def build(self):
        global wdg
        global lbl
        global btnLeer
        global btnSalir
        global camara
        
        wdg = Widget()
        
        camara = Camera(play=True, index=1, resolution=(640,480), size=(640,480),pos = (10,0))
        wdg.add_widget(camara);
        
        btnLeer = Button()
        btnLeer.text = "Leer"
        btnLeer.pos = (660,150)
        btnLeer.size = (100, 100)
        wdg.add_widget(btnLeer)        
        btnLeer.bind(on_press=self.ac_btn_leer)
        
        btnSalir = Button()
        btnSalir.text = "Salir"
        btnSalir.pos = (660,275)
        btnSalir.size = (100, 100)
        wdg.add_widget(btnSalir)        
        btnSalir.bind(on_press=self.ac_btn_salir)
        
        return wdg
        
    def ac_btn_leer(self, *args):
        camara.export_to_png('prueba.PNG')
        print("Foto tomada")
        leer()
        
    def ac_btn_salir(self, *args):
        Aplicacion.get_running_app().stop()
        
if __name__=="__main__":
 Aplicacion().run()
