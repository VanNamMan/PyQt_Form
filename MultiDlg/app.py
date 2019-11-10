from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import time,os,threading
import cv2
import numpy as np

from libs.utils import *

__appname__ = "Check Hole"
__version__ = "1.0"


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

class MyApp(QMainWindow,WindowMixin):
	def __init__(self):
		super(MyApp,self).__init__()


	def initVar(self):
		pass

	def initUI(self):
		layout = QVBoxLayout()


		pass

	def closeEvent(self,ev):
		print("%s closed."%__appname__)


if __name__ == "__main__":
	import sys
    a = QApplication(sys.argv)
    w = MyApp()
    w.showMaximized()
    a.exec_()
