from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_myForm import Ui_myForm

import os,time,cv2,numpy as np

class struct(object):
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)

Font = struct(color="#00ff7f",lw=2,font=("Arial 10 bold"))

class myForm(QMainWindow):
    def __init__(self):
        super(myForm, self).__init__(None)
        self.setWindowFlags(Qt.Window)
        self.ui = Ui_myForm()
        self.ui.setupUi(self)
        # action 
        action = [self.ui.actionOpen,self.ui.actionSave,self.ui.actionSave_As,self.ui.actionExit
                    ,self.ui.actionColor,self.ui.actionFont]
        tooltip = ["Open File","Save Cropped Image","Save As File","Exit?","Color","Font"]
        shortcut = ["Ctrl+n","Ctrl+s","Ctrl+Shift+s","Ctrl+q","Ctrl+a","Ctrl+d"]
        icon = ["ico/open.png","ico/save.png","ico/save_as.png","ico/exit.png","ico/color.png","ico/font.png"]
        for i,act in enumerate(action) : 
            act.triggered.connect(self.trigger)
            act.setStatusTip(tooltip[i])
            act.setShortcut(shortcut[i])
            act.setIcon(QIcon(icon[i]))
            
        self.ui.widget.installEventFilter(self)

        self.image = None
        self.qImage = None

        self.drawing = False
        self.startPoint = QPoint()
        self.rectCrop = QRect()

        # painter
    def paintEvent(self, event):
        if self.image is None:
            return
        painter = QPainter(self)
        painter.drawPixmap(self.ui.widget.geometry(), self.image)
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
            if self.drawing and self.image is not None:
                # self.image = QPixmap("images.png")
                self.image = QPixmap().fromImage(self.qImage)

                rx = self.image.width()/self.ui.widget.width()
                ry = self.image.height()/self.ui.widget.height()

                painter = QPainter(self.image)
                painter.begin(self)
                painter.setPen(QPen(QColor(Font.color),Font.lw,Qt.SolidLine))

                painter.drawRect(int(self.startPoint.x()*rx),int(self.startPoint.y()*ry)
                                ,int(event.x()*rx-self.startPoint.x()*rx),int(event.y()*ry-self.startPoint.y()*ry))

                self.rectCrop = QRect(int(self.startPoint.x()*rx),int(self.startPoint.y()*ry)
                                ,int(event.x()*rx-self.startPoint.x()*rx),int(event.y()*ry-self.startPoint.y()*ry))

                painter.end()
                self.update()

        elif event.type() == Qt.RightButton:
            pass

        return super(myForm, self).eventFilter(obj, event)
    def trigger(self):
        if self.sender() == self.ui.actionOpen:
            print("open")
            fileName, _ = QFileDialog.getOpenFileName(self,"Select File", "","All Files (*);;JPG Files (*.jpg)")
            if fileName == "":
                return
            self.image = QPixmap(fileName)  
            self.qImage = self.image.toImage()  
        elif self.sender() == self.ui.actionColor:
            color = QColorDialog.getColor()
            if color.isValid():
                Font.color = color.name()  
        elif self.sender() == self.ui.actionFont:
            font, ok = QFontDialog.getFont()
            if ok :
                Font.font = font.toString()
        elif self.sender() == self.ui.actionSave:
            filename = time.strftime("data/%d%m%y_%H%M%S.jpg")
            qPixmap = QPixmap().fromImage(self.qImage.copy(self.rectCrop))
            qPixmap.save(filename)
            pass
        pass
    
    # ======= Function
    # def showImage(self,widget,qPixmap):
    #     painter = QPainter(self)
    #     painter.drawPixmap(widget.geometry(),qPixmap)
    #     del painter
    # ========

    def __del__(self):
        self.ui = None