import cv2,time
import numpy as np
from pyzbar import pyzbar

from PyQt5.QtGui import QImage,QPixmap

def readCode(image):
	barcodes = pyzbar.decode(image)
	return [{"data":code.data.decode("utf-8") 
			, "rect" : code.rect 
			, "type" : code.type} for code in barcodes]


def showImage(label,image):
	width , height = label.width(),label.height()

	h,w,channel = image.shape

	s = min(width/w,height/h)

	new_w = int(w*s)
	new_h = int(h*s)

	# t0 = time.time()
	new_img = cv2.resize(image,(new_w,new_h))
	new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
	# print(time.time()-t0)
	qim = QImage(new_img.data,new_w,new_h,channel*new_w, QImage.Format_RGB888)
	# qim = QImage(image.data,w,h,channel*w, QImage.Format_RGB888)

	qpix = QPixmap(qim)

	label.setPixmap(qpix)
