from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from header.mainUi import Ui_MainWindow
from paraDlg import*
from resultDlg import*

from libs_ import resources
from libs_.utils import *

import os,cv2,time,threading
import numpy as np

__appname__ = "Vision Master"
__version__ = "1.1.0"
__date__ = "19.12.2019"

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

class mainWindow(QMainWindow):
    NORMAL = -1
    NG = 0
    OK = 1
    normStyle = "background:yellow;font:bold 72px"
    ngStyle = "background:red;font:bold 72px"
    okStyle = "background:green;font:bold 72px"
    statusSignal = pyqtSignal(int)
    def __init__(self):
        super(mainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.lbCoor = QLabel("")
        self.setWindowTitle("Automation2G-SEV Vision Master")
        self.setWindowIcon(newIcon("app"))
        self.statusBar().showMessage('%s %s' % (__appname__,__version__))
        self.statusBar().addPermanentWidget(self.lbCoor)

        dockFeatures = QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable

        self.paraDlg = ParaDlg()

        self.paraDock = QDockWidget('parameter', self)
        self.paraDock.setWidget(self.paraDlg)
        self.paraDock.setFeatures(dockFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.paraDock)
        self.toggleParaDock = self.paraDock.toggleViewAction()
        self.paraDock.setMinimumWidth(200)
        self.ui.menuSetting.addAction(self.toggleParaDock)

        self.paraDock.hide()

        self.central = QWidget(self)
        hlayout = QHBoxLayout()
        self.frame_display = QLabel("")
        self.frame_display.setStyleSheet("background:black")
        self.frame_result = QLabel("")
        self.frame_result.setStyleSheet("background:black")
        self.resultDlg = ResultDlg()
        self.resultDlg.setMaximumWidth(300)
        addWidgets(hlayout,[self.resultDlg,self.frame_display,self.frame_result])
        self.central.setLayout(hlayout)

        self.setCentralWidget(self.central)

        # Icon
        self.ui.actionopen.setIcon(newIcon("open"))
        self.ui.actionsave.setIcon(newIcon("save"))
        self.ui.actionexit.setIcon(newIcon("quit"))
        self.ui.actionversion.setIcon(newIcon("version"))
        self.ui.actioninfomation.setIcon(newIcon("info"))
        self.toggleParaDock.setIcon(newIcon("setting"))

        self.resultDlg.ui.but_start.setIcon(newIcon("start"))
        self.resultDlg.ui.but_stop.setIcon(newIcon("stop"))
        self.resultDlg.ui.but_reset.setIcon(newIcon("reset"))
        # 
        self.statusSignal.connect(self.statusRequest)
        self.statusSignal.emit(self.NG)

        # triggered
        addTriggered(self.ui.actionopen,self.openFile)

        # treeWidget
        # variable
        self.mInput = None
    
    def statusRequest(self,stt):
        if stt == self.NORMAL :
            self.resultDlg.ui.lb_result.setStyleSheet(self.normStyle)
            self.resultDlg.ui.lb_result.setText("Wait")
        elif stt == self.NG :
            self.resultDlg.ui.lb_result.setStyleSheet(self.ngStyle)
            self.resultDlg.ui.lb_result.setText("NG")
        elif stt == self.OK :
            self.resultDlg.ui.lb_result.setStyleSheet(self.okStyle)
            self.resultDlg.ui.lb_result.setText("OK")
        pass
    
    def openFile(self):
        filename,_ = QFileDialog.getOpenFileName(self,"Select Image File",os.getcwd()
        ,"Image File (*.jpg)")
        if filename:
            print(filename)
            self.mInput = cv2.imread(filename)
            showImage(self.mInput,self.frame_display)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = mainWindow()
    MainWindow.showMaximized()
    sys.exit(app.exec_())

