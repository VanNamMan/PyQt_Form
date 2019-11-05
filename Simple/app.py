from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from libs.toolBar import ToolBar
from libs.utils import *
from libs.cvLib import *
from dialog.settings_dlg import setting

import cv2
import numpy as np
import pandas as pd
import sys,os,time,threading

from configparser import ConfigParser
from functools import partial

__appname__ = "Vision Master"
__version__ = "1.1.0"

class WindowMixin(object):

    def menu(self, title, actions=None):
        menu = self.menuBar().addMenu(title)
        if actions:
            addActions(menu, actions)
        return menu

    def toolbar(self, title, actions=None):
        toolbar = ToolBar(title)
        toolbar.setObjectName(u'%sToolBar' % title)
        # toolbar.setOrientation(Qt.Vertical)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if actions:
            addActions(toolbar, actions)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        return toolbar

class myApp(QMainWindow,WindowMixin):
    def __init__(self):
        super(myApp, self).__init__()
        self.setGeometry(QRect(0,0,640,480))
        self.setWindowTitle("%s - %s"%(__appname__,__version__))

        self.menus = struct(
            file=self.menu('&File'),
            edit=self.menu('&Edit'),
            view=self.menu('&View'),
            help=self.menu('&Help'))

        action = partial(newAction, self)

        openfile = action('Open', self.openFile,
                      'Ctrl+O', 'icon/open-file.png', 'open Image File')

        quit = action('Quit', self.close,
                      'Ctrl+Q', 'icon/power-button.png', 'quitApp')

        addActions(self.menus.file,
                   (openfile, quit))

        start = action('Start',self.openCamera,'', 'icon/magic-wand.png', 'run')
        manual = action('Manual', None,'', 'icon/User_Manual.png', '')
        settings = action('Setting',self.openSettings,'', 'icon/setting.png', '')
        data = action('Data', None,'', 'icon/data2.ico', '')

        self.actions = struct(openfile=openfile,quit=quit,start=start,manual=manual,
            settings=settings,data=data)

        tools = [start,manual,settings,data]
        myTools = self.toolbar("Tools",tools) 

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        self.frame = newWidget(self,QLabel,"Vision Master","color:white;background:black; font: bold 36px;qproperty-alignment: AlignCenter;")
        layout.addWidget(self.frame)
        widget.setLayout(layout)

        #init
        self.initVar()

    def initVar(self):
        self.bOpenCamera = False
        self.cap = None
        self.bLive = False

        self.initCamera()

    def initCamera(self):
        self.cap = cv2.VideoCapture(0)
        self.bOpenCamera = self.cap.isOpened()
        print("Camera 0 open : ",self.bOpenCamera)
    
    def liveCamera(self,cap):
        self.bLive = True
        while cap.isOpened():
            if self.bLive :
                ret,image = cap.read()
                if ret :
                    newThread(self.processImage,(image,))
                    
            time.sleep(0.005)

    def openCamera(self):
        if self.actions.start.text() == "Start":
            if self.cap is None:
                self.initCamera()
            if self.bOpenCamera:
                newThread(self.liveCamera,(self.cap,))
                self.actions.start.setText("Stop")
                self.actions.start.setIcon(QIcon("icon/stop.ico"))

        elif self.actions.start.text() == "Stop":
            self.bLive = False
            self.actions.start.setText("Start")
            self.actions.start.setIcon(QIcon("icon/magic-wand.png"))


    def releaseCamera(self):
        if self.cap is not None:
            self.bLive = False
            self.cap.release()
            print("camera closed.")

    def processImage(self,image):
        t0 = time.time()

        print("frame : ",image.shape[:2][::-1])
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        showImage(self.frame,hsv)
        
        print("process-time/frame : ",time.time()-t0)

    def openFile(self):
        path = os.getcwd()
        filters = "Open Image file (%s)" % ' '.join(['*.jpg',"*.png"])
        filename,_ = QFileDialog.getOpenFileName(self,'%s - Choose a Image file' % __appname__, path, filters)
        if filename:
            image = cv2.imread(filename)
            showImage(self.frame,image)
            def func(image):
                print(readCode(image))
            newThread(func,(image,))

    def openSettings(self):
        dialog = setting(self)
        dialog.show()

    def closeEvent(self,ev):
        self.releaseCamera()
        print("%s closed."%__appname__)