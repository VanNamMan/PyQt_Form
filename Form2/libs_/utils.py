from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

import cv2,os,time,threading
import pandas as pd
import numpy as np

def mkdir(folder):
	os.makedirs(folder)

def runThread(target,args):
    thread = threading.Thread(target=target,args=args)
    thread.start()

def showImage(image,label):
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

if __name__ == "__main__":
    print("utils")
    pass
