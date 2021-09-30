import cv2
from pyzbar.pyzbar import decode
import json
import numpy as np


erroEnderecoAux = []
erroProdutoAux = []


produtosAux = []
enderecoAux = []

produtosValidos = []
enderecosValidos = []

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

                # ///////////////////////////////////////// valida qr //////////////////////////////////////////// 
                
                # if qrCodigoProduto == 0 and enderecoQr not in enderecoAux:
                #     print(' endereco encontrado')
                #     enderecoAux.append(enderecoQr)
                # elif (qrCodigoProduto,enderecoQr) not in produtosAux and qrCodigoProduto > 0 and enderecoAux !=[] and enderecoQr in enderecoAux:
                #     print(' produto encontrado')
                #     if enderecoQr in enderecoAux  and (qrCodigoProduto,enderecoQr) not in produtosAux:
                #         produtosAux.append((qrCodigoProduto,enderecoQr))

                if len(enderecoAux)== 0 and qrCodigoProduto == 0 and enderecoQr not in enderecoAux:
                    print(' endereco encontrado')
                    enderecoAux.append(enderecoQr)
                elif len(produtosAux)== 0 and  (qrCodigoProduto,enderecoQr) not in produtosAux and qrCodigoProduto > 0 and enderecoAux !=[] and enderecoQr in enderecoAux:
                    print(' produto encontrado')
                    if enderecoQr in enderecoAux  and (qrCodigoProduto,enderecoQr) not in produtosAux:
                        produtosAux.append((qrCodigoProduto,enderecoQr))
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 15)


                # ////////////////////////////////////////////// corzinha no qr validado ////////////////////////////////
                lst = np.array(produtosAux)
                result = np.where(lst == enderecoQr)

                if enderecoQr in enderecoAux  and (qrCodigoProduto,enderecoQr)  in produtosAux:
                    if (qrCodigoProduto,enderecoQr) not in produtosValidos:
                        produtosValidos.append((qrCodigoProduto,enderecoQr))
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 15)
                elif qrCodigoProduto == 0 and enderecoQr in enderecoAux and np.array(result).size > 0 :
                    if enderecoQr not in enderecosValidos:
                        enderecosValidos.append(enderecoQr)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 15)
        
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0,255), 20)

                    
        except:
            if(leituraArea):
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)


while True:
    img = cv2.imread('./img/dirnal.png')
    height, width, channels = img.shape
    lerqr(img,height,width)
    print(produtosValidos,enderecosValidos)
    
  
    cv2.imshow("camera",img)
    key = cv2.waitKey(5)
    if key == 27:
        break
    if key == 122:
        erroEnderecoAux = []
        erroProdutoAux = []


    

        