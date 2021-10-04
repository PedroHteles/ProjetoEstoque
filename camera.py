import cv2
from pyzbar.pyzbar import decode
import json
import numpy as np
import time

qrlidos = []
banco = [({'end': 0, 'e': 25}, {'p': 1, 'e': 25})]
validado = []

def lerqr(x,height,width):
    start_point = (int(width / 8), int(height  / 8))
    end_point = (int(width / 1.15), int(height / 1.15))
    cv2.rectangle(img, start_point, end_point,(255,0,0),2)
    

    for barcode in decode(x):
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        leituraArea = x < (end_point[0] - w) and x > start_point[0] and y < (end_point[1] - h ) and y > start_point[1] 
        
        try:
            qr = json.loads(barcodeData)
            qrEnd = 'end' in qr
            qrProd = 'p' in qr
            if leituraArea: 
                if qrEnd and qr not in qrlidos and len(qrlidos) == 0 or qrProd and qr not in qrlidos and qrlidos != [] and len(qrlidos) == 1:
                        qrlidos.append(qr) 
                        return
                elif qrEnd and qr not in qrlidos and len(qrlidos) > 1:
                    print('mmais de 1 enderec encontrado',qr)
                elif qrProd and qr not in qrlidos and len(qrlidos) >= 2:
                    print('mais de 1 produto encontrado',qr)

                if len(qrlidos) == 2 and qrlidos not in validado:
                    for i in qrlidos:
                        if qrEnd and qr == i or qrProd and 'end' in i and qr['e'] == i['e']:
                            if qrEnd:
                                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
                                text = 'endereco ({})'.format(qr)
                                cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255), 2)

                            if qrProd:
                             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            valor = (qrlidos[0], qrlidos[1])
                            if qrProd and valor not in validado  and 'end' in i and qr['e'] == i['e']:
                                text = 'produto ({})'.format(qr)
                                cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255), 2)
                                validado.append(valor)
                            qrlidos.clear()
                        elif qrProd and 'end' in i and qr['e'] != i['e'] or  qrEnd and qr != i:
                            if qrProd:
                                text = 'produto ({})'.format(qr)
                                cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255), 2)
                                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0,255), 2)
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0,255, 255), 25)
        except:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,255, 255), 2)


while True:
    img = cv2.imread('./img/dirnal.png')
    height, width, channels = img.shape
    lerqr(img,height,width)
    cv2.imshow("camera",img)
    key = cv2.waitKey(5)
    if key == 27:
        break
    if key == 122:
        qrlidos.clear()


    

        