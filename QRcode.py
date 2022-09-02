import numpy as np,cv2,sys
import pyqrcode,random,os
from PIL import Image
from pyzbar.pyzbar import decode

def QRcodeGenerator():
    rand = '0x' + str(random.getrandbits(64))
    try:
        with open('AuthCode.txt') as t:
            myDataList = t.read().splitlines()
        if rand in myDataList:
            rand = '0x' + str(random.getrandbits(64))
    except:
        f = open('AuthCode.txt','a')
        f.write(str(rand) + '\n')
        f.close()
    qr = pyqrcode.create(rand)
    qr.png('test.png', scale=10)
    im = Image.open(r'test.png')
    im.show()
    #cc = cv2.imread('test.png')
    #cv2.imshow('QR Code', cc)
    cv2.waitKey(5)
    os.remove('test.png')

def QRcodeChecker():
    try:
        with open('AuthCode.txt') as t:
            myDataList = t.read().splitlines()
    except:
        print('First make an entry\nGenerating QR Code')
        QRcodeGenerator()
        with open('AuthCode.txt') as t:
            myDataList = t.read().splitlines()
        pass
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    while True:
        success, img = cap.read()
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            if myData in myDataList:
                myOp = 'Authorised'
                myColor = (0,255,0)
            else:
                myOp = 'Un-Authorised'
                myColor = (0,0,255)
            print(myOp)
            pts = np.array([barcode.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(img,[pts],True,myColor,5)
            pts2 = barcode.rect
            #cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
            cv2.putText(img, myOp, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)
        cv2.imshow('Result',img)
        cp = cv2.waitKey(1)
        if cp & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    while True:
        ch = int(input("\n1. Get QR Code\n2. QR Checker\n3. Exit\nEnter Your Choice: "))
        if ch == 1:
            QRcodeGenerator()
        elif ch == 2:
            QRcodeChecker()
        elif ch == 3:
            sys.exit()
        else:
            print('Invalid')