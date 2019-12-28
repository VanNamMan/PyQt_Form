from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

import cv2,os,time,threading,sys
import pandas as pd
import numpy as np
from configparser import ConfigParser
from argparse import ArgumentParser
import re
import serial
from functools import partial
from qimage2ndarray import *

from scipy import misc
from PIL import ImageQt

from vision import *


DEFAULT_FILL_COLOR = QColor(128, 128, 255, 100)
DEFAULT_SELECT_FILL_COLOR = QColor(128, 255, 0, 100)
DEFAULT_VISIBLE_FILL_COLOR = QColor(0, 128, 255, 100)
DEFAULT_VERTEX_FILL_COLOR = QColor(0, 255, 0, 255)
DEFAULT_VERTEX_SELECT_FILL_COLOR = QColor(255,0,0, 255)

CURSOR_DEFAULT = Qt.ArrowCursor
CURSOR_POINT = Qt.PointingHandCursor
CURSOR_DRAW = Qt.CrossCursor
CURSOR_DRAW_POLYGON = Qt.SizeAllCursor
CURSOR_MOVE = Qt.ClosedHandCursor
CURSOR_GRAB = Qt.OpenHandCursor

class Items(QWidget):
    def __init__(self):
        super(Items,self).__init__()
        spin                  = QSpinBox(self)
        spin2                 = QSpinBox(self)
        self.crop             = QLineEdit("0,0,0,0",self)
        self.convert          = newCbb(["bgr2gray","gray2bgr","hsv"])
        self.binary_threshold = spin
        self.binary_type      = newCbb(["normal","inv"])
        self.binary_method    = newCbb(["normal","otsu","adaptive"])
        self.binary_blocksize = QLineEdit("11",self)
        self.blur_size        = QLineEdit("3",self)
        self.blur_method      = newCbb(["blur","median","gauss"])
        self.morph_size       = QLineEdit("3",self)
        self.morph_iter       = QLineEdit("1",self)
        self.morph_method     = newCbb(["dilate","erode","close","open"])
        self.remove_width     = QLineEdit("-1,-1",self)
        self.remove_height    = QLineEdit("-1,-1",self)
        self.remove_area      = QLineEdit("-1,-1",self)
        self.orc_oem          = newCbb(["%d"%i for i in range(4)])
        self.orc_psm          = newCbb(["%d"%i for i in range(14)])
        self.orc_lang         = newCbb(["eng","vie","kor"])
        self.match_score      = spin2
        self.camera_type      = newCbb(["webcam","basler"])
        self.camera_id        = QLineEdit("...",self)

        spin.setRange(0,255)
        spin.setValue(100)
        spin2.setRange(0,100)
        spin2.setValue(90)

class Parameter(QTreeWidget):
    def __init__(self,parent=None):
        super(Parameter,self).__init__(parent)
        _translate = QCoreApplication.translate
        self.headerItem().setText(0, _translate("", "Parameter"))
        self.headerItem().setText(1, _translate("", "Value"))
        lbs = "Camera Crop Convert Binary Blur Morph Remove OCR Matching".split()
        child = [
            "Type SN",
            "Box",
            "Type",
            "Threshold Method Type BlockSize",
            "Method Size",
            "Method Size Iter",
            "Width Height Area",
            "Lang Oem Psm",
            "Score",
        ]
        self.lb_item  = lbs
        self.lb_child = child
        for i,lb,ch in zip(range(len(lbs)),lbs,child):
            item   = QTreeWidgetItem([lb])
            chs    = ch.split()
            self.addTopLevelItem(item)
            for x in chs:
                self.topLevelItem(i).addChild(QTreeWidgetItem([x]))
            
        self.items = Items()
        addWidget = self.addWidget

        addWidget(0,0,self.items.camera_type)
        addWidget(0,1,self.items.camera_id)

        addWidget(1,0,self.items.crop)

        addWidget(2,0,self.items.convert)

        addWidget(3,0,self.items.binary_threshold)
        addWidget(3,1,self.items.binary_method)
        addWidget(3,2,self.items.binary_type)
        addWidget(3,3,self.items.binary_blocksize)

        addWidget(4,0,self.items.blur_method)
        addWidget(4,1,self.items.blur_size)

        addWidget(5,0,self.items.morph_method)
        addWidget(5,1,self.items.morph_size)
        addWidget(5,2,self.items.morph_iter)

        addWidget(6,0,self.items.remove_width)
        addWidget(6,1,self.items.remove_height)
        addWidget(6,2,self.items.remove_area)

        addWidget(7,0,self.items.orc_lang)
        addWidget(7,1,self.items.orc_oem)
        addWidget(7,2,self.items.orc_psm)

        addWidget(8,0,self.items.match_score)

    def addWidget(self,idIt,idChild,widget):
        if idChild is not None:
            it = self.topLevelItem(idIt).child(idChild)
            self.setItemWidget(it, 1, widget)
        else:
            it = self.topLevelItem(idIt)
            self.setItemWidget(it, 1, widget)

