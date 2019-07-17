from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage,QPixmap,QPainter,QPen,QBrush
from PyQt5.QtCore import Qt,QEvent,QPoint,QRect
from ui_teachdlg import Ui_TeachDlg

RECT = 0
LINE = 1

border_radius = 10

class TeachDlg(QWidget):
    def __init__(self, parent):
        super(TeachDlg, self).__init__(parent)
        #self.setWindowFlags(Qt.Window)
        self.ui = Ui_TeachDlg()
        self.ui.setupUi(self)

        self.qImage = QImage(640,480,QImage.Format_RGBA8888)
        self.drawing = False
        self.typeDraw = 0
        self.startPoint = QPoint(0,0)
        self.endPoint = QPoint(100,100)
        self.lc = Qt.red
        self.lw = 3
        self.ls = Qt.DashDotLine
        self.brush = QBrush(Qt.BDiagPattern)
        

        self.ui.widget.installEventFilter(self)

    def paintEvent(self,event):
        if not self.qImage :
             return super(TeachDlg,self).paintEvent(event)

        p = QPainter()
        p.begin(self)
        p.drawImage(self.ui.widget.geometry(),self.qImage)
        # draw Rect
        if self.drawing:
            p.setPen(QPen(self.lc,self.lw,self.ls))
            p.setBrush(self.brush)
            p.drawRect(QRect(self.startPoint,self.endPoint))

        p.end()
        self.update()
     
    def eventFilter(self,obj,event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self.drawing = True
            self.startPoint = self.getGlobalPos(event.pos())
            self.endPoint = self.getGlobalPos(event.pos())
            pass
        elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            self.drawing = False
            pass
        elif event.type() == QEvent.MouseMove:
            self.endPoint = self.getGlobalPos(event.pos())
            pass
        return super(TeachDlg, self).eventFilter(obj, event)
    def getGlobalPos(self,pos):
        return self.ui.widget.pos()+pos
    def __del__(self):
        self.ui = None