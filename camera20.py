import cv2
from pyzbar.pyzbar import decode
import json
import numpy as np

webcam = cv2.VideoCapture(0)


    
produtos = []
endereco = []
def lerqr(x):

    for barcode in decode(x):
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        qr = json.loads(barcodeData)
        try:
            
            if (qr['e']) not in endereco and qr['p'] == 0 and len(endereco) == 0:
                e = (qr['e'],x,y)
                endereco.append(e)
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(frame,[pts],True,(255,0,255),5) 
                # text = "endereco ({})".format(e)
            elif (qr['e']) not in endereco and qr['p'] == 0 and len(endereco) > 0:
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(frame,[pts],True,(255,0,255),5) 
                
                
        
            if (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) == 0 and endereco != []:

                print((x / endereco[0][1]) > 0.5)
                print(x,endereco[0][1])
                e = ((qr['p'],qr['e']),x,y)
                produtos.append(e)
                print(produtos,qr,'x:',x,'y:',y)
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(frame,[pts],True,(255,0,255),5) 
            elif (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) > 0:
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(frame,[pts],True,(255,0,255),5) 
        except:
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(frame,[pts],True,(0,0,255),50) 




if webcam.isOpened():
    validacao, frame = webcam.read()
    while validacao:
        validacao, frame = webcam.read()
        lerqr(frame)
            

        cv2.imshow("camera",frame)
        cv2.waitKey(5)
    
    

            
