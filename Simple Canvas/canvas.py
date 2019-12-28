from utils import*

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

class Items(object):
    def __init__(self,parent):
        super(Items,self).__init__()
        lastConfig = ConfigParser()
        lastConfig.read("demo/para.config")

        self.parent           = parent
        spin                  = QSpinBox(parent)
        spin2                 = QSpinBox(parent)
        self.crop             = QLineEdit("0,0,0,0",parent)
        self.convert          = newCbb(["bgr2gray","gray2bgr","hsv"])
        self.binary_threshold = spin
        self.binary_type      = newCbb(["normal","inv"])
        self.binary_method    = newCbb(["normal","otsu","adaptive"])
        self.binary_blocksize = QLineEdit("11",parent)
        self.blur_size        = QLineEdit("3",parent)
        self.blur_method      = newCbb(["blur","median","gauss"])
        self.morph_size       = QLineEdit("3",parent)
        self.morph_iter       = QLineEdit("1",parent)
        self.morph_method     = newCbb(["dilate","erode","close","open"
                                        ,"gradient","top hat","black hat"])
        self.cnts_mode      = newCbb(["external","list"])
        self.cnts_method        = newCbb(["none","simple"])

        self.remove_width     = QLineEdit("-1,-1",parent)
        self.remove_height    = QLineEdit("-1,-1",parent)
        self.remove_area      = QLineEdit("-1,-1",parent)
        self.orc_oem          = newCbb(["%d"%i for i in range(4)])
        self.orc_psm          = newCbb(["%d"%i for i in range(14)])
        self.orc_lang         = newCbb(["eng","vie","kor"])
        self.match_score      = spin2
        self.match_filename   = QLineEdit("",parent)
        # self.match_filename   = QCommandLinkButton("...",parent)
        # self.match_filename.clicked.connect(self.brower)
        self.camera_type      = newCbb(["webcam","basler"])
        self.camera_id        = QLineEdit("...",parent)

        spin.setRange(0,255)
        spin.setValue(100)
        spin2.setRange(0,100)
        spin2.setValue(90)

        self.setConfig(lastConfig)
    
    def setConfig(self,cfg):
        camera = cfg["Camera"]
        self.camera_type.setCurrentText(camera["type"])
        self.camera_id.setText(camera["sn"])
        crop = cfg["Crop"]
        self.crop.setText(crop["box"])
        cvt = cfg["Convert"]
        self.convert.setCurrentText(cvt["type"])
        binary = cfg["Binary"]
        self.binary_threshold.setValue(int(binary["threshold"]))
        self.binary_method.setCurrentText(binary["method"])
        self.binary_type.setCurrentText(binary["type"])
        self.binary_blocksize.setText(binary["blocksize"])
        blur = cfg["Blur"]
        self.blur_size.setText(blur["size"])
        self.blur_method.setCurrentText(blur["method"])
        morph = cfg["Morph"]
        self.morph_size.setText(morph["size"])
        self.morph_iter.setText(morph["iter"])
        self.morph_method.setCurrentText(morph["method"])
        cnt = cfg["Contours"]
        self.cnts_mode.setCurrentText(cnt["mode"])
        self.cnts_method.setCurrentText(cnt["method"])
        remove = cfg["Remove"]
        self.remove_width.setText(remove["width"])
        self.remove_height.setText(remove["height"])
        self.remove_area.setText(remove["area"])
        ocr = cfg["OCR"]
        self.orc_lang.setCurrentText(ocr["lang"])
        self.orc_oem.setCurrentText(ocr["oem"])
        self.orc_psm.setCurrentText(ocr["psm"])
        match = cfg["Matching"]
        self.match_score.setValue(int(match["score"]))
        self.match_filename.setText(match["file"])

        pass
    def brower(self):
        filename,_ = QFileDialog.getOpenFileName(self.parent,"Select File",os.getcwd()
                ,"Image File (*jpg *png)")
        if filename:
            self.match_filename.setText(filename)

