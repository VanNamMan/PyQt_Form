from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import cv2,time
import numpy as np
import threading 

class struct(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def newIcon(path):
    return QIcon(path)

def newAction(parent, text, slot=None, shortcut=None, icon=None,
              tip=None, checkable=False, enabled=True):
    """Create a new action and assign callbacks, shortcuts, etc."""
    a = QAction(text, parent)
    if icon is not None:
        a.setIcon(newIcon(icon))
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    return a

def addActions(widget, actions):
    for action in actions:
        if action is None:
            widget.addSeparator()
        elif isinstance(action, QMenu):
            widget.addMenu(action)
        else:
            widget.addAction(action)

def newWidget(parent,widget,text,style=None):
    try:
        w = widget(text,parent)
    except:
        w = widget(parent)
    if style is not None:
       w.setStyleSheet(style)
    return w

def newButton(parent,text,slot=None):
    but = QPushButton(text,parent)
    if slot is not None:
        but.clicked.connect(slot)

    return but

def showImage(label,image):
    
    hF,wF = label.height(),label.width()
    h,w,*channel = image.shape

    s = min(hF/h,wF/w)
    new_W = int(max(w*s - 2,1))
    new_H = int(max(h*s - 2,1))
    print(new_H,new_W)
    # rgb = np.array(image,copy=True)
    rgb = image.copy()

    rgb = cv2.resize(rgb,(new_W,new_H))

    height, width,*channel = rgb.shape
    if channel[0] == 3 :
        rgb = cv2.cvtColor(rgb,cv2.COLOR_BGR2RGB)
    else:
        rgb = cv2.cvtColor(rgb,cv2.COLOR_GRAY2RGB)

    bytesPerLine = 3 * width
    qImg = QImage(rgb.data, width, height, bytesPerLine, QImage.Format_RGB888)
    label.setPixmap(QPixmap(qImg))

def newThread(target,args=()):
    myThread = threading.Thread(target=target,args=args)
    myThread.start()