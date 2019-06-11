from PyQt5.QtWidgets import QDialog,QMainWindow, QMessageBox, QWidget, QApplication,QFileDialog,QMenu,QAction,QTableWidgetItem
from PyQt5.QtCore import Qt, QObject, QSize, QRect,QPoint
from PyQt5.QtCore import*
import PyQt5.QtWidgets 
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QResizeEvent,QImage,QPixmap,QCloseEvent,QIcon
from PyQt5 import QtGui
from PIL import ImageQt
from scipy import misc
from multiprocessing.dummy import Pool
import threading

from ui_helloworld import Ui_HelloWorldDlg
from frame import FrameDlg

from setting import Setting

from pypylon import pylon,genicam
import cv2,os,time,json,sfile
import numpy as np
import vision as vs
import serial
# import matplotlib
# matplotlib.use("TkAgg")


DINO = "Dino"
BASLER = "Basler"

FILE_PARAMS = 'parameter/params.json'

class rect():
    def __init__(self):
        self.tl = [0,0]
        self.br = [0,0]
        self.r = self.tl+self.br
class params():
    def __init__(self):
        # self.kthresh = 100
        # self.rect = []
        # self.name = ""
        # self.width = [-1,-1]
        # self.height = [-1,-1]
        # self.area = [-1,-1]
        pass   
class HelloWorld(QMainWindow):
    def __init__(self):
        super(HelloWorld, self).__init__(None)
        self.setWindowFlags(Qt.Window)
        self.ui = Ui_HelloWorldDlg()
        self.ui.setupUi(self)

        self.ui.sl_kthresh.valueChanged.connect(self.valueChange)
        self.ui.ln_area.textChanged.connect(self.valueChange)
        self.ui.ln_height.textChanged.connect(self.valueChange)
        self.ui.ln_padding.textChanged.connect(self.valueChange)
        self.ui.ln_width.textChanged.connect(self.valueChange)

        self.ui.but_save.clicked.connect(self.ProcessEvent)
        self.ui.but_load.clicked.connect(self.ProcessEvent)
        self.ui.but_live.clicked.connect(self.ProcessEvent)
        


        
        # AUTO

        self.ui.but_runTest.clicked.connect(self.ProcessEvent)
        # self.m_addFunc.ui.but_cancel.clicked.connect(self.ProcessEvent)

        # self.ui.listWidget.itemClicked.connect(self.click_item)
        
        self.ui.tableWidget.setRowCount(3)
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setHorizontalHeaderLabels(['name', 'rect'])

        self.ui.tableWidget.clicked.connect(self.click_item)
        #TEACH
        self.ui.frame.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.frame.customContextMenuRequested.connect(self.selectMenu)

        self.ui.frame.installEventFilter(self)

        self.ui.frame.setMouseTracking(True)

        self.toolRect = QAction('Rect (r)', self)
        self.toolRect.setShortcut('r')
        self.toolRect.triggered.connect(self.toolFunction)

        self.toolTest = QAction('Test (a)', self)
        self.toolTest.setShortcut('a')
        self.toolTest.triggered.connect(self.toolFunction)

        # self.buttonlw = PyQt5.QtWidgets.QPushButton('lw', self)
        menu = PyQt5.QtWidgets.QMenuBar(self)

        self.menuCam = QMenu("Camera",self)
        
        dino = self.menuCam.addMenu('&Dino')
        # basler = self.menuCam.addAction('Basler')
        self.basler = self.menuCam.addMenu('&Basler')
        self.basler.addAction("First Device")
        self.getDevicesBasler()
        for i in range(10):
            idcam = QAction('%d'%i,self)
            # idcam = QAction("0",prevAction)
            dino.addAction(idcam)
        menu.addMenu(self.menuCam)

        self.menulw = PyQt5.QtWidgets.QMenu("Lw",self)
        for i in range(10):
            self.menulw.addAction(QAction("%d"%(i+1),self))
        menu.addMenu(self.menulw)

        self.menufs = PyQt5.QtWidgets.QMenu("Fs",self)
        for i in range(10):
            self.menufs.addAction(QAction("%d"%(i+1),self))
        menu.addMenu(self.menufs)

        self.menucolor = PyQt5.QtWidgets.QMenu("Line Color",self)
        self.menufacecolor = PyQt5.QtWidgets.QMenu("Face Color",self)
        self.colors = [(0,255,0),(255,0,0),(0,0,255),(0,0,0),(255,255,255),(0,255,255)]
        self.colorNames = ["green","blue","red","black","white","yellow"]
        for i in range(len(self.colors)):
            self.menucolor.addAction(QAction(self.colorNames[i],self))
            self.menufacecolor.addAction(QAction(self.colorNames[i],self))
        menu.addMenu(self.menucolor)
        menu.addMenu(self.menufacecolor)

        self.menuCam.triggered.connect(self.triggerMenuCam)
        self.menulw.triggered.connect(self.triggerMenuLw)
        self.menufs.triggered.connect(self.triggerMenuFs)
        self.menucolor.triggered.connect(self.triggerMenuColor)
        self.menufacecolor.triggered.connect(self.triggerMenuFaceColor)
        
        self.toolbar = self.addToolBar('')
        self.toolbar.addAction(self.toolRect)
        self.toolbar.addAction(self.toolTest)

        self.toolbarMenu = self.addToolBar('')
        self.toolbarMenu.addWidget(menu)


        self.onInit()

        
        #Variable
    
        # self.InitVariable()
        
