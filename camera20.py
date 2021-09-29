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
                e = (qr['e'],(x,y))
                endereco.append(e)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 15)
                text = "endereco ({}) type({})".format(e,barcodeType)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                
            elif (qr['e']) in endereco[0] and qr['p'] == 0 and len(endereco) > 0 :
                cv2.putText(frame,'na leitura !', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2) 
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 15)
                
            if endereco != []:
                


                if (y >= endereco[0][1][1] and y / endereco[0][1][1] < 53.5  and (endereco[0][1][1] / y ) <= 0.6) and (x / endereco[0][1][0] <= 1.45 and x / endereco[0][1][0] >= 0.489) and (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) == 0 and endereco != []:
                    e = ((qr['p'],qr['e']),(x,y))
                    produtos.append(e)
                    text = "produto ({}) type({})".format(e,barcodeType)
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 0), 15) 
            

                elif (y >= endereco[0][1][1] and y / endereco[0][1][1] < 53.5  and (endereco[0][1][1] / y ) <= 0.6) and (x / endereco[0][1][0] <= 1.45 and x / endereco[0][1][0] >= 0.489) and (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) > 0 and endereco != []:
                    print((qr['p'],qr['e']) , produtos[0])
                    cv2.putText(frame, '2 produtos no mesmo endereco!', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                
                elif (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) > 0:
                    cv2.putText(frame, '+de2 qr na leitura !', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
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
    
    

            
