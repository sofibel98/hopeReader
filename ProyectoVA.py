

import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'



def obtenerfoto():
    cap = cv2.VideoCapture(1)
    fr = 1
    while fr<=5:
        leido, frame = cap.read()
        fr = fr + 1
        if fr == 5: 
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            cv2.imwrite("foto.png", gray)
            print("Foto tomada correctamente")
            return frame
    cap.release()
    
def obtenerTexto():
    img=cv2.imread("foto.png")
    text = pytesseract.image_to_string(img,config='--psm 11')
    print('Texto ',text)
 
    
obtenerfoto()
obtenerTexto()

    
''' text = pytesseract.image_to_string(gray,config='--psm 11')
        print('Texto ',text) '''
