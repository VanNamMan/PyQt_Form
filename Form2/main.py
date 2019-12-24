from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from header.mainUi import Ui_MainWindow
from paraDlg import*
from resultDlg import*

from libs_ import resources
from libs_.utils import *
from libs_.canvas import Canvas
from libs_.treeShape import TreeShapeDlg

import os,cv2,time,threading
import numpy as np
from functools import partial

__appname__ = "Vision Master"
__version__ = "1.1.0"
__date__ = "19.12.2019"
ext = ".png"

mkdir("Parameter")
mkdir("Image")

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

        # central widget
        self.stacker = QStackedWidget(self)

        self.autoWidget = QWidget(self)
        hlayout = QHBoxLayout()
        self.frame_display = Canvas(self)
        self.frame_result = Canvas(self)
        self.resultDlg = ResultDlg()
        self.resultDlg.setMaximumWidth(300)
        addWidgets(hlayout,[self.resultDlg,self.frame_display,self.frame_result])
        self.autoWidget.setLayout(hlayout)

        self.teachWidget = QWidget(self)
        self.canvas = Canvas(self)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.teachWidget.setLayout(layout)

        self.stacker.addWidget(self.autoWidget)
        self.stacker.addWidget(self.teachWidget)

        self.setCentralWidget(self.stacker)

        dockFeatures = QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable

        self.paraDlg = ParaDlg()
        self.paraDlg.saveConfigSignal.connect(self.saveConfigRequest)
        self.paraDlg.loadConfigSignal.connect(self.loadConfigRequest)

        self.paraDock = QDockWidget('parameter', self)
        self.paraDock.setWidget(self.paraDlg)
        self.paraDock.setFeatures(dockFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.paraDock)
        toggleParaDock = self.paraDock.toggleViewAction()
        self.paraDock.setMinimumWidth(200)
        self.paraDock.hide()

        self.treeShape = TreeShapeDlg(self)

        self.treeDock = QDockWidget('listShape', self)
        self.treeDock.setWidget(self.treeShape)
        self.treeDock.setFeatures(dockFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.treeDock)
        toggleParaTree = self.treeDock.toggleViewAction()
        self.treeDock.setMinimumWidth(200)
        self.treeDock.hide()
        #  action
        action = partial(newAction,self)
        auto = action("auto",self.showAuto,"a","home")
        teaching = action("teaching",self.showTeaching,"s","teach")
        addActions(self.ui.menuSetting,[auto,teaching,toggleParaDock,toggleParaTree])
        # triggered
        self.ui.actionopen.setShortcut("ctrl+o")
        self.ui.actiondraw.setShortcut("w")
        addTriggered(self.ui.actionopen,self.openFile)
        addTriggered(self.ui.actiondraw,self.drawing)
        # Icon
        self.ui.actionopen.setIcon(newIcon("open"))
        self.ui.actionsave.setIcon(newIcon("save"))
        self.ui.actionexit.setIcon(newIcon("quit"))
        self.ui.actionversion.setIcon(newIcon("version"))
        self.ui.actioninfomation.setIcon(newIcon("info"))
        self.ui.actiondraw.setIcon(newIcon("draw"))

        self.resultDlg.ui.but_start.setIcon(newIcon("start"))
        self.resultDlg.ui.but_stop.setIcon(newIcon("stop"))
        self.resultDlg.ui.but_reset.setIcon(newIcon("reset"))
        toggleParaDock.setIcon(newIcon("setting"))
        toggleParaTree.setIcon(newIcon("shape"))

        # tracking , signal teaching
        self.canvas.setTracking(True)
        self.canvas.newShapeSignal.connect(self.treeShape.newShape)
        self.canvas.deleteShapeSignal.connect(self.treeShape.deleteShape)
        self.canvas.selectedShapeSignal.connect(self.treeShape.selectedShape)
        # 
        self.statusSignal.connect(self.statusRequest)
        self.ui.actionopen.setEnabled(False)
        self.ui.actiondraw.setEnabled(False)
        # variable
        self.mInput = None
        self.paraDlg.update()
        self.statusSignal.emit(self.OK)
    
    def addLog(self,text):
        text = "%s %s"%(getStrTime(),text)
        self.resultDlg.ui.listWidget.addItem(text)

    def showTracking(self,text):
        self.lbCoor.setText(text)

    def showTeaching(self):
        self.stacker.setCurrentWidget(self.teachWidget)
        self.ui.actionopen.setEnabled(True)
        self.ui.actiondraw.setEnabled(True)

        self.treeDock.show()
        self.paraDock.show()
    
    def showAuto(self):
        self.stacker.setCurrentWidget(self.autoWidget)
        self.ui.actionopen.setEnabled(False)
        self.ui.actiondraw.setEnabled(False)

        self.treeDock.hide()
        self.paraDock.hide()
    
    def drawing(self):
        if self.canvas.image is not None:
            self.canvas.setEditing(not self.canvas.edit)
            self.canvas.drawing = False
            self.canvas.setEnableMenu(False)
            self.canvas.drawShapes(self.canvas.image.copy())

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
        ,"Image File (*.jpg *.png *.bmp)")
        if filename:
            print(filename)
            self.mInput = cv2.imread(filename,0)
            self.canvas.showImage(self.mInput)
            self.statusBar().showMessage(filename)
    
    def saveConfigRequest(self,bSave):
        if(bSave):
            QMessageBox.information(self,"Save Parameter","Done Save Parameter ")
        else:
            QMessageBox.information(self,"Save Parameter","Save Parameter Fail")

    def loadConfigRequest(self,bLoad):
        if(bLoad):
            QMessageBox.information(self,"Load Parameter","Done Load Parameter ")
        else:
            QMessageBox.information(self,"Load Parameter","Load Parameter Fail")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = mainWindow()
    MainWindow.showNormal()
    sys.exit(app.exec_())

