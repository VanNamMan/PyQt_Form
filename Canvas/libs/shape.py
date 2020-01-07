from libs.header import *
from libs.utils import *

class Shape(object):
    LINE_COLOR = QColor(0,255,0)
    def __init__(self,tl,br,label):
        super(Shape,self).__init__()
        self.points = [tl,QPointF(br.x(),tl.y()),br,QPointF(tl.x(),br.y())]
        self.selected = False
        self.visible  = False
        self.corner   = None
        self.label    = label

        # 
        self.vertex_fill_color        = DEFAULT_VERTEX_FILL_COLOR
        self.vertex_select_fill_color = DEFAULT_VERTEX_SELECT_FILL_COLOR
        self.fill_color               = DEFAULT_FILL_COLOR
        self.select_fill_color        = DEFAULT_SELECT_FILL_COLOR
        self.visible_fill_color       = DEFAULT_VISIBLE_FILL_COLOR

    def drawVertex(self, path, i):
        d = 10
        point = self.points[i]
        if self.corner is not None and i == self.corner:
            path.addRect(point.x() - d, point.y() - d, 2*d, 2*d)
        elif self.visible:
            path.addEllipse(point, d/2, d/2)
        else:
            path.addEllipse(point, d / 2.0, d / 2.0)
    
    def paint(self,painter):
        painter.setPen(QPen(self.LINE_COLOR))
        line_path = QPainterPath()
        vertex_path = QPainterPath()

        line_path.moveTo(self.points[0])

        for i, p in enumerate(self.points):
            line_path.lineTo(p)
            self.drawVertex(vertex_path,i)

        line_path.lineTo(self.points[0])
        #  draw rect
        painter.drawPath(line_path)
        # draw label
        if self.label:
            painter.drawText(self[0].x()-1,self[0].y()-1, "Shape-%d"%self.label)
        #  fill
        color = self.vertex_select_fill_color if (self.visible or self.corner is not None) else self.vertex_fill_color
        painter.fillPath(vertex_path, color)

        color = self.visible_fill_color if (self.visible or self.corner is not None) else self.fill_color
        color = self.select_fill_color if self.selected else color
        painter.fillPath(line_path, color)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value