class Parameter(QTreeWidget):
    def __init__(self,parent=None):
        super(Parameter,self).__init__(parent)
        _translate = QCoreApplication.translate
        self.headerItem().setText(0, _translate("", "Parameter"))
        self.headerItem().setText(1, _translate("", "Value"))
        lbs = "Camera Crop Convert Binary Blur Morph Contours Remove OCR Matching".split()
        child = [
            "Type SN",
            "Box",
            "Type",
            "Threshold Method Type BlockSize",
            "Method Size",
            "Method Size Iter",
            "Mode Method",
            "Width Height Area",
            "Lang Oem Psm",
            "Score File",
        ]
        self.lb_item  = lbs
        self.lb_child = child
        for i,lb,ch in zip(range(len(lbs)),lbs,child):
            item   = QTreeWidgetItem([lb])
            chs    = ch.split()
            self.addTopLevelItem(item)
            for x in chs:
                self.topLevelItem(i).addChild(QTreeWidgetItem([x]))
            
        self.items = Items(self)
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

        addWidget(6,0,self.items.cnts_mode)
        addWidget(6,1,self.items.cnts_method)

        addWidget(7,0,self.items.remove_width)
        addWidget(7,1,self.items.remove_height)
        addWidget(7,2,self.items.remove_area)

        addWidget(8,0,self.items.orc_lang)
        addWidget(8,1,self.items.orc_oem)
        addWidget(8,2,self.items.orc_psm)

        addWidget(9,0,self.items.match_score)
        addWidget(9,1,self.items.match_filename)

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
    deleteShape             = pyqtSignal()
    selectedShapeSignal     = pyqtSignal(bool)
    mouseMoveSignal         = pyqtSignal(str)

    addActionSignal         = pyqtSignal(Shape)
    testActionSignal        = pyqtSignal(Shape)
    testAllActionSignal     = pyqtSignal()
    cropActionSignal        = pyqtSignal(Shape)
    
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
        self.funcMenu      = QMenu()
        self.items         = []
        self.current       = None

        action             = partial(newAction,self)
        crop               = action("Crop",self.cropImage,"a","crop",False)
        test               = action("Test",self.test,"a","test",False)
        testAll            = action("Test all",self.testAll,"shift+a","testAll",False)
        delete             = action("Delete",self.delete,"delete","delete",False)

        deleteFunc         = action("Delete",self.deleteFunc,"","deleteFunc",True)

        self.actions       = struct(
            crop        = crop,
            test        = test,
            testAll     = testAll,
            delete      = delete,
            deleteFunc  = deleteFunc
        )
        addActions(self.contextMenu,[crop,test,testAll,delete])
        addActions(self.funcMenu,[deleteFunc])

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popUpMenu)
        # 
        layout = QVBoxLayout()

        self.listShape      = QListWidget(self)

        functions = ["crop","convert","blur","binary"
                    ,"morphology","findContours","removeBlobs","ocr","matching"]
        self.listFunction = QListWidget(self)
        addItems(self.listFunction,functions)
        for i in range(len(functions)):
            item = self.listFunction.item(i)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(not Qt.Checked)

        self.listFunction.itemClicked.connect(self.itemFuncClicked)

        self.listSelectedFunction = QListWidget(self)
        self.listSelectedFunction.itemDoubleClicked.connect(self.itemDoubleClicked)

        self.parameter = Parameter(self)
        
        self.but_save  = newButton("Save",self.save,"save")
        # self.but_apply = newButton("Apply",self.apply,"apply")
        widgets = [
            self.listShape,
            self.listFunction,
            self.listSelectedFunction,
            self.parameter,
            self.but_save
        ]
        addWidgets(layout,widgets)

        w = 300
        for wd in widgets:
            wd.setMaximumWidth(w)
        self.parameter.setMinimumHeight(300)
        self.setLayout(layout)

        # 
        self.selectedShapeSignal.connect(self._selectedShape)
        self.newShape.connect(self._newShape)
        self.listShape.itemClicked.connect(self.itemClicked)
        pass
    
    def enabled_context(self,enable):
        if enable:
            self.actions.crop.setEnabled(True)
            self.actions.test.setEnabled(True)
            self.actions.testAll.setEnabled(True)
            self.actions.delete.setEnabled(True)
        else:
            self.actions.crop.setEnabled(False)
            self.actions.test.setEnabled(False)
            self.actions.testAll.setEnabled(False)
            self.actions.delete.setEnabled(False)

    def itemDoubleClicked(self,item):
        self.funcMenu.exec_(QCursor.pos())
        pass
    def itemFuncClicked(self,item):
        if item.checkState() == Qt.Checked:
            self.listSelectedFunction.addItem(item.text())
        pass
    def itemClicked(self,item):
        index = self.items.index(item)
        for i,shape in enumerate(self.shapes):
            if i == index:
                shape.selected = True
                self.shapeSelected = shape
                self.apply()
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
            self.enabled_context(True)

            for i,shape in enumerate(self.shapes):
                if shape != self.shapeSelected:
                    shape.selected = False
                    self.listShape.item(i).setSelected(False)
            self.apply()
        else:
            self.shapeSelected = None
            self.enabled_context(False)

    def apply(self):
        if self.shapeSelected is None:
            return
        self.shapeSelected.functions = []
        n = self.listSelectedFunction.count()
        for i in range(n):
            item = self.listSelectedFunction.item(i)
            self.shapeSelected.functions.append(item.text())
        
        str_rect = "%d,%d,%d,%d"%self.shapeSelected.cvRect
        self.parameter.items.crop.setText(str_rect)

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
        self.shapeSelected.config["Contours"]    = {
            "Mode"   : item.cnts_mode.currentText(),
            "Method"     : item.cnts_method.currentText()
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
            "Score"    : item.match_score.text(),
            "File"     : item.match_filename.text()
        }

        with open("demo/para.config","w") as ff:
            self.shapeSelected.config.write(ff)
    
    def cropImage(self):
        self.cropActionSignal.emit(self.shapeSelected)
        pass
    def test(self):
        self.testActionSignal.emit(self.shapeSelected)
        pass
    def testAll(self):
        pass
    def save(self):
        pass
    def add(self):
        pass
    def deleteFunc(self):
        items = self.listSelectedFunction.selectedItems()
        if items :
            row = self.listSelectedFunction.row(items[0])
            self.listSelectedFunction.takeItem(row)
        pass
    def delete(self):
        if self.shapeSelected is not None:
            index = self.shapes.index(self.shapeSelected)
            self.shapes.remove(self.shapeSelected)
            self.shapeSelected = None
            self.listShape.takeItem(index)
            self.items.remove(self.items[index])
        pass
    def popUpMenu(self,pos):
        if pos.x() > self.origin.x():
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
        return super(Canvas, self).resizeEvent(ev)

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

