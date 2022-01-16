import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
import cv2
import numpy as np
import pyttsx3
import sys
import os

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

def obtenerTexto():
    img = cv2.imread('prueba.PNG')
    img = rotate_bound(img, 90)
    cv2.imshow('Imagen de salida',img)
    
    config = '--oem 3 --psm 11'
    txt = pytesseract.image_to_string(img, config=config, lang='eng')
    print(txt)
    return txt
obtenerTexto()
cv2.waitKey(0)
cv2.destroyAllWindows()