import cv2
from pyzbar.pyzbar import decode
import json

produtosAux = []
endereco = []
erroAux = []

def lerqr(x,height,width):

    start_point = (int(width / 6), int(height  / 6))
    end_point = (int(width / 1.20), int(height / 1.20))
    color = (255, 0, 0)
    thickness = 2
    cv2.rectangle(img, start_point, end_point, color, thickness)
    

    for barcode in decode(x):
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        leituraArea = x < (end_point[0] - w) and x > start_point[0] and y < (end_point[1] - h ) and y > start_point[1] 
        try:
            qr = json.loads(barcodeData)
            enderecoQr = qr['e']
            qrCodigoProduto = qr['p']     

            if leituraArea and enderecoQr not in endereco and qrCodigoProduto == 0 and len(endereco) == 0:
                e = ((enderecoQr),(x,y))
                endereco.append(e)
                print(' endereco encontrado')
            elif endereco == []:
                print('aguardando qr Endereco')    


            if leituraArea and (qrCodigoProduto,enderecoQr) not in produtosAux and qrCodigoProduto > 0 and len(produtosAux) == 0 and endereco !=[]:
                p = ((qrCodigoProduto,enderecoQr),(x,y))
                produtosAux.append(p)
                print(' produto encontrado')
            elif produtosAux == []:
                print('aguardando qr Produto')

            #  //////////////////////////////////// VERIFICACAO QR ///////////////////////////////   

            pCpQrAux = produtosAux[0][0][0]
            pAux = produtosAux[0][0]
            
            eQrAux = endereco[0][0]

            # verifica se existe mais de 1 qr na leitura
            if leituraArea and qrCodigoProduto == 0 and enderecoQr != eQrAux and len(erroAux) == 0 :
                print('mais de 1 endereco encontrado')
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 20)
                e = ((enderecoQr),(x,y))
                erroAux.append(e)
            else:
                erroAux = []

            if leituraArea and qrCodigoProduto > 0 and qrCodigoProduto != pCpQrAux:
                print('mais de 1 Produto encontrado')
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
                
            # valida qr endereco
            if erroAux == []:
                if leituraArea and qrCodigoProduto == 0 and enderecoQr == eQrAux:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

                elif leituraArea and qrCodigoProduto == 0 and enderecoQr != eQrAux:
                    print('erro qr endereco')
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0,255), 5)

                # valida qr produto
                if leituraArea and qrCodigoProduto > 0 and (qrCodigoProduto,enderecoQr) == pAux and enderecoQr == eQrAux:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)

                elif leituraArea and qrCodigoProduto > 0 and (qrCodigoProduto,enderecoQr) == pAux and enderecoQr != eQrAux:
                    print('Produto no endereco errado')
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0,255), 5)
            else:
                if(leituraArea):
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0,255), 5)
                    if leituraArea and qrCodigoProduto == 0:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 15)
                    
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
    
    

            
