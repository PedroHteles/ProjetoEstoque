import cv2
from pyzbar.pyzbar import decode
import json
import numpy as np

webcam = cv2.VideoCapture(0)

def lerqr(x):
    produtos = []
    endereco = []
    for barcode in decode(x):
            lst = np.array(produtos)
            result = np.where(lst == endereco)
            qr = json.loads(barcode.data)
            if qr not in produtos and qr['p'] > 0:
                p = (qr['p'],qr['e'])
                produtos.append(p)
            elif qr not in endereco and qr['p'] == 0:
                p = (qr['e'])
                endereco.append(p)
            print(produtos, endereco)

            print(np.array(result).size > 0)
    return           
if webcam.isOpened():
    validacao, frame = webcam.read()
    while validacao:
        validacao, frame = webcam.read()
        lerqr(frame)
            

        cv2.imshow("camera",frame)
        cv2.waitKey(5)
    
    

            
