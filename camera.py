from ctypes import resize
from os import closerange
import cv2
from numpy.core.numeric import isclose
from pyzbar.pyzbar import decode
import json
import numpy as np

banco = ({'end': 0, 'e': 21}, {'p': 10, 'e': 21})
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
                if validado != []:
                    print(len(decode(img)))
                    if len(decode(img)) <= 1 or len(decode(img)) > 2:
                        leituraProduto.clear()
                        leituraEndereco.clear()
                        validado.clear()
                        pass
                    if validado != []:
                        leituraProduto.clear()
                        leituraEndereco.clear()
                        return validado[0]
                else:
                    if qrEnd and qr not in leituraEndereco:
                        leituraEndereco.append(qr) 
                    elif  qrProd and qr not in leituraProduto and leituraEndereco !=[]:
                        leituraProduto.append(qr)
                    if len(decode(img)) > 2:
                        if qr not in area:
                            area.append(qr) 
                    elif len(decode(img)) <= 2:
                        print('a',leituraProduto,leituraEndereco)
                        if qrProd and len(leituraEndereco) != 1:
                            leituraEndereco.clear()
                        elif qrEnd and len(leituraProduto) != 1:
                            leituraProduto.clear()
                        area.clear()
                    
                    if qrProd and len(decode(img)) == 1:
                        print('Aguardand endereco')
                        leituraEndereco.clear()
                        validado.clear()
                    elif qrEnd and len(decode(img)) == 1:
                        print('Aguardando Produto!')
                        leituraProduto.clear()
                        validado.clear()

                    if len(decode(img)) == 2 and len(leituraEndereco) == 1 and len(leituraProduto) == 1 and area ==[]:
                        area.clear()
                        if len(decode(img)) == 2 and area == []:
                            valor = (leituraEndereco[0],leituraProduto[0])
                            return valor
                    else:
                        print('debug')
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
    result = lerqr(img,height,width)
    print(result)
    
    for leitura in decode(img):
        (x, y, w, h) = leitura.rect
        if result and len(result) == 2 :
            start_point = (int(width / 8), int(height  / 8))
            end_point = (int(width / 1.15), int(height / 1.15))
            leituraArea = x < (end_point[0] - w) and x > start_point[0] and y < (end_point[1] - h ) and y > start_point[1] 
            barcodeData = leitura.data.decode("utf-8")
            if leitura:
                qr = json.loads(barcodeData)
                if result[0]['e'] == result[1]['e'] and len(result) == 2:
                    if result not in validado:
                        validado.append(result)
                    # print('validado',result)
                    # print(result == banco)
                    leituraProduto.clear()
                    leituraEndereco.clear()
                    if qr in result:
                        if 'end' in qr:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 15) 
                        elif 'p' in qr:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,255), 15)
                elif  result[0]['e'] != result[1]['e']:
                    validado.clear()
                    leituraProduto.clear()
                    leituraEndereco.clear()
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 15)
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 15)

    cv2.imshow("camera",img)
    key = cv2.waitKey(5)
    if key == 27:
        break