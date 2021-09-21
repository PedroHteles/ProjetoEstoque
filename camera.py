from sys import intern
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import json






# try:

#     endereco = json.loads(endereco)
#     valida = endereco["end"]
#     try:
#         produto = json.loads(produto)
#         valida = produto["p"],produto["e"]
        
#         print(f'''Endereco: {endereco["end"]}''')
#         print(f'''Produto:'{produto["p"]}, Endereco-Do-Produto:{produto["e"]}''')
#         print(f'''Posicao-Pedido: {produto["p"]} Endereco: {produto["e"]}''', produto["e"] == endereco["end"])

#     except:
#         print('qr code produto errado')
    
# except:
#     print('qr code endereco errado')



# errados = []
# corretos = []
enderecos = []
itens = []
teste = {}


img = cv2.imread('opa.png')
webcam = cv2.VideoCapture(0)
webcam.set(3,640)
webcam.set(4,480)

while True:
    validacao, frame = webcam.read()

    for barcode in decode(img):
        myData = barcode.data
        try:   
            qr = json.loads(myData)
            if qr not in itens:
                produtos = []
                product = {}
                if len(qr) == 2:
                    if {'p':qr["p"],'e':qr["e"]}:
                        product['p'] = qr['p']
                        product['e'] = qr['e']
                        print(len(product))
                        if len(product) <= 2:
                            pts = np.array([barcode.polygon], np.int32)
                            pts = pts.reshape((-1,1,2))
                            cv2.polylines(img,[pts],True,(0,255,0),5)  
                elif len(qr) == 1:
                    if {'end':qr["end"]}:
                        pts = np.array([barcode.polygon], np.int32)
                        pts = pts.reshape((-1,1,2))
                        cv2.polylines(img,[pts],True,(255,0,0),5)  
                        print({'end':qr["end"]})

        except:
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(img,[pts],True,(0,0,255),5)  
            print('erro')
            
    
    cv2.imshow("teste",img)
    cv2.waitKey(5)

# if produtos['e'] == enderecos['end']:
#     print('ok')
