from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_myForm import Ui_myForm

class myForm(QMainWindow):
    def __init__(self):
        super(myForm, self).__init__(None)
        self.setWindowFlags(Qt.Window)
        self.ui = Ui_myForm()
        self.ui.setupUi(self)

        self.ui.widget.installEventFilter(self)

        self.image = QPixmap("images.png")
        self.qImage = self.image.toImage()

        self.drawing = False
        self.startPoint = QPoint()
        self.rectCrop = QRect()

        # painter
    def paintEvent(self, event):
        painter = QPainter(self)
        r = self.ui.widget.geometry()
        painter.drawPixmap(r, self.image)
        painter.drawPixmap(self.ui.miniWidget.geometry(),QPixmap().fromImage(self.qImage.copy(self.rectCrop)))

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            print("press")
            self.drawing = True
            self.startPoint = event.pos()

        elif event.type() == QEvent.MouseButtonRelease:
            self.drawing = False
            pass

        elif event.type() == QEvent.MouseMove:
            if self.drawing:
                # self.image = QPixmap("images.png")
                self.image = QPixmap().fromImage(self.qImage)

                rx = self.image.width()/self.ui.widget.width()
                ry = self.image.height()/self.ui.widget.height()

                painter = QPainter(self.image)
                painter.begin(self)
                painter.setPen(QPen(Qt.red,1, Qt.SolidLine))

                painter.drawRect(int(self.startPoint.x()*rx),int(self.startPoint.y()*ry)
                                ,int(event.x()*rx-self.startPoint.x()*rx),int(event.y()*ry-self.startPoint.y()*ry))

                self.rectCrop = QRect(int(self.startPoint.x()*rx),int(self.startPoint.y()*ry)
                                ,int(event.x()*rx-self.startPoint.x()*rx),int(event.y()*ry-self.startPoint.y()*ry))

                painter.end()
                self.update()

        elif event.type() == Qt.RightButton:
            pass

        return super(myForm, self).eventFilter(obj, event)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.drawing = True
    #         self.startPoint = event.pos()

    # def mouseMoveEvent(self, event):
    #     print("mouse")
    #     if event.buttons() and Qt.LeftButton and self.drawing:
    #         # self.image = QPixmap("images.png")
    #         self.image = QPixmap().fromImage(self.qImage)

    #         rx = self.image.width()/self.ui.widget.width()
    #         ry = self.image.height()/self.ui.widget.height()

    #         painter = QPainter(self.image)
    #         painter.begin(self)
    #         painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))

    #         x,y = self.ui.widget.x(),self.ui.widget.y()
    #         painter.drawRect(self.startPoint.x()-x,self.startPoint.y()-y
    #         ,self.event.x()-x,self.event.y()-y)

    #         # self.lastPoint = event.pos()
    #         painter.end()
    #         self.update()
            

    # def mouseReleaseEvent(self, event):
    #     if event.button == Qt.LeftButton:
    #         self.drawing = False


    def __del__(self):
        self.ui = None