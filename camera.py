from collections import namedtuple
import cv2
from pyzbar.pyzbar import decode
import json
import numpy as np

banco = [({'end': 0, 'e': 25}, {'p': 1, 'e': 25})]
validado = []
naoValido = []

leituraProduto = []
leituraEndereco = []
area = []

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
                if qrEnd and qr not in leituraEndereco:
                    leituraEndereco.append(qr) 
                elif  qrProd and qr not in leituraProduto and leituraEndereco !=[]:
                    leituraProduto.append(qr) 

                if qrProd and len(decode(img)) == 1:
                    leituraEndereco.clear()
                    validado.clear()
                elif qrEnd and len(decode(img)) == 1:
                    leituraProduto.clear()
                    validado.clear()
                
                elif len(decode(img)) == 2:
                    area.clear()
                    if len(decode(img)) == 2 and area == []:
                        valor = (leituraEndereco[0],leituraProduto[0])
                        if valor[0]['e'] == valor[1]['e']:
                            print('validado')
                            if valor not in validado:
                                validado.append(valor)
                            return validado
                        else:
                            if valor not in naoValido:
                                print('Nao validado')
                                naoValido.append(valor)
                            return naoValido
                else:
                    if qr not in area:
                        area.append(qr)
                    if len(area) == len(decode(img)):
                        return area    
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 15)                   
        except:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,255, 255), 2)
while True:
    img = cv2.imread('./img/dirnal.png')
    height, width, channels = img.shape
    print(lerqr(img,height,width))
    cv2.imshow("camera",img)
    key = cv2.waitKey(5)
    if key == 27:
        break