from pathlib import PureWindowsPath
from sys import intern
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import json
import time
import math 





img = cv2.imread('dinalerro.png')
webcam = cv2.VideoCapture(0)
webcam.set(3,640)
webcam.set(4,480)

produtos = []
endereco = []



                # result =  np.where(produtos[0][1] in endereco)

                # if (qr['p'],qr['e']) not in produtos and qr['p'] > 0 and len(produtos) == 0:
                #     p = (qr['p'],qr['e'],x,y)
                #     # produtos.append(p)
                #     cv2.rectangle(img, (x, y), (x + w, y + h), (0,255, 0), 3)
                #     text = "Produto ({})".format(p) 
                #     cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                #     result =  np.where(produtos[0][1] in endereco)
                # elif (qr['p'],qr['e'])  in produtos and qr['p'] > 0:
                #     cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,0), 20)
                #     result =  np.where(produtos[0][1] in endereco)




def lerqr(x):

    for barcode in decode(x):
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        qr = json.loads(barcodeData)
            
        if (qr['e']) not in endereco and qr['p'] == 0 and len(endereco) == 0:
            e = (qr['e'],x,y)
            endereco.append(e)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 30)
            # text = "endereco ({})".format(e)
        elif (qr['e']) not in endereco and qr['p'] == 0 and len(endereco) > 0:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 15)
            
            
    
        if (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) == 0 and endereco != []:
            if(x > endereco[0][1] - 189 and x < endereco[0][1] + 189):
                print('teste')
            print(x,endereco[0][1] - 189)
            e = ((qr['p'],qr['e']),x,y)
            produtos.append(e)
            print(produtos,qr,'x:',x,'y:',y)
            cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 0), 30)   
        elif (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) > 0:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 105)



        







while True:
    validacao, frame = webcam.read()
    x = img
    lerqr(x)
    
    cv2.imshow("produtos",img)
    cv2.waitKey(5)
