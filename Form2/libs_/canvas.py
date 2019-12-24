from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from libs_.utils import*
from libs_.treeShape import TreeShapeDlg
from libs_.shape import Shape

from functools import partial

import cv2
import numpy as np

ext = ".png"
COLOR = (0,255,0)
SLECTED_COLOR = (0,255,255)
CIRCLE_COLOR = (0,0,255)

BB = QDialogButtonBox

class Dialog(QDialog):
    def __init__(self):
        super(Dialog,self).__init__()
        layout = QVBoxLayout()
        self.buttonBox = bb = BB(BB.Cancel | BB.Ok, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
    def popUp(self, move=True):
        if move:
            self.move(QCursor.pos())
        return self.exec_()

class Canvas(QWidget):
    deleteShapeSignal = pyqtSignal()
    newShapeSignal = pyqtSignal()
    selectedShapeSignal = pyqtSignal(bool)
    def __init__(self,parent):
        super(Canvas,self).__init__(parent)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.tl = (0,0)
        self.br = (0,0)
        self.shapes = []
        self.currentShape = None
        self.selectedShape = None
        self.shapesToItems = {}
        self.itemsToShapes = {}
        self.scale = 1
        self.image = None
        # layout
        self.frame = QLabel("",self)
        self.frame.setAlignment(Qt.AlignCenter)
        self.frame.setStyleSheet("background:black")
        layout = QHBoxLayout()
        layout.addWidget(self.frame)
        self.setLayout(layout)
        # 
        self.edit = False
        self.mouseTracking = False
        self.drawing = False
        self.thickness = 1
        self.fontScale = 1

        self.frame.installEventFilter(self)
        self.frame.setMouseTracking(True)

        action = partial(newAction,self)
        self.menu = QMenu(self)

        self.crop = action("Crop",self.cropped)
        self.menu.addAction(self.crop)

        self.mean = action("Mean",self.compute_mean)
        self.menu.addAction(self.mean)

        self.area = action("Area",self.compute_area)
        self.menu.addAction(self.area)

        self.distance = action("Mean",self.compute_distance)
        self.menu.addAction(self.distance)

        self.menu.addSeparator()
        self.deleteShape = action("Delete",self.deleteShape,icon="delete")
        self.menu.addAction(self.deleteShape)

        self.setEnableMenu(False)

    def cropped(self):
        shape = self.selectedShape
        x,y,w,h = shape.r
        mCrop = self.image[y:y+h,x:x+w]
        filename = "Image/mCrop%s"%ext
        cv2.imwrite(filename,mCrop)
        self.parent().window().statusBar().showMessage("Image saved at %s"%filename)
    def compute_mean(self):
        pass
    def compute_area(self):
        pass
    def compute_distance(self):
        pass
    def deleteShape(self):
        self.deleteShapeSignal.emit()

    def setEnableMenu(self,enable):
        actions = [self.crop,self.area,
                self.mean,self.distance,self.deleteShape]
        for a in actions:
            a.setEnabled(enable)

    def showImage(self,image):
        self.image = image.copy()
        self.scale = showImage(self.image,self.frame)

        w = np.min(self.image.shape[:2])
        if (w > 2000):
            self.thickness = 6
            self.fontScale = 2
        elif (1000<w<=2000):
            self.thickness = 3
            self.fontScale = 1.5
        elif (500<w<=1000):
            self.thickness = 2
            self.fontScale = 0.5
        else:
            self.thickness = 1
            self.fontScale = 0.2

    def eventFilter(self, obj, ev):
        if self.image is None:
            return super(Canvas, self).eventFilter(obj, ev)

        if(ev.type() == QEvent.MouseMove):
            copy = self.image.copy()
            if self.edit:
                self.drawShapes(copy)
                if not self.drawing:
                    self.tl = self.transformPos(ev.pos())
                self.br = self.transformPos(ev.pos())
                if self.insidePos(ev.pos()) and not self.drawing:
                    self.drawCenterLine(copy,self.br)
                    
                if self.drawing:
                    self.drawRect(copy)
                
                if self.mouseTracking and self.insidePos(ev.pos()):
                    bgr = self.image[self.br[1],self.br[0]]
                    text = "Size:%dx%d | Point:%d,%d | Shape:%d,%d,%d,%d | BGR:%d,%d,%d"%(
                        self.image.shape[1],self.image.shape[0],
                        self.br[0],self.br[1],
                        self.tl[0],self.tl[1],self.br[0]-self.tl[0],self.br[1]-self.tl[1],
                        bgr[0],bgr[1],bgr[2]
                    )
                    # self.drawingSignal.emit(text)
                    self.parent().window().lbCoor.setText(text)
            if self.edit:
                self.scale = showImage(copy,self.frame)
            
        if ev.type() == QEvent.MouseButtonPress and self.insidePos(ev.pos()):
            if Qt.LeftButton & ev.buttons():
                if self.edit:
                    if not self.drawing:
                        self.tl = self.transformPos(ev.pos())        
                    self.drawing = not self.drawing
                else:
                    if not self.drawing:
                        self.tl = self.transformPos(ev.pos())
                        self.shapeTracking(self.tl)
                        if self.selectedShape is not None:
                            self.selectedShapeSignal.emit(True)
                        else:
                            self.selectedShapeSignal.emit(False)
                
        if(ev.type() == QEvent.MouseButtonRelease) and self.edit:   
            if Qt.LeftButton == ev.button():
                if not self.drawing:
                    self.edit = False
                    shape = (self.tl[0],self.tl[1],self.br[0]-self.tl[0]
                            ,self.br[1]-self.tl[1])
                    self.currentShape = Shape(shape)
                    dialog = Dialog()
                    if dialog.popUp():
                        self.edit = False
                        self.shapes.append(self.currentShape)
                        self.newShapeSignal.emit()
                    else:
                        self.edit = True
                    self.setEnableMenu(True)
                    
        return super(Canvas, self).eventFilter(obj, ev)
    
    def shapeTracking(self,pos):
        def posInShape(p,shape):
            x,y,w,h = shape.r
            x0,y0 = p
            if x < x0 < x+w and y < y0 < y+h:
                return True
        
        for shape in self.shapes:
            if (posInShape(pos,shape)):
                self.selectedShape = shape
                return
        
        self.selectedShape = None

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

        cvx = int(w*rx)
        cvy = int(h*ry)
        if cvx < 0:
            cvx = 0
        elif cvx > w-1:
            cvx = w-1
        if cvy < 0:
            cvy = 0
        elif cvy > h-1:
            cvy = h-1

        return(cvx,cvy)
    
    def drawRect(self,mat):
        cv2.rectangle(mat,self.tl,self.br,COLOR,self.thickness)
    
    def drawCenterLine(self,mat,pos):
        x,y = pos
        w,h = mat.shape[:2][::-1]
        pt1,pt2 = (x,0),(x,h)
        cv2.line(mat,pt1,pt2,(0,0,0),self.thickness)
        pt1,pt2 = (0,y),(w,y)
        cv2.line(mat,pt1,pt2,(0,0,0),self.thickness)
    
    def drawShapes(self,mat=None,shape=None):
        if mat is None:
            mat = self.image.copy()
        for s in self.shapes:
            pt1 = s.tl
            pt2 = s.br
            cv2.rectangle(mat,pt1,pt2,COLOR,self.thickness)
        if shape is not None:
            pt1 = shape.tl
            pt2 = shape.br
            cv2.rectangle(mat,pt1,pt2,SLECTED_COLOR,self.thickness)
            for point in shape.points:
                cv2.circle(mat,point,self.thickness*5,CIRCLE_COLOR,-1)
                
        
        showImage(mat,self.frame)