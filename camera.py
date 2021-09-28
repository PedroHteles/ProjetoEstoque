from pathlib import PureWindowsPath
from sys import intern
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import json
import time
import math 





img = cv2.imread('dirnal.png')
webcam = cv2.VideoCapture(0)
webcam.set(3,640)
webcam.set(4,480)

produtos = []
endereco = []




def lerqr(x):

    for barcode in decode(x):
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        try:
            qr = json.loads(barcodeData)
            if x < 1000 and x > 300 and  (qr['e']) not in endereco and qr['p'] == 0 and len(endereco) == 0:
                e = (qr['e'],(x,y))
                endereco.append(e)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 15)
                text = "endereco ({}) type({})".format(e,barcodeType)
                cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
            elif (qr['e']) not in endereco and qr['p'] == 0 and len(endereco) > 0:
                print(' mais de 1 endereco foi encontrado!!!')
                t = ((qr['e']),x,y)
                text = "mais de 1 endereco foi encontrado!!! endereco ({})".format(t)
                cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 15)
                
            
            if endereco != []:
                if (y >= endereco[0][1][1] and y / endereco[0][1][1] < 53.5  and (endereco[0][1][1] / y ) <= 0.6) and (x / endereco[0][1][0] <= 1.45 and x / endereco[0][1][0] >= 0.489) and (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) == 0 and endereco != []:
                    e = ((qr['p'],qr['e']),x,y)
                    produtos.append(e)
                    text = "produto ({}) type({})".format(e,barcodeType)
                    cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 0), 15) 

                elif (y >= endereco[0][1][1] and y / endereco[0][1][1] < 53.5  and (endereco[0][1][1] / y ) <= 0.6) and (x / endereco[0][1][0] <= 1.45 and x / endereco[0][1][0] >= 0.489) and (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) > 0 and endereco != []:
                    e = ((qr['p'],qr['e']),x,y)
                    text = "2 produtos encontrados!! produto ({})".format(e)
                    cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 15)

                elif (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) > 0:
                    e = ((qr['p'],qr['e']),x,y)
                    text = "!! produto ({})".format(e)
                    cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 15)
        except:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 15)



        







while True:
    validacao, frame = webcam.read()
    x = img
    lerqr(x)
    print('endereco:',endereco,'produtos:',produtos)
    
    cv2.imshow("produtos",img)
    cv2.waitKey(5)
