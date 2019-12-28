from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

import cv2,os,time,threading,sys
import pandas as pd
import numpy as np
from configparser import ConfigParser
from argparse import ArgumentParser
import re
import serial
from functools import partial
from qimage2ndarray import *

from scipy import misc
from PIL import ImageQt

class HashableQListWidgetItem(QListWidgetItem):

    def __init__(self, *args):
        super(HashableQListWidgetItem, self).__init__(*args)

    def __hash__(self):
        return hash(id(self))

class Port(serial.Serial):
    def __init__(self,port="COM1",baud=9600,prefix="@",suffix="\r\n",_timeout=0.01):
        super(Port,self).__init__(port,baud)
        self.prefix = prefix
        self.suffix = suffix
        self.data = ""
        self._timeout = 0.01
    
    def isMessage(self,data):
        return re.findall(self.prefix,data) and re.findall(self.suffix,data)
    
    def splitData(self,data):
        start = re.search(self.prefix,data).end()
        end = re.search(self.suffix,data).start()
        return data[start:end]

class struct(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def getStrDateTime():
    return time.strftime("%d%m%y_%H%M%S")

def getStrTime():
    return time.strftime("%H:%M:%S")
def inSide(x,tup):
    m,M = tup
    if m == -1:
        return x < M
    elif M == -1:
        return m < x
    else :
        return m < x < M
def drawRect(mat,box,color=(0,255,0),lw=2):
    x,y,w,h = box
    cv2.rectangle(mat,(x,y),(x+w,y+h),color,lw)

def drawText(mat,text,org,color=(0,255,0),fs=1,lw=2):
    cv2.putText(mat,text,org,cv2.FONT_HERSHEY_COMPLEX,fs,color,lw)

def distance(v1,v2):
    assert len(v1)==len(v2),print("v1,v2 need same length")
    v = np.array([v2[i] - v1[i] for i in range(len(v1))])
    return np.sqrt(np.sum(np.square(v)))

def str2ListInt(string):
    lst = string.split(",")
    return [int(l) for l in lst]

def addItems(cbb,items):
    [cbb.addItem(it) for it in items]

def newCbb(items,parent):
    cbb = QComboBox(parent)
    addItems(cbb,items)
    return cbb

def newIcon(icon):
    return QIcon(':/' + icon)

def addActions(menu,actions):
    for act in actions:
        if isinstance(act,QAction):
            menu.addAction(act)
        else:
            menu.setMenuBar(act)

def newCbb(items,slot=None):
    cbb = QComboBox()
    [cbb.addItem(item) for item in items]
    if slot is not None:
        cbb.activated.connect(slot)
    return cbb
def newButton(text,slot=None,icon=None):
    b = QPushButton(text)
    if slot is not None:
        b.clicked.connect(slot)
    if icon is not None:
        b.setIcon(newIcon(icon))
    
    return b

def addWidgets(layout,wds):
    for w in wds:
        if isinstance(w,QWidget):
            layout.addWidget(w)
        else:
            layout.addLayout(w)

def addTriggered(action,trigger):
    action.triggered.connect(trigger)

def newAction(parent,text,slot=None,shortcut=None,icon=None,enabled=True):
    a = QAction(text,parent)
    if icon is not None:
        a.setIcon(newIcon(icon))
    if shortcut is not None:
        a.setShortcut(shortcut)
    if slot is not None:
        a.triggered.connect(slot)
    a.setEnabled(enabled)
    return a

def mkdir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def runThread(target,args):
    thread = threading.Thread(target=target,args=args)
    thread.start()

def showImage(image,label):
    width , height = label.width(),label.height()

    h,w = image.shape[:2]

    s = min(width/w,height/h)

    new_w = int(w*s)
    new_h = int(h*s)

    # t0 = time.time()
    new_img = cv2.resize(image,(new_w,new_h))
    # print(time.time()-t0)
    if len(image.shape) == 2:
        new_img = cv2.cvtColor(new_img, cv2.COLOR_GRAY2RGB)
        qpix = QPixmap.fromImage(ImageQt.ImageQt(misc.toimage(new_img)))
    else:
        channel = image.shape[-1]
        new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
        qim = QImage(new_img.data,new_w,new_h,channel*new_w, QImage.Format_RGB888)
        qpix = QPixmap(qim)

    label.setPixmap(qpix)

    return s

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    wd = QMainWindow()
    canvas = Canvas(wd)
    wd.setCentralWidget(canvas)
    wd.show()
    sys.exit(app.exec_())
    