import cv2
from numpy.lib.function_base import append, piecewise
from pyzbar.pyzbar import decode
import json
import numpy as np


qrlidos = []
enderecoLidos = []
produtosLidos = []

enderec = []

banco = [({'end': 0, 'e': 25}, {'p': 1, 'e': 25})]

def lerqr(x,height,width):
    start_point = (int(width / 6), int(height  / 6))
    end_point = (int(width / 1.20), int(height / 1.20))
    cv2.rectangle(img, start_point, end_point,(255,0,0),2)
    

    for barcode in decode(x):
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        leituraArea = x < (end_point[0] - w) and x > start_point[0] and y < (end_point[1] - h ) and y > start_point[1] 
        
        try:
            qr = json.loads(barcodeData)
            quantidadeQrIdentificado = len(decode(img))
            qrEnd = 'end' in qr
            qrProd = 'p' in qr
            if leituraArea: 
                if qr not in qrlidos:
                    if qrEnd and qr not in enderec:
                        enderec.append(qr)
                    elif len(enderec) > 1 :
                        if qrEnd:
                            text = 'end {} invalido'.format(qr)
                            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.3, (0,0,255), 1)


                    if qrProd and len(enderec) == 1:
                        for i in enderec: 
                            if qr['e'] == i['e'] and (enderec[0],qr) not in qrlidos:
                                dados = (enderec[0],qr)
                                qrlidos.append(dados)
                            elif qr['e'] != i['e']:
                                text = 'produto no enderec errado'
                                cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.3, (0,0,255), 1)
                    else:
                        if qrProd and len(enderec) == 0:
                            text = 'aguardando qr enderec'
                            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.3, (0,0,255), 1)
                                
                
                
                if quantidadeQrIdentificado == 2 and len(qrlidos) == 1: 
                    if qrlidos == banco:
                        if qrProd:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            text = "prod({})".format(qr)
                        elif qrEnd:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                            text = "end ({})".format(qr)
                    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.3, (0,0,255), 1)
                    if qrlidos != banco:
                        print('teste')
                        if qr['p'] > 0:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0,255), 2)
                        elif qrEnd:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        print('produto no endereco errado',qrlidos)


            else:
                quantidadeQrIdentificado - 1
                cv2.rectangle(img, (x, y), (x + w, y + h), (87, 1,25), 15)
        except:
            if(leituraArea):
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)


while True:
    img = cv2.imread('./img/dirnal.png')
    height, width, channels = img.shape
    lerqr(img,height,width)
    
  
    cv2.imshow("camera",img)
    key = cv2.waitKey(5)
    if key == 27:
        break
    if key == 122:
        enderecoLidos.clear()
        produtosLidos.clear()
        qrlidos.clear()
        enderec.clear()


    

        