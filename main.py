import cv2
import pyqrcode,random

rand = '0x' + str(random.getrandbits(64))
qr = pyqrcode.create(rand)
qr.png('test.png', scale=120)
cc = open('test.png')
cv2.imshow('QR Code', cc)
cv2.waitKey(1)