class BBox(QDialog):
    def __init__(self):
        super(BBox,self).__init__()
        layout = QVBoxLayout()
        bb = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        bb.rejected.connect(self.reject)
        bb.accepted.connect(self.accept)
        layout.addWidget(bb)
        self.setLayout(layout)
    def popUp(self):
        self.move(QCursor.pos())
        return True if self.exec_() else False

class Shape(QRect):
    def __init__(self,rect):
        super(Shape,self).__init__(rect)
        self.rect                     = rect
        self.cvRect                   = None
        self.functions                = []
        self.config                   = ConfigParser()
        self.fill                     = True
        self.selected                 = False
        self.visible                  = False
        self.points                   = [self.topLeft(),self.topRight(),self.bottomRight(),self.bottomLeft()]
        self.vertex_fill_color        = DEFAULT_VERTEX_FILL_COLOR
        self.vertex_select_fill_color = DEFAULT_VERTEX_SELECT_FILL_COLOR
        self.fill_color               = DEFAULT_FILL_COLOR
        self.select_fill_color        = DEFAULT_SELECT_FILL_COLOR
        self.visible_fill_color       = DEFAULT_VISIBLE_FILL_COLOR
        
    def scaled_(self,scale,w,h):
        sx,sy = scale
        for i in range(4):
            p = self.points[i]
            self.points[i] = QPoint(int(p.x()*sx),int(p.y()*sy))

    def drawVertex(self, path, i):
        d = 10
        point = self.points[i]
        if self.selected:
            path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
        else:
            path.addEllipse(point, d / 2.0, d / 2.0)
        
    def paint(self,painter):
        painter.setPen(QPen(Qt.black))
        painter.setBrush(QBrush())
        line_path = QPainterPath()
        vertex_path = QPainterPath()

        line_path.moveTo(self.points[0])

        for i, p in enumerate(self.points):
            line_path.lineTo(p)
            self.drawVertex(vertex_path,i)

        line_path.lineTo(self.points[0])

        painter.drawPath(line_path)
        painter.drawPath(vertex_path)
        if self.selected:
            painter.fillPath(vertex_path, self.vertex_select_fill_color)
        else:
            painter.fillPath(vertex_path, self.vertex_fill_color)
        if self.fill:
            color = self.visible_fill_color if self.visible else self.fill_color
            color = self.select_fill_color if self.selected else color
            painter.fillPath(line_path, color)

