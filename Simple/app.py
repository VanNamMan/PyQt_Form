from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from libs.toolBar import ToolBar
from libs.utils import struct,newAction,addActions,newLabel
# from libs_.cvLib import *
from dialog.settings_dlg import settingDialog
from labelImg_master.labelImg import Master

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
        self.addToolBar(Qt.BottomToolBarArea, toolbar)
        return toolbar

class myApp(QMainWindow,WindowMixin):
    def __init__(self):
        super(myApp, self).__init__()
        self.setGeometry(QRect(0,0,640,480))
        self.setWindowTitle("%s - %s"%(__appname__,__version__))

        settingDialog(self).show()

        self.menus = struct(
            tools=self.menu('&Tools'))
            # edit=self.menu('&Setting'),
            # view=self.menu('&View'),
            # help=self.menu('&Help'))

        action = partial(newAction, self)

        run = action('Start', self.openCamera,
                      'alt+a', 'icon/start.ico', 'run camera real time')

        quit = action('Quit', self.close,
                      'alt+Q', 'icon/power-button.png', 'quit app')

        capture = action('Capture', self.capture,
                      'alt+c', 'icon/capture.png', 'capture')

        addActions(self.menus.tools,
                   (run,capture,quit))

        # addActions(self.menus.edit,
        #            (config,))

        auto = action('Auto',self.swicthWidget,'', 'icon/magic-wand.png', 'run')
        manual = action('Manual', self.swicthWidget,'', 'icon/User_Manual.png', '')
        teaching = action('Teaching',self.swicthWidget,'', 'icon/draw.png', '')
        data = action('Data', self.swicthWidget,'', 'icon/data2.ico', '')

        self.actions = struct(run=run,auto=auto,manual=manual,
            teaching=teaching,data=data)

        tools = [auto,manual,teaching,data]
        myTools = self.toolbar("Control",tools) 


        # auto
        auto = QWidget(self)
        layout = QVBoxLayout()
        self.frame = newLabel("Vision Master","color:white;background:black; font: bold 36px;qproperty-alignment: AlignCenter;")
        layout.addWidget(self.frame)
        auto.setLayout(layout)

        # manual
        teaching = Master(defaultPrefdefClassFile="defaultFunc.txt")
        
        self.widgets = struct(auto=auto,teaching=teaching)

        self.stacker = QStackedWidget(self)
        self.stacker.addWidget(auto)
        self.stacker.addWidget(teaching)

        self.setCentralWidget(self.stacker)

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
        if self.actions.run.text() == "Start":
            if self.cap is None:
                self.initCamera()
            if self.bOpenCamera:
                newThread(self.liveCamera,(self.cap,))
                self.actions.run.setText("Stop")
                self.actions.run.setIcon(QIcon("icon/stop.ico"))

        elif self.actions.run.text() == "Stop":
            self.bLive = False
            self.actions.run.setText("Start")
            self.actions.run.setIcon(QIcon("icon/start.ico"))


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

    def run(self):
        pass

    def capture(self):
        dialog = settingDialog(self)
        dialog.show()

    def swicthWidget(self):
        if self.sender() == self.actions.auto:
            self.stacker.setCurrentWidget(self.widgets.auto)
        elif self.sender() == self.actions.teaching:
            self.stacker.setCurrentWidget(self.widgets.teaching)


    def closeEvent(self,ev):
        self.releaseCamera()
        print("%s closed."%__appname__)