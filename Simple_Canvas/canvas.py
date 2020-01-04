from bbox import*
import resources

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

class Shape(object):
    def __init__(self,rect,lb,parent=None):
        super(Shape,self).__init__()
        self.parent                   = parent
        self.rect                     = rect
        self.cvRect                   = parent._transformCvRect(self.rect.topLeft()
                                                            ,self.rect.bottomRight())
        self.result                   = {
            "pixmap" : None,
            "text"   : None
        } 
        self.label                    = lb
        self.functions                = []
        self.config                   = {}
        self.fill                     = True
        self.selected                 = False
        self.visible                  = False
        self.corner                   = None
        self.points                   = [self.rect.topLeft(),self.rect.topRight()
                                        ,self.rect.bottomRight(),self.rect.bottomLeft()]
        self.vertex_fill_color        = DEFAULT_VERTEX_FILL_COLOR
        self.vertex_select_fill_color = DEFAULT_VERTEX_SELECT_FILL_COLOR
        self.fill_color               = DEFAULT_FILL_COLOR
        self.select_fill_color        = DEFAULT_SELECT_FILL_COLOR
        self.visible_fill_color       = DEFAULT_VISIBLE_FILL_COLOR

    def scaled_(self):
        w,h             = self.parent.mat.shape[:2][::-1]
        aw,ah           = self.parent.width_,self.parent.height_
        sx,sy,sw,sh     = str2ListInt(self.config["crop"]["Box"])
        rx,ry,rw,rh     = sx/w,sy/h,sw/w,sh/h
        x,y,w,h         = int(rx*aw),int(ry*ah),int(rw*aw),int(rh*ah)
        rect            = QRect(x,y,w,h)
        self.points     = [rect.topLeft(),rect.topRight(),rect.bottomRight(),rect.bottomLeft()]
        self.rect       = rect
        if self.result["pixmap"] is not None:
            self.result["pixmap"] = self.result["pixmap"].scaled(w,h)
        return

    def drawVertex(self, path, i):
        d = 10
        point = self.points[i]
        if self.selected:
            if i == self.corner:
                d = 20
                path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
            else:
                path.addEllipse(point, d / 2.0, d / 2.0)
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
        #  draw rect
        painter.drawPath(line_path)
        #  draw corner
        painter.drawPath(vertex_path)
        #  draw label
        font = QFont()
        font.setPointSize(self.parent.fs)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(self.parent.color)
        if(self.label == None):
            self.label = ""
        painter.drawText(self[0].x()-1,self[0].y()-1, self.label)

        # draw shape result
        if self.result["pixmap"] is not None:
            painter.drawPixmap(self[0].x(),self[0].y(),self.result["pixmap"])
        if self.result["text"] is not None:
            x,y,w,h = self[0].x(),self[0].y(),self.rect.width(),self.rect.width()
            painter.drawText(x,y,w,h,0,self.result["text"])
        #  fill shape
        bTest = self.result["pixmap"] is not None or self.result["text"] is not None
        if self.selected:
            painter.fillPath(vertex_path, self.vertex_select_fill_color)
        else:
            painter.fillPath(vertex_path, self.vertex_fill_color)
        if self.fill and not bTest:
            color = self.visible_fill_color if self.visible else self.fill_color
            color = self.select_fill_color if self.selected else color
            painter.fillPath(line_path, color)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value

