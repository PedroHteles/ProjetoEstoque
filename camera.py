from sys import intern
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import json


webcam = cv2.VideoCapture(0)
webcam.set(3,640)
webcam.set(4,480)

produto ='{"p":1234,"e":1}'
endereco = '{"end":1}'


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
produtos = []
enderecos = []
itens = []
teste = {}


img = cv2.imread('final.png')

while True:
    validacao, frame = webcam.read()

    for barcode in decode(img):
        myData = barcode.data
        try:   
            qr = json.loads(myData)
            if qr not in itens:
                if len(qr) == 2:
                    if {'p':qr["p"],'e':qr["e"]} not in produtos:
                        product = {}
                        product['p'] = qr['p']
                        product['e'] = qr['e']
                        produtos.append(product)  
                elif len(qr) == 1:
                    if {'end':qr["end"]} not in enderecos:
        
                        enderecos.append({'end':qr["end"]})

        except:
            print('erro')
    break

# if produtos['e'] == enderecos['end']:
#     print('ok')
print(produtos)
print(enderecos)


        
    #     pts = np.array([barcode.polygon], np.int32)
    #     pts = pts.reshape((-1,1,2))
    #     cv2.polylines(frame,[pts],True,(255,0,255),5)  
    # cv2.imshow("teste",frame)
    # cv2.waitKey(5)

