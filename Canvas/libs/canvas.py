from libs.header import *
from libs.utils import *
from libs.bbox import BBox
from libs.shape import Shape

class Canvas(QWidget):
    cropSignal = pyqtSignal(Shape)
    newShape   = pyqtSignal(Shape)
    def __init__(self,parent=None):
        super(Canvas,self).__init__(parent)
        self.pixmap = QPixmap(640,480)
        self.scale = 1
        self.painter = QPainter()
        self.color = QColor(0,255,0)
        self.current = None
        self.shapeSelected = None
        self.shapes = []
        self.edit = False
        self.drawing = False
        self.recreate = False
        self.idRecreate = None

        self.tl = None
        self.br = None

        self.line_x = []
        self.line_y = []
        # context menu
        self.contextMenu = QMenu()
        action = partial(newAction,self)
        crop = action("Crop",self.crop,"ctrl+x","crop","Crop image")
        addActions(self.contextMenu,[crop])
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popUpMenu)
        # 
        self.loadPixmap(QPixmap("image/image.png"))
        self.setMouseTracking(True)

    def popUpMenu(self,pos):
        self.contextMenu.exec_(QCursor.pos())
    
    def crop(self):
        if self.selectedShape is not None:
            self.cropSignal.emit(self.self.selectedShape)
        else:
            self.cropSignal.emit(self.self.current)

    def formatShape(self,shape):
        x = int(shape[0].x())
        y = int(shape[0].y())
        w = int(shape[2].x() - shape[0].x())
        h = int(shape[2].y() - shape[0].y())
        return {
            "label"  : shape.label,
            "cvRect" : [x,y,w,h]
        }

    def setEditing(self):
        self.edit = True

    def loadPixmap(self,pixmap):
        self.pixmap = pixmap

    def selectedShape(self,i):
        for j in range(len(self.shapes)):
            self.shapes[j].selected = False
        if i is not None :
            self.shapes[i].selected = True
            self.shapeSelected = self.shapes[i]
        
    def hilightVertex(self,i,visible=False,corner=None):
        for j in range(len(self.shapes)):
            self.shapes[j].corner = None
            self.shapes[j].visible = False
        if i is not None:
            if visible:
                self.shapes[i].visible = True
            elif corner is not None:
                self.shapes[i].corner = corner

    def mouseMoveEvent(self,ev):
        pos = self.transformPos(ev.pos())
        self.hilightVertex(None)
        index = self.findShapeNearest(pos)
        self.hilightVertex(index,visible=True)
        for i in range(len(self.shapes)):
            corner = self.findCorner(pos,self.shapes[i])
            self.idRecreate = None
            if corner is not None:
                self.hilightVertex(i,corner=corner)
                self.idRecreate = i
                break
        if self.recreate and not self.drawing:
            self.br = pos
            self.shapes[self.idRecreate] = Shape(self.tl,self.br,self.idRecreate)

        if self.pixmap is None :
            return super(Canvas,self).mouseMoveEvent(ev)
        
        if self.edit:
            p1 = QPointF(0,pos.y())
            p2 = QPointF(self.pixmap.width(),pos.y())
            self.line_x = [p1,p2]

            p1 = QPointF(pos.x(),0)
            p2 = QPointF(pos.x(),self.pixmap.height())
            self.line_y = [p1,p2]
        
        elif self.drawing:
            self.br = pos
            self.current = Shape(self.tl,self.br,len(self.shapes))
    
    def mousePressEvent(self,ev):
        pos = self.transformPos(ev.pos())
        if self.edit:
            self.tl = pos
            self.drawing = True
            self.edit = False
            self.line_x = None
            self.line_y = None
        
        if ev.button() == Qt.LeftButton:
            if not self.drawing:
                index = self.findShapeNearest(pos)
                self.selectedShape(index)


    def mouseReleaseEvent(self,ev):
        if ev.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            if BBox().popUp():
                if self.current:
                    self.shapes.append(self.current)
                    self.newShape.emit(self.shapes[-1])    
            else:
                self.current = None
                self.tl = None
                self.br = None
                pass
    
    def findCorner(self,pos,shape,epsilon=10):
        d = self.disToShape(pos,shape)
        if d > 0:
            return None
        else:
            points = shape.points
            D = [self.distance(pos,p) for p in points]
            if (min(D) < epsilon):
                return np.argmin(D)
            else:
                return None

    def findShapeNearest(self,pos):
        if self.shapes:
            d_min = 2000
            index = None
            for i,shape in enumerate(self.shapes):
                d = self.disToShape(pos,shape)
                if 0 < d < d_min:
                    d_min = d
                    index = i
            return index
        else:
            return None
    
    def distance(self,p,q):
        point = p-q
        return np.sqrt(point.x()**2+point.y()**2)

    def disToShape(self,pos,shape):
        format_shape = self.formatShape(shape)
        x0,y0 = pos.x(),pos.y()
        x,y,w,h = format_shape["cvRect"]
        if x < x0 < x+w and y < y0 < y+h:
            dx = min(x0-x,x+w-x0)
            dy = min(y0-y,y+h-y0)
            return min(dx,dy)
        else:
            return -1
    
    def transformPos(self,pos):
        center = self.offsetToCenter()
        pos = (pos - center)/self.scale
        x_min = min(pos.x(),self.pixmap.width())
        y_min = min(pos.y(),self.pixmap.height())
        x_min = max(x_min,0)
        y_min = max(y_min,0)
        return QPointF(x_min,y_min)

    def paintEvent(self,ev):
        if not self.pixmap:
            return super(Canvas, self).paintEvent(ev)
        p = self.painter
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        p.translate(self.offsetToCenter())
        p.scale(self.scale,self.scale)
        p.drawPixmap(0,0,self.pixmap)

        if self.line_x:
            p.drawLine(self.line_x[0],self.line_x[1])
        if self.line_y:
            p.drawLine(self.line_y[0],self.line_y[1])

        if self.tl is not None and self.br is not None:
            p.drawRect(QRectF(self.tl,self.br))

        for shape in self.shapes:
            shape.paint(p)
        
        self.update()
        p.end()

    def offsetToCenter(self):
        W,H = self.width()-2,self.height()-2
        w,h = self.pixmap.width(),self.pixmap.height()
        x,y = w*self.scale/2,h*self.scale/2
        X,Y = W/2,H/2
        return QPointF(X-x,Y-y)

    def resizeEvent(self,ev):
        if self.pixmap is None:
            return super(Canvas, self).resizeEvent(ev)

        W,H = self.width()-2,self.height()-2
        w,h = self.pixmap.width(),self.pixmap.height()
        self.scale = min(W/w,H/h)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    wd = QMainWindow()
    canvas = Canvas(wd)
    scroll = QScrollArea(wd)

    scroll.setWidget(canvas)
    scroll.setWidgetResizable(True)
    
    wd.setCentralWidget(scroll)
    wd.show()
    sys.exit(app.exec_())