class Canvas(QWidget):
    newShape                = pyqtSignal()
    addShape                = pyqtSignal()
    deleteShape             = pyqtSignal()
    selectedShapeSignal     = pyqtSignal(bool)
    mouseMoveSignal         = pyqtSignal(str)
    
    def __init__(self,*args,**kwargs):
        super(Canvas,self).__init__(*args,**kwargs)
        self.setMouseTracking(True)
        self.pixmap        = None
        self.scaled        = None
        self.mat           = None
        self.paint_        = QPainter()
        self.shapes        = []
        self.width_        = None
        self.height_       = None
        self.width_0        = None
        self.height_0       = None
        self.shapeSelected = None
        self.edit          = False
        self.drawing       = False
        self.verified      = False
        self.tl            = QPoint()
        self.br            = QPoint()
        self.scale         = (1.,1.)
        self.bbox          = BBox()
        self.curPos        = None
        self.contextMenu   = QMenu()
        self.items         = []
        self.current       = None

        action             = partial(newAction,self)
        test               = action("Test",self.test,"a","test",False)
        testAll            = action("Test all",self.testAll,"shift+a","testAll",False)
        delete             = action("Delete",self.delete,"delete","delete",False)

        self.actions       = struct(
            test    = test,
            testAll = testAll,
            delete  = delete
        )
        addActions(self.contextMenu,[test,testAll,delete])
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popUpMenu)
        # 
        layout = QVBoxLayout()

        self.listShape      = QListWidget(self)

        functions = ["crop","convert","blur","binary"
                    ,"morphology","removeBlobs","ocr","matching"]
        self.listFunction = QListWidget(self)
        addItems(self.listFunction,functions)
        for i in range(len(functions)):
            item = self.listFunction.item(i)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(not Qt.Checked)

        self.parameter = Parameter(self)
        
        self.but_save  = newButton("Save",self.save,"save")
        self.but_apply = newButton("Apply",self.apply,"apply")

        addWidgets(layout,[self.listShape,self.listFunction
                ,self.parameter,self.but_apply,self.but_save])

        w = 200
        self.listShape.setMaximumWidth(w)
        self.listShape.setMaximumHeight(100)
        self.listFunction.setMaximumWidth(w)
        self.listFunction.setMaximumHeight(100)
        self.parameter.setMaximumWidth(w)
        self.but_save.setMaximumWidth(w)
        self.but_apply.setMaximumWidth(w)
        self.setLayout(layout)

        # 
        self.selectedShapeSignal.connect(self._selectedShape)
        self.newShape.connect(self._newShape)
        self.listShape.itemClicked.connect(self.itemClicked)
        pass

    def itemClicked(self,item):
        index = self.items.index(item)
        for i,shape in enumerate(self.shapes):
            if i == index:
                shape.selected = True
                self.shapeSelected = shape
            else:
                shape.selected = False
        
    def _newShape(self):
        shape = self.current
        tl           = self._transformCvPos(self.tl)
        br           = self._transformCvPos(self.br)
        cvRect       = (tl.x(),tl.y(),br.x()-tl.x(),br.y()-tl.y())
        str_rect     = "%d,%d,%d,%d"%cvRect
        text         = "shape-%d [%s]"%(len(self.shapes),str_rect)

        item = QListWidgetItem(text)
        self.listShape.addItem(item)
        self.parameter.items.crop.setText(str_rect)
        shape.cvRect = cvRect
        self.shapes.append(shape)
        self.items.append(item)
        pass
    def _selectedShape(self,selected):
        if selected:
            i = self.shapes.index(self.shapeSelected)
            item = self.listShape.item(i)
            item.setSelected(True)
            self.actions.test.setEnabled(True)
            self.actions.testAll.setEnabled(True)
            self.actions.delete.setEnabled(True)
            str_rect = "%d,%d,%d,%d"%self.shapeSelected.cvRect
            self.parameter.items.crop.setText(str_rect)

            for i,shape in enumerate(self.shapes):
                if shape != self.shapeSelected:
                    shape.selected = False
                    self.listShape.item(i).setSelected(False)
        else:
            self.shapeSelected = None
            self.actions.test.setEnabled(False)
            self.actions.testAll.setEnabled(False)
            self.actions.delete.setEnabled(False)

    def apply(self):
        if self.shapeSelected is None:
            return
        self.shapeSelected.functions = []
        n = self.listFunction.count()
        for i in range(n):
            item = self.listFunction.item(i)
            # "Camera Crop Convert Binary Blur Morph Remove OCR Matching"
            if item.checkState() == Qt.Checked:
                self.shapeSelected.functions.append(item.text())

        para = self.parameter
        item = para.items
        self.shapeSelected.config["Camera"]   = {
            "Type"     : item.camera_type.currentText(),
            "SN"       : item.camera_id.text()
        }
        self.shapeSelected.config["Crop"]     = {
            "Box"      : item.crop.text()
        }
        self.shapeSelected.config["Convert"]  = {
            "Type"     : item.convert.currentText()
        }
        self.shapeSelected.config["Binary"]   = {
            "Threshold": item.binary_threshold.text(),
            "Method"   : item.binary_method.currentText(),
            "Type"     : item.binary_type.currentText(),
            "BlockSize": item.binary_blocksize.text(),
        }
        self.shapeSelected.config["Blur"]     = {
            "Method"   : item.blur_method.currentText(),
            "Size"     : item.blur_size.text()
        }
        self.shapeSelected.config["Morph"]    = {
            "Method"   : item.morph_method.currentText(),
            "Size"     : item.morph_size.text(),
            "Iter"     : item.morph_iter.text()
        }
        self.shapeSelected.config["Remove"]   = {
            "Width"    : item.remove_width.text(),
            "Height"   : item.remove_height.text(),
            "Area"     : item.remove_area.text()
        }
        self.shapeSelected.config["OCR"]      = {
            "Lang"     : item.orc_lang.currentText(),
            "Oem"      : item.orc_oem.currentText(),
            "Psm"      : item.orc_psm.currentText()
        }
        self.shapeSelected.config["Matching"] = {
            "Score"    : item.match_score.text()
        }

        # with open("para.config","w") as ff:
        #     self.shapeSelected.config.write(ff)
    def test(self):
        shape = self.shapeSelected
        config = shape.config
        mat = process(self.mat,shape.functions,config)
        if isinstance(mat,np.ndarray):
            cv2.imshow("",mat)
            cv2.waitKey()
        pass
    def testAll(self):
        pass
    def save(self):
        pass
    def add(self):
        pass
    def delete(self):
        if self.shapeSelected is not None:
            index = self.shapes.index(self.shapeSelected)
            self.shapes.remove(self.shapeSelected)
            self.shapeSelected = None
            self.listShape.takeItem(index)
        pass
    def popUpMenu(self):
        self.contextMenu.exec_(QCursor.pos())
        pass
    def QPixmapToCvMat(self,pixmap):
        '''  Converts a QImage into an opencv MAT format  '''
        qimage = pixmap.toImage()
        arr = rgb_view(qimage)
        arr = arr[:,:,::-1]
        return arr
    def scaled_(self):
        if self.pixmap is not None:            
            w  = self.width_
            h  = self.height_
            self.scaled = self.pixmap.scaled(w,h)

            for shape in self.shapes:
                self._transformInv(shape)
        
    def loadPixmap(self,pixmap):
        self.pixmap = pixmap
        self.mat    = self.QPixmapToCvMat(pixmap)
        self.scaled_()
        self.repaint()
    
    def _transform(self,pos):
        return pos - self.origin
    def _transformCvPos(self,pos):
        w,h        = self.mat.shape[:2][::-1]
        aw,ah      = self.width_,self.height_
        px         = pos.x()
        py         = pos.y()
        rx,ry      = px/aw,py/ah
        return QPoint(int(rx*w),int(ry*h))
    
    def _transformInv(self,shape):
        w,h         = self.mat.shape[:2][::-1]
        aw,ah       = self.width_,self.height_
        sx,sy,sw,sh = shape.cvRect
        rx,ry,rw,rh       = sx/w,sy/h,sw/w,sh/h
        x,y,w,h     = int(rx*aw),int(ry*ah),int(rw*aw),int(rh*ah)
        rect = QRect(x,y,w,h) 
        shape.points = [rect.topLeft(),rect.topRight(),rect.bottomRight(),rect.bottomLeft()]
        shape.rect   = rect
    
    def resizeEvent(self,ev):
        self.origin = self.listShape.geometry().topRight()
        w,h         = self.width()-self.origin.x(),self.height()-self.origin.y()
        self.width_ = w
        self.height_ = h
        self.scaled_()
        super(Canvas, self).resizeEvent(ev)

    def paintEvent(self,ev):
        if not self.pixmap:
            return super(Canvas, self).paintEvent(ev)

        w,h = self.width(),self.height()
        p = self.paint_
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        # p.scale(self.scale,self.scale)
        # p.translate(self.offsetToCenter())
        p.setPen(QPen(Qt.black,2,Qt.DashDotLine))
        p.setBrush(QBrush(Qt.green,Qt.BDiagPattern))
        self.origin = self.listShape.geometry().topRight()
        p.translate(self.origin)
        p.drawPixmap(0,0,self.scaled)
        if self.curPos is not None and self.edit and not self.drawing:
            p.setPen(Qt.black)
            pos = self.curPos
            pos1 = QPoint(0,pos.y())
            pos2 = QPoint(self.width(),pos.y())
            pos3 = QPoint(pos.x(),0)
            pos4 = QPoint(pos.x(),self.height())
            p.drawLine(pos1,pos2)
            p.drawLine(pos3,pos4)
        if self.drawing:
            p.drawRect(QRect(self.tl,self.br))
        for shape in self.shapes:
            shape.paint(p)

        
        self.setAutoFillBackground(True)
        if self.verified:
            pal = self.palette()
            pal.setColor(self.backgroundRole(), QColor(184, 239, 38, 128))
            self.setPalette(pal)
        else:
            pal = self.palette()
            pal.setColor(self.backgroundRole(), QColor(232, 232, 232, 255))
            self.setPalette(pal)

        self.update()
        p.end()

    def mouseMoveEvent(self,ev):
        pos = self._transform(ev.pos())
        self.curPos = pos
        text = "%dx%d"%(self.curPos.x(),self.curPos.y())
        self.mouseMoveSignal.emit(text)
        if self.drawing :
            self.setCursor(CURSOR_DRAW)
            self.br = self.curPos
        else:
            for shape in self.shapes:
                if self.inShape(pos,shape):
                    shape.visible = True
                else:
                    shape.visible = False

    def mousePressEvent(self,ev):
        pos = self._transform(ev.pos())
        if ev.button() == Qt.LeftButton:
            if not self.drawing and self.edit:
                self.drawing = True
                self.tl = pos
                self.br = pos
            if not self.drawing and not self.edit:
                idx = -1
                for i,shape in enumerate(self.shapes):
                    if self.inShape(pos,shape):
                        shape.selected = True
                        self.shapeSelected = shape
                        self.selectedShapeSignal.emit(True)
                        idx = i
                        break
                if idx == -1:
                    self.selectedShapeSignal.emit(False)
                
    def mouseReleaseEvent(self,ev):
        pos = self._transform(ev.pos())
        if ev.button() == Qt.LeftButton and self.drawing and self.isDraw():
            if self.bbox.popUp():
                self.cancelEdit()
                self.setCursor(CURSOR_DEFAULT)
                self.current = Shape(QRect(self.tl,self.br))
                self.newShape.emit()
            else:
                self.cancelEdit()
                self.setCursor(CURSOR_DEFAULT)
                pass
        
        elif not self.isDraw():
            self.cancelEdit()
    
    def cancelEdit(self):
        self.drawing = False
        self.edit = False
    def isDraw(self):
        return True if self.tl != self.br else False
    def inShape(self,pos,shape):
        tl = shape.rect.topLeft()
        br = shape.rect.bottomRight()
        if tl.x() < pos.x() < br.x() and tl.y() < pos.y() < br.y():
            return True
        else:
            return False

