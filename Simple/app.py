from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from libs.toolBar import ToolBar
from libs.utils import *

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

        tools = [action('Auto',None,'Ctrl+Q', 'icon/magic-wand.png', 'run'),
                    action('Manual', None,'Ctrl+Q', 'icon/User_Manual.png', ''),
                    action('Setting', None,'Ctrl+Q', 'icon/setting.png', ''),
                    action('Data', None,'Ctrl+Q', 'icon/data2.ico', '')]
        myTools = self.toolbar("Tools",tools) 

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        self.frame = newWidget(self,QLabel,"Vision Master","color:white;background:black; font: bold 36px;qproperty-alignment: AlignCenter;")
        layout.addWidget(self.frame)
        widget.setLayout(layout)

               
    
    def openCamera(self):
        pass
    def openFile(self):
        path = os.getcwd()
        filters = "Open Image file (%s)" % ' '.join(['*.jpg',"*.png"])
        filename,_ = QFileDialog.getOpenFileName(self,'%s - Choose a Image file' % __appname__, path, filters)
        if filename:
            showImage(self.frame,cv2.imread(filename))