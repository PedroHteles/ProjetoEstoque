import cv2
from pyzbar.pyzbar import decode
import json
import numpy

webcam = cv2.VideoCapture(0)
img = cv2.imread('./img/dirnal.png')

produtos = []
endereco = []
def lerqr(x,height,width):
    # print(((height - (height * 0.55)) / 2),(width - (width * 0.55))/ 2)

    start_point = (int(width / 4), int(height  / 4))
    end_point = (int(width / 1.35), int(height / 1.35))
    color = (255, 0, 0)
    thickness = 2
    cv2.rectangle(img, start_point, end_point, color, thickness)

    for barcode in decode(x):
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        try:
            qr = json.loads(barcodeData)
            # print(qr,y < int(height / 1.35) and y > int(height / 4))
            
            if x < int(width / 1.35) and x > int(width / 4) and y < int(height / 1.35) and y > int(height / 4) and (qr['e']) not in endereco and qr['p'] == 0 and len(endereco) == 0:
                e = ((qr['e']),(x,y))
                endereco.append(e)
            elif x < int(width / 1.35) and x > int(width / 4) and y < int(height / 1.35) and y > int(height / 4) and (qr['p'],qr['e']) not in produtos and qr['p'] > 0 and len(produtos) == 0 and endereco !=[]:
                p = ((qr['p'],qr['e']),(x,y))
                produtos.append(p)
            
            
            if x < int(width / 1.35) and x > int(width / 4) and (qr['e']) and qr['p'] == 0 and qr['e'] == endereco[0][0] :
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 1)

            
            if x < int(width / 1.35) and x > int(width / 4) and qr['p'] > 0 and (qr['p'],qr['e']) == produtos[0][0]:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 5)

        except:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

while True:
    img = cv2.imread('./img/dirnal.png')
    height, width, channels = img.shape
    lerqr(img,height,width)
        
    cv2.imshow("camera",img)
    key = cv2.waitKey(5)
    if key == 27:
        break
    
    

            
