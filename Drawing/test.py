import sys
from PyQt5.QtCore import Qt, QPoint,QRect
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QPen

class Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.drawing = False
        self.startPoint = QPoint()
        self.image = QPixmap("images.png")
        self.qImage = self.image.toImage()
        self.setGeometry(0, 0, 640, 480)
        # self.resize(self.image.width(), self.image.height())
        self.show()

    def paintEvent(self, event):
        print("paint")
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.startPoint = event.pos()

    def mouseMoveEvent(self, event):
        print("mouse")
        if event.buttons() and Qt.LeftButton and self.drawing:
            # self.image = QPixmap("images.png")
            self.image = QPixmap().fromImage(self.qImage)

            rx = self.image.width()/self.width()
            ry = self.image.height()/self.height()

            painter = QPainter(self.image)
            painter.begin(self)
            painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))

            painter.drawRect(int(self.startPoint.x()*rx),int(self.startPoint.y()*ry)
            ,int(event.x()*rx-self.startPoint.x()*rx),int(event.y()*ry-self.startPoint.y()*ry))

            # self.lastPoint = event.pos()
            painter.end()
            self.update()
            

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())