from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

import cv2,os,time,threading
import pandas as pd
import numpy as np

def getStrDateTime():
	return time.strftime("%d%m%y_%H%M%S")

def getStrTime():
	return time.strftime("%H:%M:%S")

def newIcon(icon):
    return QIcon(':/' + icon)

def addActions(menu,actions):
    for act in actions:
        menu.addAction(act)

def addWidgets(layout,wds):
    for w in wds:
        layout.addWidget(w)

def addTriggered(action,trigger):
    action.triggered.connect(trigger)

def newAction(parent,text,slot=None,shortcut=None,icon=None):
	a = QAction(text,parent)
	if icon is not None:
		a.setIcon(newIcon(icon))
	if shortcut is not None:
		a.setShortcut(shortcut)
	if slot is not None:
		a.triggered.connect(slot)
	return a

def mkdir(folder):
	if not os.path.exists(folder):
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

	return s

if __name__ == "__main__":
    print("utils")
    pass
