from sys import intern
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import json


webcam = cv2.VideoCapture(0)
webcam.set(3,640)
webcam.set(4,480)

itens =[]
print(len(itens))
while True:
    validacao, frame = webcam.read()

    for barcode in decode(frame):
        myData = barcode.data.decode('utf-8')
        if myData not in itens: 
            teste = myData.split(',')
            if 'p' in myData:
                print('p:',teste[0].split(':')[1])
            if 'e' in myData:
                print('e:',teste[1].split(':')[1])

        
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame,[pts],True,(255,0,255),5)  
    cv2.imshow("teste",frame)
    cv2.waitKey(5)