# ===========================funtion==================================================
    def getDevicesBasler(self):
        dev = []
        try:
            devices = pylon.TlFactory.GetInstance().EnumerateDevices()
            cameras = pylon.InstantCameraArray(2)
            for i,cam in enumerate(cameras):
                cam.Attach(pylon.TlFactory.GetInstance().CreateDevice(devices[i]))
                self.basler.addAction(cam.GetDeviceInfo().GetSerialNumber())
        except:
            pass
# =============================================================================
    def rect2cvRect(self,rect):
        W,H = self.ui.frame.width(),self.ui.frame.height()
        H0,W0 = self.image.shape[:2]
        x,y,w,h = rect
        x,y,w,h = int(x*W0/W),int(y*H0/H),int(w*W0/W),int(h*H0/H)

        return [x,y,w,h]
    
    def point2cvPoint(self,point):
        W,H = self.ui.frame.width(),self.ui.frame.height()
        H0,W0 = self.image.shape[:2]
        x,y= point
        x,y = int(x*W0/W),int(y*H0/H)

        return [x,y]
    # def mouseMoveEvent(self, event):
    #     self.ui.lb_xy.setText("%d,%d" % (event.x(), event.y()))
# =============================================================================
    def onInit(self):
        self.camera = None
        self.cameraName = ""
        self.bOpenCam = False
        # self.bOpenCamBasler = False
        self.bLive = False
        self.lw = 2
        self.fs = 2
        self.color = (0,255,0)
        self.facecolor = (0,255,0)
        self.ui.lb_color.setText("Lw : 2,Fs : 2,Line : green,Text : green")
        self.bDrawRect = False
        self.bDrawLine = False
        self.rect = rect()
        self.cvRect = [0,0,0,0]
        self.image = cv2.imread("res/balloon.jpg")
        self.draw = self.image.copy()
        self.showImage(self.ui.frame,self.image)


        # self.ui.groupBox.setEnabled(False)

    def valueChange(self):
        # if self.sender() == self.ui.sl_kthresh:
        value = self.ui.sl_kthresh.value()
        self.ui.lb_kthresh.setText("%d"%value)

        name = self.ui.lb_name.text()

        self.roiTest()
        pass

    def click_item(self,item):
        for item in self.ui.tableWidget.selectedItems():
            row = item.row()
            name = self.ui.tableWidget.item(row,0).text()
            rect = self.ui.tableWidget.item(row,1).text()

            self.ui.groupBox.setEnabled(True)
            try:
                self.ui.lb_name.setText(name)
                self.ui.ln_rect.setText(rect)
            except:
                pass
            # print(row,name,rect)
    def get_current_item(self):
        row = self.ui.listWidget.currentRow()
        return self.listRect[row]
    def triggerMenuCam(self,q):
        txt = q.text()
        lst_idCam = ["%d"%i for i in range(10)]
        if txt in lst_idCam:
            idCam = int(txt)
            m_frame = FrameDlg(self)
            m_frame.setWindowTitle("Dino %d"%idCam)
            m_frame.cameraName = DINO
            m_frame.camera,m_frame.bOpenCam = m_frame.onCamera(cameraName=m_frame.cameraName,idCam=idCam)
            m_frame.show()

            pass
        else :
            m_frame = FrameDlg(self)
            m_frame.setWindowTitle(BASLER +"---"+txt)
            
            m_frame.cameraName = BASLER
            idCam = txt
            m_frame.camera,m_frame.bOpenCam = m_frame.onCamera(cameraName=m_frame.cameraName,idCam=idCam)

            m_frame.show()
            pass
        pass
    def triggerMenuLw(self,q):
        self.lw = int(q.text())
        txt = "Lw : {},Fs : {},Line : {},Text : {}".format(self.lw,self.fs,self.colorNames[self.colors.index(self.color)]
        ,self.colorNames[self.colors.index(self.facecolor)])
        self.ui.lb_color.setText(txt)
        pass
    def triggerMenuFs(self,q):
        self.fs = int(q.text())
        txt = "Lw : {},Fs : {},Line : {},Text : {}".format(self.lw,self.fs,self.colorNames[self.colors.index(self.color)]
        ,self.colorNames[self.colors.index(self.facecolor)])
        self.ui.lb_color.setText(txt)
        pass
    def triggerMenuColor(self,q):
        colorname = q.text()
        i = self.colorNames.index(colorname)
        self.color = self.colors[i]
        txt = "Lw : {},Fs : {},Line : {},Text : {}".format(self.lw,self.fs,self.colorNames[self.colors.index(self.color)]
        ,self.colorNames[self.colors.index(self.facecolor)])
        self.ui.lb_color.setText(txt)
        pass
    def triggerMenuFaceColor(self,q):
        colorname = q.text()
        i = self.colorNames.index(colorname)
        self.facecolor = self.colors[i]
        txt = "Lw : {},Fs : {},Line : {},Text : {}".format(self.lw,self.fs,self.colorNames[self.colors.index(self.color)]
        ,self.colorNames[self.colors.index(self.facecolor)])
        self.ui.lb_color.setText(txt)
        pass
    def toolFunction(self):
        if self.sender() == self.toolRect:
            self.bDrawLine = True
            self.toolbar.setEnabled(False)
        elif self.sender() == self.toolTest:
            self.runTest()
        pass
    def __del__(self):
        self.ui     = None
    
    def openFileNameDialog(self):
        sDir = os.getcwd()    
        fileName, _ = QFileDialog.getOpenFileName(self,"Slect File",sDir,"All Files (*);;Image Files (*.jpg)")
        return fileName
