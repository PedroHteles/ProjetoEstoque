from sys import intern
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import json
import time





img = cv2.imread('agrvai.png')
webcam = cv2.VideoCapture(0)
webcam.set(3,640)
webcam.set(4,480)


            
produt = []
enderc = [ ]
produtos = []
enderecos = []
a=[]
def lerqr(x):
    
    for barcode in decode(x):
        myData = barcode.data
        qr = json.loads(myData)
        product = {}

        try:
            if qr not in produtos and qr['p'] > 0:
                p = (qr['p'],qr['e'])
                product['p'] = qr['p']
                product['e'] = qr['e'] 
                produtos.append(qr)
                produt.append(p)
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(img,[pts],True,(0,255,0),5)  
                a.append(p)
            elif qr not in enderecos and qr['p'] == 0:
                product['e'] = qr['e']
                enderecos.append(qr)
                p = (qr['e'])
                enderc.append(p)
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(img,[pts],True,(0,255,0),5)  
                a.append(p)
            elif qr:
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(img,[pts],True,(110,0,85),5)  
  
        except:
            print('AAA')
        



while True:
    validacao, frame = webcam.read()
    x = img
    lerqr(x)
    lst = np.array(produt)
    result = np.where(lst == enderc)
    print(result[0])
    






    
    cv2.imshow("produtos",img)
    cv2.waitKey(5)
