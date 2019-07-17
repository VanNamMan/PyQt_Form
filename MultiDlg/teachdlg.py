from PyQt5.QtWidgets import QWidget,QToolBar,QMainWindow,QAction,QFileDialog
from PyQt5.QtGui import QImage,QPixmap,QPainter,QPen,QBrush,QIcon,QColor
from PyQt5.QtCore import Qt,QEvent,QPoint,QRect
from ui_teachdlg import Ui_TeachDlg

import os

RECT = 0
LINE = 1

image_extensions = [".jpg",".png",".bmp",".gif"]
border_radius = 10

class TeachDlg(QMainWindow):
    def __init__(self, parent):
        super(TeachDlg, self).__init__(parent)
        #self.setWindowFlags(Qt.Window)
        self.ui = Ui_TeachDlg()
        self.ui.setupUi(self)
        # toolbar
        self.myTool = QToolBar("Toolbar")
        acts = ["Open Ctrl+O","Save Ctrl+S","DrawRect R"]
        icons = ["res/open.png","res/save.png","res/crop.png"]
        shortcuts = ["Ctrl+o","Ctrl+s","r"]
        triggers = [self.openFile,self.saveFile,self.startDrawing] 
        for i,act in enumerate(acts):
            action = QAction(QIcon(icons[i]),act,self)
            action.triggered.connect(triggers[i])
            action.setShortcut(shortcuts[i])
            self.myTool.addAction(action)
        self.addToolBar(Qt.LeftToolBarArea,self.myTool)
        # variable for paiter
        self.qImage = QImage(640,480,QImage.Format_RGBA8888)
        self.drawing = False
        self.drawRect = False
        self.drawLine = False
        self.typeDraw = 0
        self.startPoint = self.ui.widget.pos()
        self.endPoint = self.startPoint
        self.rectCrop = None
        self.brushColor = Qt.darkGreen
        self.lc = Qt.black
        self.lw = 3
        self.ls = Qt.DashDotLine
        self.brush = QBrush(Qt.blue,Qt.BDiagPattern)
        self.pen = QPen(self.lc,self.lw,self.ls)
        

        self.ui.widget.installEventFilter(self)
        self.ui.widget.setMouseTracking(True)

    def paintEvent(self,event):
        if not self.qImage :
             return super(TeachDlg,self).paintEvent(event)

        p = QPainter()
        p.begin(self)
        p.drawImage(self.ui.widget.geometry(),self.qImage)
        if self.rectCrop is None:
            p.drawImage(self.ui.miniWidget.geometry(),self.qImage)
        else:
            p.drawImage(self.ui.miniWidget.geometry(),self.qImage.copy(self.rectCrop))
        # draw Line
        if self.drawing and self.drawLine:
            p.setPen(QPen(self.lc,self.lw,Qt.SolidLine))
            org = self.ui.widget.geometry()
            pos = self.getGlobalPos(self.endPoint)
            x,y = pos.x(),pos.y()
            p.drawLine(x,org.y()+5,x,org.y()+org.height()-5)
            p.drawLine(org.x()+5,y,org.x()+org.width()-5,y)
            pass
        # draw Rect
        if  self.drawing and not self.drawLine:
            p.setPen(self.pen)
            p.setBrush(self.brush)
            p.drawRect(QRect(self.getGlobalPos(self.startPoint),self.getGlobalPos(self.endPoint)))

        p.end()
        self.update()
     
    def eventFilter(self,obj,event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            if self.drawLine:
                self.drawLine = False
                self.startPoint = event.pos()
                self.endPoint = event.pos()
            pass
        elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            self.drawRect = False
            self.drawLine = False
            pass
        elif event.type() == QEvent.MouseMove:
            if self.drawRect or self.drawLine:
                self.endPoint = event.pos()
                self.rectCrop = self.getRectCrop(self.startPoint,self.endPoint)
            pass
        return super(TeachDlg, self).eventFilter(obj, event)
    def startDrawing(self):
        self.drawing = True
        self.drawRect = True
        self.drawLine = True
        self.startPoint = self.ui.widget.pos()
        self.endPoint = self.startPoint
    def getGlobalPos(self,pos):
        rect = self.ui.widget.geometry()
        pos = self.ui.widget.pos()+pos
        x,y = pos.x(),pos.y()
        x = max(min(x,rect.x()+rect.width()),rect.x())
        y = max(min(y,rect.y()+rect.height()),rect.y())
        return QPoint(x,y)
    def getRectCrop(self,p1,p2):
        if self.qImage:
            ww,hh = self.qImage.width(),self.qImage.height()
            w,h = self.ui.widget.width(),self.ui.widget.height()

            x = int(p1.x()*ww/w)
            y = int(p1.y()*hh/h)
            w0 = int(p2.x()*ww/w) - x
            h0 = int(p2.y()*hh/h) - y

            return QRect(x,y,w0,h0)        
    def openFile(self):
        filepath,_ = QFileDialog.getOpenFileName(self,"Select File","","All Files (*);;Image Files (*.jpg)")
        filename, file_extension = os.path.splitext(filepath)
        if file_extension in image_extensions:
            self.qImage = QImage(filepath)
        pass
    def saveFile(self):
        pass

    def __del__(self):
        self.ui = None