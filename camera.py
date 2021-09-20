from sys import intern
import cv2
# from pyzbar.pyzbar import decode
import numpy as np
import json


webcam = cv2.VideoCapture(0)
webcam.set(3,640)
webcam.set(4,480)

produto ='{"p":1234,"e":1}'
endereco = '{"end":1}'


try:

    endereco = json.loads(endereco)
    valida = endereco["end"]
    try:
        produto = json.loads(produto)
        valida = produto["p"],produto["e"]
        
        print(f'''Endereco: {endereco["end"]}''')
        print(f'''Produto:'{produto["p"]}, Endereco-Do-Produto:{produto["e"]}''')
        print(f'''Posicao-Pedido: {produto["p"]} Endereco: {produto["e"]}''', produto["e"] == endereco["end"])

    except:
        print('qr code produto errado')
    
except:
    print('qr code endereco errado')



# errados = []
# corretos = []
# produtos = []
# enderecos = []
# itens = []
# print(len(itens))



# while True:
#     validacao, frame = webcam.read()

#     for barcode in decode(frame):
#         myData = barcode.data.decode('utf-8')
#         if myData not in itens:
#             qr = json.loads(myData)
#             if qr["p"] and qr["e"] in qr:
#                   produto = json.loads(myData)
#             elif  qr["e"] in qr:
#                   enderecos = json.loads(myData)
#             else:
#                   print('erro ao ler qr ')
#             # if produto["p"] and produto["e"] in produto:
#             #     print(produto["p"],produto["e"])
#             # else if (produto["p"] and produto["e"] not in produto):
#             #     print('erro ao ler o qr code')
#             # if enderecos["end"]:
#             #     print(enderecos["end"])

        
#         pts = np.array([barcode.polygon], np.int32)
#         pts = pts.reshape((-1,1,2))
#         cv2.polylines(frame,[pts],True,(255,0,255),5)  
#     cv2.imshow("teste",frame)
#     cv2.waitKey(5)

