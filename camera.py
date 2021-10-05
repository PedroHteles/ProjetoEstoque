
import cv2
from pyzbar.pyzbar import decode
import json
import numpy as np

qrlidos = []
banco = [({'end': 0, 'e': 25}, {'p': 1, 'e': 25})]
validado = []
naoValido = []

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
                if qrEnd and qr not in qrlidos or qrProd and qr not in qrlidos:
                    qrlidos.append(qr) 
                # elif qrEnd and qr not in qrlidos:
                #     print('mais de 1 enderec encontrado',qr)
                #     # qrlidos.clear()
                # elif qrProd and qr not in qrlidos:
                #     print('mais de 1 produto encontrado',qr)
                #     # qrlidos.clear()
                elif len(qrlidos) > 2:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0,255, 255), 25)
                    print('mais de 2 qr na area da leitura')
                    qrlidos.clear()


                if len(qrlidos) == 2 and qrlidos not in validado:
                    for i in qrlidos:
                        valor = (qrlidos[0],qrlidos[1])
                        if qrProd and 'end' in i: 
                            if valor not in validado and qr['e'] == i['e']:
                                print('validado')
                                validado.append(valor)
                                qrlidos.clear()
                            elif qr['e'] != i['e']:
                                print('Nao validado')
                                if valor not in naoValido:
                                    naoValido.append(valor)
                    for i in validado:
                        if qr == i[0]:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0,255, 0), 15)
                        elif qr == i[1]:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,255), 15)
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


    

        