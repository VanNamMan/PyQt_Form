from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from libs_.utils import*

import cv2
import numpy as np

ext = ".png"

class Canvas(QWidget):
    addRoiSignal = pyqtSignal()
    cropSignal = pyqtSignal()
    computeMeanSignal = pyqtSignal()
    computeAreaSignal = pyqtSignal()
    computeDistanceSignal = pyqtSignal()
    def __init__(self,parent):
        super(Canvas,self).__init__(parent)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.tl = (0,0)
        self.br = (0,0)
        self.shape = QRect()
        self.scale = 1
        self.image = None
        self.frame = QLabel("",self)
        self.frame.setAlignment(Qt.AlignCenter)
        self.frame.setStyleSheet("background:black")
        layout = QVBoxLayout()
        layout.addWidget(self.frame)
        self.setLayout(layout)

        self.edit = False
        self.mouseTracking = False
        self.drawing = False
        self.thickness = 1
        self.fontScale = 1
        self.frame.installEventFilter(self)
        self.frame.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.selectMenu)

    def showImage(self,image):
        self.image = image.copy()
        self.scale = showImage(self.image,self.frame)
        self.thickness = max(self.image.shape[0]//500,1)
        self.fontScale = max(self.image.shape[0]/500,0.2)

    def eventFilter(self, obj, ev):
        if self.image is None:
            return super(Canvas, self).eventFilter(obj, ev)

        if(ev.type() == QEvent.MouseMove) and self.edit:
            copy = self.image.copy()
            self.br = self.transformPos(ev.pos())
            if self.insidePos(ev.pos()) and not self.drawing:
                self.drawCenterLine(copy,self.br)
            if self.drawing:
                self.shape = QRect(self.tl[0],self.tl[1]
                ,self.br[0]-self.tl[0],self.br[1]-self.tl[1])
                self.drawRect(copy)
            if self.mouseTracking and self.insidePos(ev.pos()):
                bgr = self.image[self.br[1],self.br[0]]
                text = "[%d,%d] [%d,%d,%d,%d] (%d,%d,%d)"%(
                    self.br[0],self.br[1],
                    self.shape.x(),self.shape.y(),self.shape.width(),self.shape.height(),
                    bgr[0],bgr[1],bgr[2]
                )
                cv2.putText(copy,text,(10,10),cv2.FONT_HERSHEY_COMPLEX
                ,self.fontScale,(0,0,0),self.thickness)
            showImage(copy,self.frame)

        if(ev.type() == QEvent.MouseButtonPress) and self.insidePos(ev.pos()) and self.edit:
            if Qt.LeftButton & ev.buttons():
                self.tl = self.transformPos(ev.pos())
                self.drawing = not self.drawing

        if(ev.type() == QEvent.MouseButtonRelease) and self.edit:   
            if Qt.LeftButton == ev.button():
                if not self.drawing:
                    self.edit = False
            
        return super(Canvas, self).eventFilter(obj, ev)
    
    def insidePos(self,pos):
        w,h = self.image.shape[:2][::-1]
        W,H = self.frame.width(),self.frame.height()
        new_w,new_h = w*self.scale,h*self.scale

        dx,dy = (W-new_w)//2,(H-new_h)//2

        x,y = pos.x(),pos.y()

        if(dx<x<W-dx) and (dy<y<H-dy):
            return True
        else:
            return False

    def setEditing(self,edit):
        self.edit = edit
    
    def setTracking(self,tracking):
        self.mouseTracking = tracking

    def transformPos(self,pos):
        w,h = self.image.shape[:2][::-1]
        W,H = self.frame.width(),self.frame.height()
        new_w,new_h = w*self.scale,h*self.scale

        dx,dy = (W-new_w)//2,(H-new_h)//2

        x = pos.x() - dx
        y = pos.y()- dy

        rx,ry = x/new_w,y/new_h
        return(int(w*rx),int(h*ry))
    
    def drawRect(self,mat):
        cv2.rectangle(mat,self.tl,self.br,(0,255,0),self.thickness)
    
    def drawCenterLine(self,mat,pos):
        x,y = pos
        w,h = mat.shape[:2][::-1]
        pt1,pt2 = (x,0),(x,h)
        cv2.line(mat,pt1,pt2,(0,0,0),self.thickness)
        pt1,pt2 = (0,y),(w,y)
        cv2.line(mat,pt1,pt2,(0,0,0),self.thickness)
    
    def crop(self):
        l,t = self.tl
        r,b = self.br
        return self.image[t:b,l:r]

    def selectMenu(self,point):
        menu = QMenu(self)
        addRoi = menu.addAction("Add Roi")
        crop = menu.addAction("Crop")
        computeMean = menu.addAction("Compute Mean")
        computeArea = menu.addAction("Compute Area")
        computeDistance = menu.addAction("Compute Distance")

        parent_point = point
        action = menu.exec_(self.mapToParent(parent_point))
        
        if action == addRoi:
            self.addRoiSignal.emit()
        if action == crop:
            self.cropSignal.emit()
        if action == computeMean:
            self.computeMeanSignal.emit()
        if action == computeArea:
            self.computeAreaSignal.emit()
        if action == computeDistance:
            self.computeDistanceSignal.emit()