import cv2
from numpy.lib.function_base import append
from pyzbar.pyzbar import decode
import json
import numpy as np


qrlidos = []
enderecoLidos = []
produtosLidos = []

enderecosValidos = []
produtosValidos = []

tess = [{'p': 0, 'e': 1005}, {'p': 1, 'e': 1005}]

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
            enderecoQr = qr['e']
            qrCodigoProduto = qr['p']
            if leituraArea: 
                if qr not in qrlidos:
                    qrlidos.append(qr)
                    return

                if len(decode(img)) == 2:
                    print(qrlidos,qrlidos == tess)

                elif len(decode(img)) > 2:
                    for i in qrlidos:
                        if i['p'] == 0:
                            if i not in enderecoLidos:
                                enderecoLidos.append(i)

                    if len(enderecoLidos) == 1 and  enderecoLidos !=[]:            
                        for i in qrlidos:
                            if i['p'] > 0:
                                if i not in produtosLidos:
                                    produtosLidos.append(i)
                            if len(produtosLidos) > 1:
                                if qr in  produtosLidos:
                                    print('mais de 1 produto encontrado!',produtosLidos)
                                    return produtosLidos
                    elif len(enderecoLidos) > 1:
                        if qr in enderecoLidos:
                            print('mais de 1 endereco encontrado!',enderecoLidos)
            
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0,255), 20)
        except:
            if(leituraArea):
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

img = cv2.imread('./img/dirnal.png')
while True:
    
    height, width, channels = img.shape
    print(len(decode(img)))
    lerqr(img,height,width)
    
  
    cv2.imshow("camera",img)
    key = cv2.waitKey(5)
    if key == 27:
        break
    if key == 122:
        erroEnderecoAux = []
        erroProdutoAux = []


    

        