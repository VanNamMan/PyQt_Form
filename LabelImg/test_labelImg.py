from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from libs.canvas import *
from libs.utils import *
from libs.toolBar import ToolBar
from libs.labelDialog import *
from libs.zoomWidget import ZoomWidget

import os,time

__appname__ = "CopyRight2019 label master."

class WindowMixin(object):

    def menu(self, title, actions=None):
        menu = self.menuBar().addMenu(title)
        if actions:
            addActions(menu, actions)
        return menu
    def toolbar(self, title, actions=None):
        toolbar = ToolBar(title)
        toolbar.setObjectName(u'%sToolBar' % title)
        # toolbar.setOrientation(Qt.Vertical)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if actions:
            addActions(toolbar, actions)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        return toolbar
class labelMaster(QMainWindow,WindowMixin):
     FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = list(range(3))
     def __init__(self):
         QWidget.__init__(self)
         self.setFixedSize(800, 600)
         self.labelCoordinates = QLabel('')
         self.statusBar().addPermanentWidget(self.labelCoordinates)
         
         self.dirty = False
         self.filePath = ""
         self.prevLabel = "Enter object label"
         self.labelDialog = LabelDialog(listItem=["Add Rect","OCR","Barcode","Crop"])
         self.statusBar().showMessage('%s started.' % __appname__)
         # self.statusBar().show()
         #============ menu=========
         self.menus = struct(
            file=self.menu('&File'),
            edit=self.menu('&Edit'),
            view=self.menu('&View'),
            help=self.menu('&Help'))

         #=======toolBar==========
         actions = [newAction(self,"Open",slot=self.open,icon="res/open-file-icon.png")
         			,newAction(self,"Save",slot=self.save,icon="res/ooo-draw-icon.png")
         			,newAction(self,"Create Rect",slot=self.createRect,icon="res/Save-as-icon.png")]
         self.toolbar("Tools",actions=actions)
         addActions(self.menus.file,actions)

         #================
         self.zoomWidget = ZoomWidget()

         self.zoomMode = self.MANUAL_ZOOM
         self.scalers = {
            self.FIT_WINDOW: self.scaleFitWindow,
            self.FIT_WIDTH: self.scaleFitWidth,
            # Set to one to scale to 100% when loading files.
            self.MANUAL_ZOOM: lambda: 1,
         }

         layout = QVBoxLayout(self)

         # ==============================
         self.canvas = Canvas(self)
         self.canvas.setStyleSheet("QWidget{border: 3px solid red;}")
         
         qImage = QImage("res/Bird.ico")
         self.canvas.loadPixmap(QPixmap.fromImage(qImage))
        
         scroll = QScrollArea()
         scroll.setWidget(self.canvas)
         scroll.setWidgetResizable(True)
         self.scrollBars = {
            Qt.Vertical: scroll.verticalScrollBar(),
            Qt.Horizontal: scroll.horizontalScrollBar()
         }
         self.scrollArea = scroll
         # self.canvas.scrollRequest.connect(self.scrollRequest)

         self.canvas.newShape.connect(self.newShape)
         # self.canvas.shapeMoved.connect(self.setDirty)
         # self.canvas.selectionChanged.connect(self.shapeSelectionChanged)
         # self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)

         self.setCentralWidget(scroll)
 		
         # self.canvas.setEnabled(True)
         # self.adjustScale(initial=True)
         # self.paintCanvas()
         # self.canvas.setFocus(True)
         # set mode drawing rect
         self.fitState()
         self.setCreateMode()
         #=============
         layout.addWidget(self.canvas)
        
         self.setLayout(layout)
         # ==============================

         palette = self.palette()
         role = self.backgroundRole()
         palette.setColor(role, QColor(232, 232, 232, 255))
         self.setPalette(palette)

         palette = self.canvas.palette()
         role = self.canvas.backgroundRole()
         palette.setColor(role, QColor(232, 232, 232, 255))
         self.canvas.setPalette(palette)

     def createRect(self):
     	self.canvas.setEditing(False)
     def open(self):
     	filters = "All File(*.*);;JPG iamge (*.jpg)"
     	self.filePath,_ = QFileDialog.getOpenFileName(self,'Select File',"", filters)
     	if self.filePath != "" and os.path.exists(self.filePath):

     		self.resetState()
     		self.canvas.setEnabled(False)
     		self.canvas.verified = False

     		imageData = self.read(self.filePath, None)
     		qImage = QImage.fromData(imageData)
     		self.canvas.loadPixmap(QPixmap.fromImage(qImage))

     		self.canvas.setEnabled(True)
     		self.adjustScale(initial=True)
     		self.paintCanvas()
     		self.canvas.setFocus(True)

     	pass
     def save(self):
     	[print(self.formatShape(shape)) for shape in self.canvas.shapes]
     def setDirty(self):
        self.dirty = True
        # self.actions.save.setEnabled(True)
     def formatShape(self,shape):
     		points = shape.points
     		tl = points[0].toPoint()
     		br = points[2].toPoint()
     		label = shape.label
     		cvRect = QRect(tl,br)
     		return [cvRect,label]
     def newShape(self):
        #Pop-up and give focus to the label editor.             
        text = self.labelDialog.popUp(text = self.prevLabel)
        if text :
        	generate_color = generateColorByText(text)
        	shape = self.canvas.setLastLabel(text, generate_color, generate_color)
        	self.prevLabel = text
        	self.canvas.setEditing(True)
        	if text == "Crop":
        		print(self.formatShape(shape))
        	
        else:
        	self.canvas.resetAllLines() # redraw rect
        pass
     def scrollRequest(self, delta, orientation):
        units = - delta / (8 * 15)
        bar = self.scrollBars[orientation]
        bar.setValue(bar.value() + bar.singleStep() * units)
     def setCreateMode(self):
     	 self.canvas.setEditing(False)
     def paintCanvas(self):
         # assert not self.image.isNull(), "cannot paint null image"
         self.canvas.scale = 0.01 * self.zoomWidget.value()
         self.canvas.adjustSize()
         self.canvas.update()
     def adjustScale(self, initial=False):
        value = self.scalers[self.FIT_WINDOW if initial else self.zoomMode]()
        self.zoomWidget.setValue(int(100 * value))
     def scaleFitWindow(self):
        """Figure out the size of the pixmap in order to fit the main widget."""
        e = 2.0  # So that no scrollbars are generated.
        w1 = self.centralWidget().width() - e
        h1 = self.centralWidget().height() - e
        a1 = w1 / h1
        # Calculate a new scale value based on the pixmap's aspect ratio.
        w2 = self.canvas.pixmap.width() - 0.0
        h2 = self.canvas.pixmap.height() - 0.0
        a2 = w2 / h2
        return w1 / w2 if a2 >= a1 else h1 / h2
     def scaleFitWidth(self):
        # The epsilon does not seem to work too well here.
        w = self.centralWidget().width() - 2.0
        return w / self.canvas.pixmap.width()
     def resetState(self):
        # self.filePath = None
        self.canvas.resetState()
        self.labelCoordinates.clear()
        
     def fitState(self):
     	self.canvas.setEnabled(True)
     	self.adjustScale(initial=True)
     	self.paintCanvas()
     	self.canvas.setFocus(True)
        
     def read(self,filename,default=None):
     	try:
     		with open(filename,"rb") as f:
     			return f.read()
     	except:
     		return default
     def resizeEvent(self, event):
        if self.canvas and self.zoomMode != self.MANUAL_ZOOM:
            self.adjustScale()
        super(labelMaster, self).resizeEvent(event)

def main():
     import sys
     a = QApplication(sys.argv)
     w = labelMaster()
     w.show()
     a.exec_()

if __name__ == "__main__":
     main()