class HashableQListWidgetItem(QListWidgetItem):

    def __init__(self, *args):
        super(HashableQListWidgetItem, self).__init__(*args)

    def __hash__(self):
        return hash(id(self))

class Port(serial.Serial):
    def __init__(self,port="COM1",baud=9600,prefix="@",suffix="\r\n",_timeout=0.01):
        super(Port,self).__init__(port,baud)
        self.prefix = prefix
        self.suffix = suffix
        self.data = ""
        self._timeout = 0.01
    
    def isMessage(self,data):
        return re.findall(self.prefix,data) and re.findall(self.suffix,data)
    
    def splitData(self,data):
        start = re.search(self.prefix,data).end()
        end = re.search(self.suffix,data).start()
        return data[start:end]

class struct(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def getStrDateTime():
    return time.strftime("%d%m%y_%H%M%S")

def getStrTime():
    return time.strftime("%H:%M:%S")

def distance(v1,v2):
    assert len(v1)==len(v2),print("v1,v2 need same length")
    v = np.array([v2[i] - v1[i] for i in range(len(v1))])
    return np.sqrt(np.sum(np.square(v)))

def str2ListInt(string):
    lst = string.split(",")
    return [int(l) for l in lst]

def addItems(cbb,items):
    [cbb.addItem(it) for it in items]

def newCbb(items,parent):
    cbb = QComboBox(parent)
    addItems(cbb,items)
    return cbb

def newIcon(icon):
    return QIcon(':/' + icon)

def addActions(menu,actions):
    for act in actions:
        if isinstance(act,QAction):
            menu.addAction(act)
        else:
            menu.setMenuBar(act)

def newCbb(items,slot=None):
    cbb = QComboBox()
    [cbb.addItem(item) for item in items]
    if slot is not None:
        cbb.activated.connect(slot)
    return cbb
def newButton(text,slot=None,icon=None):
    b = QPushButton(text)
    if slot is not None:
        b.clicked.connect(slot)
    if icon is not None:
        b.setIcon(newIcon(icon))
    
    return b

def addWidgets(layout,wds):
    for w in wds:
        if isinstance(w,QWidget):
            layout.addWidget(w)
        else:
            layout.addLayout(w)

def addTriggered(action,trigger):
    action.triggered.connect(trigger)

def newAction(parent,text,slot=None,shortcut=None,icon=None,enabled=True):
    a = QAction(text,parent)
    if icon is not None:
        a.setIcon(newIcon(icon))
    if shortcut is not None:
        a.setShortcut(shortcut)
    if slot is not None:
        a.triggered.connect(slot)
    a.setEnabled(enabled)
    return a

def mkdir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def runThread(target,args):
    thread = threading.Thread(target=target,args=args)
    thread.start()

def showImage(image,label):
    width , height = label.width(),label.height()

    h,w = image.shape[:2]

    s = min(width/w,height/h)

    new_w = int(w*s)
    new_h = int(h*s)

    # t0 = time.time()
    new_img = cv2.resize(image,(new_w,new_h))
    # print(time.time()-t0)
    if len(image.shape) == 2:
        new_img = cv2.cvtColor(new_img, cv2.COLOR_GRAY2RGB)
        qpix = QPixmap.fromImage(ImageQt.ImageQt(misc.toimage(new_img)))
    else:
        channel = image.shape[-1]
        new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
        qim = QImage(new_img.data,new_w,new_h,channel*new_w, QImage.Format_RGB888)
        qpix = QPixmap(qim)

    label.setPixmap(qpix)

    return s

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    wd = QMainWindow()
    canvas = Canvas(wd)
    wd.setCentralWidget(canvas)
    wd.show()
    sys.exit(app.exec_())
    