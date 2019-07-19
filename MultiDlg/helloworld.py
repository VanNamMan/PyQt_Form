from PyQt5.QtWidgets import QMainWindow,QDialog, QMessageBox,QWidget, QApplication,QMenu,QAction,QFileDialog,QToolBar
from PyQt5.QtCore import Qt, QObject, QSize, QRect,QPoint
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QResizeEvent,QImage,QPixmap,QCloseEvent,QIcon
from ui_helloworld import Ui_HelloWorldDlg
from autodlg import AutoDlg
from manualdlg import ManualDlg
from teachdlg import TeachDlg
from datadlg import DataDlg
import cv2
import threading,time,os
import numpy as np
from scipy import misc
from PIL import ImageQt

import sfile
import vision as vs

class HelloWorld(QMainWindow):
    def __init__(self):
        super(HelloWorld, self).__init__(None)
        self.setWindowFlags(Qt.Window)
        self.ui = Ui_HelloWorldDlg()
        self.ui.setupUi(self)

        self.m_auto = AutoDlg(self)
        self.m_manual = ManualDlg(self)
        self.m_teach = TeachDlg(self)
        self.m_data = DataDlg(self)
        self.ui.mdiArea.addSubWindow(self.m_auto, Qt.FramelessWindowHint)
        self.ui.mdiArea.addSubWindow(self.m_manual, Qt.FramelessWindowHint)
        self.ui.mdiArea.addSubWindow(self.m_teach, Qt.FramelessWindowHint)
        self.ui.mdiArea.addSubWindow(self.m_data, Qt.FramelessWindowHint)

        self.show()
        self.m_auto.showMaximized()
        #self.m_manual.setEnabled(False)

        btns = [self.ui.but_Auto,self.ui.but_Manual,self.ui.but_Teach,self.ui.but_Data]
        icons = ["res/auto.png","res/manual.png","res/setting.png","res/data.png"]
        for i,btn in enumerate(btns):
            btn.clicked.connect(self.UpdateUI)
            btn.setIconSize(QSize(64,64))
            btn.setIcon(QIcon(icons[i]))
        
        # Auto
        self.m_auto.ui.but_Start.clicked.connect(self.ProcessEvent)
        self.m_auto.ui.but_Stop.clicked.connect(self.ProcessEvent)
        self.m_auto.ui.but_Reset.clicked.connect(self.ProcessEvent)

        # Teach
        self.m_teach.ui.widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.m_teach.ui.widget.customContextMenuRequested.connect(self.selectMenu)


        self.OninitDialog()

        
    def OninitDialog(self):
        pass
    def openFileNameDialog(self):    
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fileName, _ = QFileDialog.getOpenFileName(self,"Slect File", "","All Files (*);;Image Files (*.jpg)", options=options)
        fileName, _ = QFileDialog.getOpenFileName(self,"Slect File", "","All Files (*);;Image Files (*.jpg)")
        
        return fileName

    def openFolderNameDialog(self,sDir="D:\\"):    
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory",sDir))
        return folder
    # 
    def getStrDateTime(self):
        return time.strftime("%d%m%y_%H%M%S")
    
    def valuechange(self):
        pass

    def cbbSelection(self):
        pass
    def savePara(self,parameter,filename):
        pass
    def updateSetting(self,parameter):
        pass
    def loadPara(self,filepara):
        
        pass

    def selectMenuListWidget(self,point):
        menu = QMenu(self.m_teach)
        clear = QAction("Clear", self)
        menu.addAction(clear)

        parent_point = point+self.m_teach.ui.tabWidget.pos()+self.m_teach.ui.listWidget.pos()+QPoint(10,10)
        action = menu.exec_(self.mapToParent(parent_point))

        if action == clear:
            n = self.m_teach.ui.listWidget.count()
            for i in range(n):      
                self.m_teach.ui.listWidget.takeItem(0)
            pass
        pass
    def selectMenu(self,point):
        menu = QMenu(self.m_teach)

        tools = menu.addMenu("Add...")
        addRect = QAction("Rect", self)
        
        tools.addAction(addRect)

        tools = menu.addMenu("Function...")
        # addOCR = QAction("OCR",self)
        addBarcode = QAction("Barcode",self)
        tools.addAction(addBarcode)

        save = menu.addAction("Save")
        clearAll = menu.addAction("Clear All")


        toolsPSM = tools.addMenu("&OCR")
        addOCR = []
        num_oem = 4
        num_psm = 14
        for oem in range(num_oem):
            toolOem = toolsPSM.addMenu("&oem %d"%oem)
            for psm in range(num_psm):
                act = QAction("psm %d"%psm,self)
                toolOem.addAction(act) 
                addOCR.append(act)

        parent_point = point+self.m_teach.ui.widget.pos()+QPoint(10,10)

        action = menu.exec_(self.mapToParent(parent_point))

        if action == addRect:
            if self.m_teach.globalRectCrop:
                self.m_teach.listGlobalRectCrop.append(self.m_teach.globalRectCrop)
                self.m_teach.listCvRectCrop.append(self.m_teach.cvRectCrop)
                self.m_teach.globalRectCrop = None
            pass
        elif action == save:
            filename = "data/"+self.getStrDateTime()+".jpg"
            self.m_teach.qImage.copy(self.m_teach.cvRectCrop).save(filename)
            pass
        elif action == clearAll:
            self.m_teach.drawing = False
        elif action in addOCR:
            index = addOCR.index(action)
            psm = index%num_psm
            oem = index//num_psm
            pass
        elif action == addBarcode:
            t0 = time.time()
            x,y,w,h = self.V.cvRect
            roi = self.V.imgTeach[y:y+h,x:x+w]
            txt = vs.get_matrixCode(roi)
            dt = time.time() - t0
            self.log(self.m_teach.ui.listWidget,"dt : %.2f"%dt)
            self.log(self.m_teach.ui.listWidget,txt)
            pass


    def threadTimer(self):
        self.V.bTimer = True
        thread = threading.Thread(target=self.loopTimer)
        thread.start()
    def loopTimer(self):
        while self.V.bTimer :
            self.V.strTime = time.strftime("%H:%M:%S")
            time.sleep(1)
            self.m_auto.ui.lb_timer.setText(self.V.strTime)
    def threadLiveCam(self,idCam,frame):
        thread = threading.Thread(target=self.loopCam,args=(idCam,frame))
        thread.start()
    def loopCam(self,idCam,frame):
        pass
    def mkDir(self,folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
    def threadProcess(self):
        thread = threading.Thread(target=self.loopProcess)
        thread.start()
        pass
    def loopProcess(self):
        pass
    def onClickButStart(self):
        pass
    def onClickButStop(self):
        pass
    def onClickButReset(self):
        pass
    def onClickButLoadImage(self):
        file_name = self.openFileNameDialog()
        if file_name == "":
            return
    def ProcessEvent(self):
        #AUTO
        if self.sender()==self.m_auto.ui.but_Start:
            self.onClickButStart()
            pass
        elif self.sender() == self.m_auto.ui.but_Stop:    
            self.onClickButStop()
            pass
        elif self.sender() == self.m_auto.ui.but_Reset:    
            self.onClickButReset()
            pass
    # log , showImage 
    def log(self,idlog,text):
        strtime = time.strftime("%H:%M:%S : ")
        text = strtime+str(text)
        idlog.addItem(text)
    def showImage(self,frame,pic):
        h,w = pic.shape[0],pic.shape[1]
        hFrame,wFrame = frame.height(),frame.width()
        img = cv2.resize(pic,(wFrame,hFrame))

        if len(pic.shape) == 2:
            qPix = QPixmap.fromImage(ImageQt.ImageQt(misc.toimage(img)))
            
        else:
            ch = 3
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            qImg = QImage(img.data,wFrame,hFrame,ch*wFrame,QImage.Format_RGB888)
            qPix = QPixmap(qImg)
            
        frame.setPixmap(qPix)
    # Resize , update UI
    bFirst = True
    baseRectElement = []
    widgets = []
    bazeSize = QSize
            
    def resizeEvent(self, QResizeEvent):
        if self.bFirst:
            self.bFirst = False
            self.bazeSize = self.window().size()
            self.widgets = self.window().findChildren(QWidget)
            for widget in self.widgets:
                self.baseRectElement.append(widget.geometry())
            return

        dScaleW = self.window().width() / self.bazeSize.width()
        dScaleH = self.window().height() / self.bazeSize.height()

        for i in range(0, len(self.widgets)):
            rect = self.baseRectElement[i]
            widget = self.widgets[i]
            newRect = QRect(dScaleW * rect.left(), dScaleH * rect.top(), dScaleW * rect.width(),
                            dScaleH * rect.height())
            widget.setGeometry(newRect)
            widget.updateGeometry()
        return

    def UpdateUI(self):
        if self.sender() == self.ui.but_Auto:
            self.m_auto.showMaximized()
        elif self.sender() == self.ui.but_Manual:
            self.m_manual.showMaximized()
        elif self.sender() == self.ui.but_Teach:
            self.m_teach.showMaximized()
        elif self.sender() == self.ui.but_Data:
            self.m_data.showMaximized()
    # 
    def closeEvent(self,QCloseEvent):
        pass
    def __del__(self):
        self.ui     = None