# =============================================================================
    def loadImage(self):
        file_name = self.openFileNameDialog()
        if file_name != "":
            self.image = cv2.imread(file_name)
            self.showImage(self.ui.frame,self.image)
            
    def list2Str(self,lst):
        strl = str(lst)
        strl = strl[1:len(strl)-1]
        return strl
    def str2List(self,string):
        lststring = string.split(",")
        try:
            A = [int(s) for s in lststring]
            if len(A) == 1:
                A = [A[0],A[0]]
        except:
            A = len(lststring)*[0]
        return A
    def str2int(self,string):
        if string == "":
            return 0
        return int(string)
        pass
    def savePara(self):
        QMessageBox.information(self,"Save","Done")

        pass
    def loadPara(self,file_para = FILE_PARAMS):
        pass
    def log(self,text):
        text = str(text)
        strTime = time.strftime("%H:%M:%S  ")
        text = strTime + text
        self.ui.listWidget.addItem(text)

    def paddingRoi(self,rect,pad=3):
        return vs.add(rect,[-pad,-pad,pad,pad])
    def putText(slef,img,text,p,color=(0,255,0),lw=2,fs=2):
        cv2.putText(img,text,p,cv2.FONT_HERSHEY_COMPLEX,fs,color,lw,cv2.LINE_AA)
    def rectangle(self,img,r,color=(0,255,0),lw=2):
        x1,y1,x2,y2 = r
        cv2.rectangle(img,(x1,y1),(x2,y2),color,lw)
    def get_mean(self,img,rects=-1):
        if rects == -1:
            m,std = cv2.meanStdDev(img)
            return int(m[0][0])
        M = []
        for r in rects:
            x,y,x1,y1 = r
            roi = img[y:y1,x:x1]
            m,std = cv2.meanStdDev(roi)
            M.append(int(m[0][0]))
        
        return M
    def roiTest(self):
        pass
        
    def runTest(self):
        pass

    def selectMenu(self,point):
        menu = QMenu(self)

        view = QAction("View", self)
        clear = QAction("Clear All", self)
        cancel = QAction("Cancel ", self)

        save = QAction("Save", self)

        menu.addAction(view)
        menu.addAction(clear)
        menu.addAction(cancel)
        menu.addAction(save)


        # tools = menu.addMenu("&Add...")
        # addRoi = QAction("Roi", self)
        # addRectRight = QAction("Rect Right", self)
        # addRectTop = QAction("Rect Top", self)
        # addRectBot = QAction("Rect Bot", self)

        # # tools.addAction(addRoi)
        # # tools.addAction(addRectRight)
        # # tools.addAction(addRectTop)
        # # tools.addAction(addRectBot)


        parent_point = point+self.ui.frame.pos()+QPoint(10,10)

        action = menu.exec_(self.mapToParent(parent_point))

        if action == view:
            pass

        elif action == cancel:
            pass

        elif action == clear:
            pass
        elif action == save:
            x1,y1,x2,y2 = self.cvRect
            roi = self.image[y1:y2,x1:x2]
            strtime = time.strftime("%H_%M_%S")
            cv2.imwrite("data/%s.jpg"%strtime,roi)
            pass
            
    

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if self.bDrawLine:
                self.bDrawRect = True
                self.bDrawLine = False
                self.rect.tl = [event.x(),event.y()]
            pass
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            if self.bDrawRect:
                self.bDrawRect = False
                self.toolbar.setEnabled(True)
                # pos = QPoint(self.rect.br[0],self.rect.br[1])
                # self.m_addFunc.move(self.mapToGlobal(pos+self.ui.frame.pos()))
                # self.m_addFunc.show()
            pass

        elif event.type() == QtCore.QEvent.MouseMove:
            copy  = self.image.copy()
            self.rect.br = [event.x(),event.y()]

            if self.bDrawLine:
                H0,W0 = self.image.shape[:2]
                x1,y1 = self.point2cvPoint(self.rect.br)
                cv2.line(copy,(0,y1),(W0,y1),self.color,self.lw)
                cv2.line(copy,(x1,0),(x1,H0),self.color,self.lw)
                self.showImage(self.ui.frame,copy)

            elif self.bDrawRect:
                x2,y2 = self.rect.br
                x1,y1 = self.rect.tl
                self.cvRect = self.rect2cvRect([min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2)])
                x1,y1,x2,y2 = self.cvRect
                cv2.rectangle(copy,(x1,y1),(x2,y2),self.color,self.lw)

                txt = "Rect : [X:{},Y:{},W:{},H:{}]".format(x1,y1,x2-x1,y2-y1)
                self.ui.lb_xywh.setText(txt)

                self.showImage(self.ui.frame,copy)

            x1,y1 = self.point2cvPoint(self.rect.br)
            txt = "Point : [X:{},Y:{}]".format(x1,y1)
            self.ui.lb_xy.setText(txt)

        elif event.type() == QtCore.Qt.RightButton:
            pass
        
        return super(HelloWorld, self).eventFilter(obj, event)

    
    def onClickButLive(self):
        if self.ui.but_live.text()=="Live":
            self.bLive = True
            self.ui.but_live.setText("Stop")
            if self.cameraName == DINO:
                m_frame = FrameDlg(self)
                m_frame.show()
                myframe = m_frame.ui.frame
                self.threadLiveDinoCam(myframe)
            elif self.cameraName == BASLER:
                self.threadLiveBaslerCam()
        elif self.ui.but_live.text()=="Stop":
            self.ui.but_live.setText("Live")
            self.bLive = False

    def ProcessEvent(self):
        # M_ADDFUNCTION
        if self.sender() == self.ui.but_save:
            self.savePara()
            pass
        if self.sender() == self.ui.but_runTest:
            self.runTest()
            pass
        if self.sender() == self.ui.but_load:
            self.loadImage()
            pass
        if self.sender() == self.ui.but_live:
            self.onClickButLive()
            pass

# =============================================================================
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
# =============================================================================

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
        self.showImage(self.ui.frame,self.image)
        return
    def closeEvent(self,QCloseEvent):
        pass 

    

