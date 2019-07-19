from PyQt5.QtWidgets import QApplication,QWidget,QToolBar,QMainWindow,QAction,QFileDialog
from PyQt5.QtGui import QImage,QPixmap,QPainter,QPen,QBrush,QIcon,QColor,QFont,QCursor
from PyQt5.QtCore import Qt,QEvent,QPoint,QRect
from ui_teachdlg import Ui_TeachDlg

import os,math

RECT = 0
LINE = 1

image_extensions = [".jpg",".png",".bmp",".gif"]
border_radius = 10
hand_cursor = Qt.OpenHandCursor
size_fdiag = Qt.SizeFDiagCursor
size_bdiag = Qt.SizeBDiagCursor


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

        self.startPosActive = None
        self.endPosActive = None

        self.idRectActive = -1
        self.idRectTracking = -1
        self.cvRectCrop = None
        self.globalRectCrop = None
        self.listCvRectCrop = []
        self.listGlobalRectCrop = []
        self.brushColor = Qt.darkGreen
        self.lc = QColor(0,0,0)
        self.lcAdded = QColor(0,170,0)
        self.lcTracking = QColor(170,0,0)
        self.lcActive = QColor(255,170,0)
        self.lw = 3
        self.ls = Qt.DashDotLine
        self.brush = QBrush(Qt.blue,Qt.BDiagPattern)

        self.ui.widget.installEventFilter(self)
        self.ui.widget.setMouseTracking(True)

    def paintEvent(self,event):
        if not self.qImage :
             return super(TeachDlg,self).paintEvent(event)

        p = QPainter()
        p.begin(self)
        p.drawImage(self.ui.widget.geometry(),self.qImage)
        if self.cvRectCrop is None:
            p.drawImage(self.ui.miniWidget.geometry(),self.qImage)
        else:
            p.drawImage(self.ui.miniWidget.geometry(),self.qImage.copy(self.cvRectCrop))
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
        if self.drawing and not self.drawLine and self.globalRectCrop is not None and self.idRectActive == -1:
            p.setPen(QPen(self.lc,self.lw,self.ls))
            p.setBrush(self.brush)
            p.drawRect(self.globalRectCrop)

        # draw rect tracking , active rect , size
        if self.drawing and not self.drawLine and not self.drawRect:
            for i,globalRect in enumerate(self.listGlobalRectCrop):
                if i != self.idRectTracking:
                    p.setPen(QPen(self.lcAdded,self.lw,Qt.SolidLine))
                else:
                    p.setPen(QPen(self.lcTracking,self.lw,Qt.SolidLine))
                    p.setBrush(QBrush(Qt.blue))
                    p.drawEllipse(globalRect.topLeft(),5,5)
                    p.drawEllipse(globalRect.topRight(),5,5)
                    p.drawEllipse(globalRect.bottomRight(),5,5)
                    p.drawEllipse(globalRect.bottomLeft(),5,5)

                p.setBrush(self.brush)
                p.drawRect(globalRect)

                p.setFont(QFont("Arial",20,QFont.Bold))
                p.drawText(globalRect.x(),globalRect.y()-5,str(i))

        p.end()
        self.update()
     
    def eventFilter(self,obj,event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            # draw line
            pos = event.pos()
            if self.drawLine:
                self.drawLine = False
                self.startPoint = pos
                self.endPoint = pos
            # draw rect , active rect
            if not self.drawRect and not self.drawLine:
                for r in self.listGlobalRectCrop:
                    if r.contains(pos):
                        self.idRectActive = self.listGlobalRectCrop.index(r)
                        self.startPosActive = self.getGlobalPos(pos)
                pass
        elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            # release draw
            pos = event.pos()
            self.drawRect = False
            self.drawLine = False
            self.idRectActive = -1
            pass
        elif event.type() == QEvent.MouseMove:
            pos = event.pos()
            globalPos = self.getGlobalPos(pos)
            # draw rect
            if self.drawRect or self.drawLine:
                self.endPoint = pos
                self.cvRectCrop = self.getCvRectCrop(self.startPoint,self.endPoint)
                self.globalRectCrop = self.getGlobalRectCrop(self.startPoint,self.endPoint)
            else:
                # tarcking Rect
                if self.idRectActive == -1:
                    for r in self.listGlobalRectCrop:
                        if r.contains(globalPos):
                            self.idRectTracking = self.listGlobalRectCrop.index(r)
                            QApplication.setOverrideCursor(hand_cursor)
                            break
                        else:
                            QApplication.restoreOverrideCursor()
                # Move rect actived
                else:
                    self.endPosActive = globalPos
                    v = self.endPosActive-self.startPosActive
                    r = self.listGlobalRectCrop[self.idRectActive]
                    self.listGlobalRectCrop[self.idRectActive] = r.translated(v)
                    self.cvRectCrop = self.globalRect2CvRect(self.listGlobalRectCrop[self.idRectActive])

                    self.startPosActive = self.endPosActive
                # change cursor size_fdiag
                if self.idRectTracking != -1:
                    flag = self.checkRectCorner(globalPos,self.listGlobalRectCrop[self.idRectTracking],5)
                    if flag == 0:
                        QApplication.setOverrideCursor(size_fdiag)
                    elif flag == 1:
                        QApplication.setOverrideCursor(size_bdiag)
                                 
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
    def globalRect2CvRect(self,r):
        p1 = r.topLeft() - self.ui.widget.pos()
        p2 = r.bottomRight() - self.ui.widget.pos()
        # print("p1 , p2 : ",p1,p2)
        return self.getCvRectCrop(p1,p2)
    def getGlobalRectCrop(self,p1,p2):
        return (QRect(self.getGlobalPos(self.startPoint),self.getGlobalPos(self.endPoint)))
    def getCvRectCrop(self,p1,p2):
        if self.qImage:
            ww,hh = self.qImage.width(),self.qImage.height()
            w,h = self.ui.widget.width(),self.ui.widget.height()

            x = int(p1.x()*ww/w)
            y = int(p1.y()*hh/h)
            w0 = int(p2.x()*ww/w) - x
            h0 = int(p2.y()*hh/h) - y

            return QRect(x,y,w0,h0)

    def checkRectCorner(self,p,r,d=2):
        tl,tr,bl,br = r.topLeft(),r.topRight(),r.bottomLeft(),r.bottomRight()
        p_tl = self.distance(p,tl)
        p_tr = self.distance(p,tr)
        p_bl = self.distance(p,bl)
        p_br = self.distance(p,br)

        if min(p_tl,p_br) < d:
            return 0
        elif min(p_tr,p_bl) < d:
            return 1
        else:
            return -1

    def distance(self,p1,p2):
        p = p1-p2
        return math.sqrt(math.pow(p.x(),2)+math.pow(p.y(),2))    
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