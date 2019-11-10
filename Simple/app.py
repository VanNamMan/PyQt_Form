from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from libs.toolBar import ToolBar
from libs.utils import *
from libs.resources import *
from myLibs.cvLib import *
from dialog.settings_dlg import settingDialog
from dialog.AutoUI import AutoDlg
from dialog.ManualUI import ManualDlg
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

        self.menus = struct(
            tools=self.menu('&Tools'))
            # edit=self.menu('&Setting'),
            # view=self.menu('&View'),
            # help=self.menu('&Help'))

        action = partial(newAction, self)

        run = action('Start', self.run,
                      'alt+a', 'start', 'run camera real time')

        quit = action('Quit', self.close,
                      'alt+Q', 'quit', 'quit app')

        capture = action('Capture', self.capture,
                      'alt+c', 'capture', 'capture')

        addActions(self.menus.tools,
                   (run,capture,quit))

        # addActions(self.menus.edit,
        #            (config,))

        auto = action('Auto',self.swicthWidget,'', 'auto', 'run')
        manual = action('Manual', self.swicthWidget,'', 'manual', '')
        teaching = action('Teaching',self.swicthWidget,'', 'setting', '')
        data = action('Data', self.swicthWidget,'', 'data', '')

        self.actions = struct(run=run,auto=auto,manual=manual,
            teaching=teaching,data=data)

        tools = [auto,manual,teaching,data]
        myTools = self.toolbar("Control",tools) 


        # widget
        self.auto = AutoDlg(self)
        self.manual = ManualDlg(self)
        self.teaching = Master(defaultPrefdefClassFile="defaultFunc.txt")
        

        self.stacker = QStackedWidget(self)
        self.stacker.addWidget(self.auto)
        self.stacker.addWidget(self.manual)
        self.stacker.addWidget(self.teaching)

        self.setCentralWidget(self.stacker)

        #init
        self.initVar()

    def initVar(self):
        self.image = None
        self.bOpenCamera = False
        self.cap = None
        self.bLive = False

        self.bClock = True
        newThread(self.loopClock)

        self.initCamera()

    def initCamera(self):
        self.cap = cv2.VideoCapture(0)
        self.bOpenCamera = self.cap.isOpened()
        print("Camera 0 open : ",self.bOpenCamera)
    
    def liveCamera(self,cap):
        self.bLive = True
        while cap.isOpened():
            if self.bLive :
                ret,self.image = cap.read()
                if ret :
                    showImage(self.auto.frame,self.image)
                    newThread(self.processImage,(self.image,))
                    
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
        if self.image is None:
            return
        t0 = time.time()

        print("frame : ",image.shape[:2][::-1])
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        
        print("process-time/frame : ",time.time()-t0)

    def run(self):
        self.openCamera()
        pass

    def capture(self):
        folder = QFileDialog.getExistingDirectory(self,"Choose folder",os.getcwd(),QFileDialog.ShowDirsOnly)
        basename = os.path.basename(folder)

        filename = folder+"/%s.jpg"%basename
        # time.strftime("%d%m%y_%H%M%S.jpg")

        if self.bLive and self.image is not None:
            if cv2.imwrite(filename,self.image):
                print("image saved at %s"%filename)


    def swicthWidget(self):
        if self.sender() == self.actions.auto:
            self.stacker.setCurrentWidget(self.auto)
        elif self.sender() == self.actions.manual:
            self.stacker.setCurrentWidget(self.manual)
        elif self.sender() == self.actions.teaching:
            self.stacker.setCurrentWidget(self.teaching)

    def loadParameter(self,filename):

        pass

    def loopClock(self):
        while self.bClock:
            curtime = time.strftime("%H:%M:%S")
            self.auto.ui.clock.setText(curtime)
            time.sleep(1)

    def stopThread(self):
        self.bClock = False

    def closeEvent(self,ev):
        self.releaseCamera()
        self.stopThread()
        print("%s closed."%__appname__)