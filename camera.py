from sys import intern
import cv2
from numpy.core.fromnumeric import amax
from pyzbar.pyzbar import decode
import numpy as np
import json
import time
import math 





img = cv2.imread('dinal.png')
webcam = cv2.VideoCapture(0)
webcam.set(3,640)
webcam.set(4,480)


            
def lerqr(x):
    produtos = []
    endereco = []
    for barcode in decode(x):
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        try:
            qr = json.loads(barcodeData)
            if (qr['p'],qr['e']) not in produtos and qr['p'] > 0:
                p = (qr['p'],qr['e'])
                produtos.append(p)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0,255, 0), 2)
                text = "Produto ({})".format(barcodeType)
            elif (qr['e']) not in endereco and qr['p'] == 0:
                p = (qr['e'])
                endereco.append(p)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                text = "endereco ({})".format(barcodeType)
            else:
                return 'error'
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
        except:
            text = "erro qr '{}' nao e valido ({})".format(barcodeData,barcodeType)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
        result =  np.where(produtos[0][1] in endereco)
    return np.array(result).size 
        
while True:
    validacao, frame = webcam.read()
    x = img
    print(lerqr(x) > 0)

    
    cv2.imshow("produtos",img)
    cv2.waitKey(5)