class Canvas(QWidget):
    drawShape               = pyqtSignal(Shape)
    newShape                = pyqtSignal(Shape)
    deleteShape             = pyqtSignal(Shape)
    selectedShapeSignal     = pyqtSignal(bool)
    mouseMoveSignal         = pyqtSignal(str,str)

    addActionSignal         = pyqtSignal(Shape)
    testActionSignal        = pyqtSignal(Shape)
    testAllActionSignal     = pyqtSignal()
    cropActionSignal        = pyqtSignal(Shape)
    
    def __init__(self,parent=None):
        super(Canvas,self).__init__(parent)
        self.setMouseTracking(True)
        self.origin        = QPoint(0,0)
        self.pixmap        = QPixmap(640,480)
        self.scaled        = None
        self.fs            = 10
        self.color         = QColor(0,170,0)
        self.mat           = self.QPixmapToCvMat(self.pixmap)
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
        self.editShape     = False
        self.shapeEdit     = None
        self.moveShape     = None
        self.posMove       = None
        self.nearest       = False
        self.tl            = QPoint()
        self.br            = QPoint()
        self.scale         = (1.,1.)
        self.bbox          = BBox()
        self.curPos        = None
        self.contextMenu   = QMenu()
        self.items         = []
        self.current       = None
        self.boxTeaching   = parent.boxTeaching
        
        action             = partial(newAction,self)
        crop               = action("Crop",self.cropImage,"a","crop",False)
        test               = action("Test",self.test,"a","test",False)
        testAll            = action("Test all",self.testAll,"shift+a","testAll",False)
        delete             = action("Delete",self.delete,"delete","delete",False)

        self.actions       = struct(
            crop        = crop,
            test        = test,
            testAll     = testAll,
            delete      = delete
        )
        addActions(self.contextMenu,[crop,test,testAll,delete])

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popUpMenu)
        # 
        # # 
        self.selectedShapeSignal.connect(self._selectedShape)
        self.newShape.connect(self._newShape)
        self.drawShape.connect(self._drawShape)
        self.deleteShape.connect(self._delShape)
        pass
    
    def enabled_context(self,enable):
        self.actions.crop.setEnabled(enable)
        self.actions.test.setEnabled(enable)
        self.actions.testAll.setEnabled(enable)
        self.actions.delete.setEnabled(enable)

    def reCreateShape(self,idx,tl,br,corner=None):
        self.shapes[idx]            = Shape(QRect(tl,br),"shape-%d"%idx,self)
        self.shapes[idx].corner     = corner
        self.shapes[idx].config     = self.boxTeaching.getConfig()
        self.shapeSelected          = self.shapes[idx]
        self.selectedShapeSignal.emit(True)

        #  auto test
        if self.boxTeaching.autotest.isChecked():
            self.testActionSignal.emit(self.shapes[idx])
        return self.shapes[idx]
    def _delShape(self,shape):
        self.shapes.remove(self.shapeSelected)
        self.shapeSelected = None
        pass
    def _drawShape(self,shape):
        str_cvRect                  = "%d,%d,%d,%d"%shape.cvRect
        str_qRect                   = "%d,%d,%d,%d"%(shape.rect.x()
                                            ,shape.rect.y()
                                            ,shape.rect.width()
                                            ,shape.rect.height())
        self.boxTeaching.boxParameter.items.crop.setText(str_cvRect)
        self.boxTeaching.boxParameter.items.qrect.setText(str_qRect)
        pass
    def _newShape(self,shape):
        shape.config    = self.boxTeaching.getConfig()

        label           = "shape-%d"%(len(self.shapes))
        item = QListWidgetItem(label)
        self.boxTeaching.listShape.addItem(item)
        shape.selected  = True
        self.shapeSelected = shape
        self.shapes.append(shape)
        self.items.append(item)
        self.selectedShapeSignal.emit(True)
        # self.apply()
        pass
    def _selectedShape(self,selected):
        if selected:
            index           = self.shapes.index(self.shapeSelected)
            item            = self.boxTeaching.listShape.item(index)
            config          = self.shapeSelected.config
            item.setSelected(True)
            self.shapeSelected.selected = True
            self.boxTeaching.setConfig(config)
            str_cvRect                  = "%d,%d,%d,%d"%self.shapeSelected.cvRect
            self.window().lbRect.setText("[%s]"%str_cvRect)

            #  auto test
            if self.boxTeaching.autotest.isChecked():
                self.testActionSignal.emit(self.shapes[index])

            for j,shape in enumerate(self.shapes):
                if shape != self.shapeSelected:
                    shape.selected = False
                    self.boxTeaching.listShape.item(j).setSelected(False)

            
            self.enabled_context(True)
            
        else:
            for i,shape in enumerate(self.shapes):
                shape.selected = False
                self.boxTeaching.listShape.item(i).setSelected(False)
            self.shapeSelected = None
            self.enabled_context(False)
    
    def apply(self):
        if self.shapeSelected is None:
            return
        self.shapeSelected.functions = []
        list_                        = self.boxTeaching.boxSelectedFunction.list
        para                         = self.boxTeaching.boxParameter
        n = list_.count()
        for i in range(n):
            item = list_.item(i)
            self.shapeSelected.functions.append(item.text())
        
        cvRect  = "%d,%d,%d,%d"%self.shapeSelected.cvRect
        tl      = self.shapeSelected.rect.topLeft()
        br      = self.shapeSelected.rect.bottomRight()
        qRect   = "%d,%d,%d,%d"%(tl.x(),tl.y(),br.x()-tl.x(),br.y()-tl.y())
        para.items.crop.setText(cvRect)
        item = para.items
        self.shapeSelected.config["camera"]   = {
            "Type"     : item.camera_type.currentText(),
            "SN"       : item.camera_id.text()
        }
        self.shapeSelected.config["crop"]     = {
            "Box"      : cvRect,
            "QRect"    : qRect
        }
        self.shapeSelected.config["convert"]  = {
            "Type"     : item.convert.currentText()
        }
        self.shapeSelected.config["binary"]   = {
            "Threshold": item.binary_threshold.text(),
            "Method"   : item.binary_method.currentText(),
            "Type"     : item.binary_type.currentText(),
            "BlockSize": item.binary_blocksize.text(),
        }
        self.shapeSelected.config["blur"]     = {
            "Method"   : item.blur_method.currentText(),
            "Size"     : item.blur_size.text()
        }
        self.shapeSelected.config["morph"]    = {
            "Method"   : item.morph_method.currentText(),
            "Size"     : item.morph_size.text(),
            "Iter"     : item.morph_iter.text()
        }
        self.shapeSelected.config["contours"]    = {
            "Mode"   : item.cnts_mode.currentText(),
            "Method"     : item.cnts_method.currentText()
        }
        self.shapeSelected.config["remove"]   = {
            "Width"    : item.remove_width.text(),
            "Height"   : item.remove_height.text(),
            "Area"     : item.remove_area.text()
        }
        self.shapeSelected.config["ocr"]      = {
            "Lang"     : item.orc_lang.currentText(),
            "Oem"      : item.orc_oem.currentText(),
            "Psm"      : item.orc_psm.currentText()
        }
        self.shapeSelected.config["matching"] = {
            "Score"    : item.match_score.text(),
            "File"     : item.match_filename.text(),
            "Multiple" : str(item.match_multi.isChecked())
        }

        with open("demo/para.config","w") as ff:
            config              = ConfigParser()
            key                 = self.shapeSelected.label
            config[key]         = self.shapeSelected.config
            config.write(ff)
    
    def cropImage(self):
        self.cropActionSignal.emit(self.shapeSelected)
        pass
    def test(self):
        self.testActionSignal.emit(self.shapeSelected)
        pass
    def testAll(self):
        pass
    def delete(self):
        if self.shapeSelected is not None:
            index = self.shapes.index(self.shapeSelected)
            self.shapes.remove(self.shapeSelected)
            self.shapeSelected = None
            self.boxTeaching.listShape.takeItem(index)
            self.items.remove(self.items[index])
        pass
    # def popUpMenuFunc(self):
    #     if self.listSelectedFunction.count() > 0:
    #         self.funcMenu.exec_(QCursor.pos())
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
            self.fs     = max(self.width_//100,6)
            self.mat    = self.QPixmapToCvMat(self.pixmap)

            for shape in self.shapes:
                # self._transformInv(shape)
                shape.scaled_()
        
    def loadPixmap(self,pixmap):
        self.pixmap = pixmap
        self.scaled_()
        self.repaint()
    
    def coverPos(self,pos):
        x = max(pos.x(),0)
        y = max(pos.y(),0)
        pos = QPoint(x,y)
        return pos
    def _transform(self,pos):
        pos -= self.origin
        return self.coverPos(pos)
    def _transformCvRect(self,tl,br):
        tl         = self._transformCvPos(tl)
        br         = self._transformCvPos(br)
        return     (tl.x(),tl.y(),br.x()-tl.x(),br.y()-tl.y())
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
        return shape
    
    def resizeEvent(self,ev):
        # self.origin = self.listShape.geometry().topRight()
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
        p.setPen(QPen(self.color,2,Qt.DashDotLine))
        p.setBrush(QBrush(Qt.green,Qt.BDiagPattern))
        p.translate(self.origin)
        p.drawPixmap(0,0,self.scaled)
        if self.curPos is not None and self.edit and not self.drawing:
            p.setPen(QPen(Qt.black,2))
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
        if self.pixmap is None:
            return super(Canvas,self).mouseMoveEvent(ev)
        pos         = self._transform(ev.pos())
        self.curPos = pos
        cvPos       = self._transformCvPos(pos)
        ptext       = "%dx%d"%(cvPos.x(),cvPos.y())
        if self.drawing :
            self.setCursor(CURSOR_POINT)
            self.br      = self.curPos
            rtext        = "%d,%d,%d,%d"%self._transformCvRect(self.tl,self.br)
            self.mouseMoveSignal.emit(rtext,ptext)
            lb           = "shape-%d"%(len(self.shapes))
            self.current = Shape(QRect(self.tl,self.br),lb,self)
            self.drawShape.emit(self.current)
        else:
            self.mouseMoveSignal.emit("",ptext)
            idx = self.findShapeNearest(pos)
            if idx is None:
                for shape in self.shapes:
                    shape.visible = False
                    self.setCursor(CURSOR_DEFAULT)
            else:
                for i,shape in enumerate(self.shapes):
                    if i == idx:
                        shape.visible = True
                        if not self.nearest:
                            self.setToolTip(" drag & move Shape")
                            self.setCursor(CURSOR_MOVE)
                    else:
                        shape.visible = False

            if self.shapeSelected is not None and not self.editShape:
                index             = self.shapes.index(self.shapeSelected)
                near,p            = self.isNearestCorner(pos,self.shapes[index])
                self.nearest      = near
                if near :
                    self.shapes[index].corner  = self.shapeSelected.points.index(p)
                    self.setToolTip(" drag & change Shape")
                    self.setCursor(CURSOR_DRAW)
                else:
                    self.shapes[index].corner  = None

            elif self.editShape and self.shapeEdit is not None:
                idx                         = self.shapeEdit
                corner                      = self.shapes[idx].corner
                topleft                     = self.shapes[idx].points[0]
                bottomright                 = self.shapes[idx].points[2]
                tl                          = topleft
                br                          = bottomright
                if corner == 0:
                    tl                      = pos 
                elif corner == 1:
                    tl                      = QPoint(topleft.x(),pos.y())
                    br                      = QPoint(pos.x(),bottomright.y())
                elif corner == 2:
                    br                      = pos
                else:
                    tl                      = QPoint(pos.x(),topleft.y())
                    br                      = QPoint(bottomright.x(),pos.y()) 
                self.current = self.reCreateShape(idx,tl,br,corner)
                self.drawShape.emit(self.current)
                pass
            
            if self.moveShape and not self.editShape and self.shapeEdit is not None:
                idx                         = self.shapeEdit
                topleft                     = self.shapes[idx].points[0]
                bottomright                 = self.shapes[idx].points[2]
                v                           = pos - self.posMove
                self.posMove                = pos
                tl                          = topleft + v
                br                          = bottomright + v
                dx                          = self.width_ - br.x()
                dy                          = self.height_- br.y()
                if(tl.x()*tl.y()*dx*dy) > 0:
                    self.current = self.reCreateShape(idx,tl,br)
                    self.drawShape.emit(self.current)

    def mousePressEvent(self,ev):
        pos = self._transform(ev.pos())
        # if ev.button() == Qt.RightButton:
        #     if self.shapeSelected is not None:
        #         self.apply()
        #     pass
        if ev.button() == Qt.LeftButton:
            if not self.drawing and self.edit:
                self.drawing = True
                self.tl = pos
                self.br = pos
            if not self.drawing and not self.edit and not self.nearest:
                idx = self.findShapeNearest(pos)
                if idx is None:
                    self.selectedShapeSignal.emit(False)
                else:
                    shape                   = self.shapes[idx]
                    shape.selected          = True
                    self.shapeSelected      = shape
                    if not self.moveShape:
                        self.moveShape          = True
                        self.posMove            = pos
                        self.shapeEdit          = self.shapes.index(self.shapeSelected)
                    self.selectedShapeSignal.emit(True)
                    self.setCursor(CURSOR_MOVE)

            if self.nearest and self.shapeSelected is not None and not self.editShape:
                self.editShape                     = True
                self.shapeEdit                     = self.shapes.index(self.shapeSelected)
                self.setCursor(CURSOR_DRAW)
                
    def mouseReleaseEvent(self,ev):
        pos = self._transform(ev.pos())
        self.moveShape                          = False
        self.setCursor(CURSOR_DEFAULT)
        if self.editShape and self.shapeEdit is not None:
            self.editShape                      = False
            self.shapes[self.shapeEdit].corner  = None
            self.shapeEdit                      = None
            self.nearest                        = False
            
        
        if ev.button() == Qt.LeftButton and self.drawing and self.isDraw():
            if self.bbox.popUp():
                self.cancelEdit()
                self.setCursor(CURSOR_DEFAULT)
                self.newShape.emit(self.current)
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
    
    def disToShape(self,pos,shape):
        x0,y0 = pos.x(),pos.y()
        tl = shape.rect.topLeft()
        br = shape.rect.bottomRight()
        x,y = tl.x(),tl.y()
        X,Y = br.x(),br.y()
        if x <= x0 <= X and y <= y0 <= Y:
            return min(x0-x,X-x0,y0-y,Y-y0)
        else:
            return -1
    def findShapeNearest(self,pos):
        if self.shapes:
            dis = []
            for i,shape in enumerate(self.shapes):
                d = self.disToShape(pos,shape)
                if d == 0:
                    dis.append(0)
                else:
                    dis.append(1/d)
            if max(dis) >= 0:
                return np.argmax(dis)
            else:
                return None
        else:
            return None

    def isNearestCorner(self,pos,shape):
        def distance(p1,p2):
            x1,y1 = p1.x(),p1.y()
            x2,y2 = p2.x(),p2.y()
            return np.sqrt((x1-x2)**2+(y1-y2)**2)
        epsilon = 10.
        for point in shape.points:
            d = distance(pos,point)
            if d < epsilon:
                return True,point
        return False,None

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    wd = QMainWindow()
    canvas = Canvas()
    canvas.edit = True
    wd.setCentralWidget(canvas)
    wd.show()
    sys.exit(app.exec_())