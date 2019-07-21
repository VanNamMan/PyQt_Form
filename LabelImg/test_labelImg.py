from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from libs.canvas import *
from libs.utils import *
from libs.hashableQListWidgetItem import *
from libs.toolBar import ToolBar
from libs.labelDialog import *
from libs.zoomWidget import ZoomWidget

from libs.cvLib import *
from UI_Convert.paramsCv import paramsCv

import os,time
from functools import partial


__appname__ = "CopyRight2019 label master."
__imageFile__ = [".jpg",".png",".bmp",".gif",".PNG"]

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
         # self.setFixedSize(800, 600)
         self.setWindowTitle("Label Master")
         self.labelCoordinates = QLabel('')
         self.statusBar().addPermanentWidget(self.labelCoordinates)
         # intit 
         self.cvMat = None
         self.qImage = None
         self.dirty = False
         self.saveFolder = None
         self.filePath = ""
         self.prevLabel = "Enter object label"
         fileLabel = "label.txt"
         listLabel = []
         if os.path.exists(fileLabel):
             with open(fileLabel,"r") as inFile:
                listLabel = inFile.readline().split(",")
         self.labelDialog = LabelDialog(listItem=listLabel)
         self.itemsToShapes = {}
         self.shapesToItems = {}
         self._noSelectionSlot = False
         self._beginner = True
         self.statusBar().showMessage('%s' % __appname__)
         # self.statusBar().show()
         #============ menu=========
         self.menus = struct(
            file=self.menu('&File'),
            edit=self.menu('&Edit'),
            view=self.menu('&View'),
            help=self.menu('&Help'),
            labelList = QMenu(),
            fileLog = QMenu())

         #================init UI ==============
         action = partial(newAction,self)

         #=======toolBar==========
         openFile = action("Open",self.open
            ,"Ctrl+o","res/open.png","Open image file")
         createShape = action("Create rect box",self.createShape
            ,"r","res/draw.png","Start draw rectangle")
         saveFile = action("Save",self.save
            ,"Ctrl+s","res/save.png","Save parameters")
         editLabel = action("Edit label",self.editLabel
            ,"Ctrl+e","res/edit.png","Editting label", enabled=False)
         deleteShape = action("Delete shape",self.delete
            ,"Ctrl+d","res/delete.png","Delete shape selected", enabled=False)

         implement = action("Implement",self.implement
            ,"a","res/event.png","Implement function", enabled=False)

         zoomIn = action('zoomin', partial(self.addZoom, 10),
                        'Ctrl++', 'res/zoom-in.png','zoominDetail', enabled=False)
         zoomOut = action('zoomout', partial(self.addZoom, -10),
                         'Ctrl+-', 'res/zoom-out.png','zoomoutDetail', enabled=False)
         zoomOrg = action('originalsize', partial(self.setZoom, 100),
                         'Ctrl+=', 'res/zoom.png','originalsizeDetail', enabled=False)
         fitWindow = action('fitWin', self.setFitWindow,
                           'Ctrl+F', 'res/fit-window.png','fitWinDetail',
                           checkable=True, enabled=False)
         fitWidth = action('fitWidth', self.setFitWidth,
                          'Ctrl+Shift+F', 'res/fit-width.png','fitWidthDetail',
                          checkable=True, enabled=False)

         clearAll = action('clearAll', self.clearList,
                          'Ctrl+Shift+d', 'res/clear-all.png','Clear all list items',
                          checkable=True, enabled=True)

         actionMenuFile = [openFile,saveFile,createShape,implement,editLabel,deleteShape]
         addActions(self.menus.file,actionMenuFile)

         actionToolbar = (openFile,saveFile,createShape,editLabel,implement)
         self.toolbar("Tools",actions=actionToolbar)

         self.zoomWidget = ZoomWidget()
         zoom = QWidgetAction(self)
         zoom.setDefaultWidget(self.zoomWidget)
         self.zoomWidget.setWhatsThis(
            u"Zoom in or out of the image. Also accessible with"
            " %s and %s from the canvas." % (fmtShortcut("Ctrl+[-+]"),
                                             fmtShortcut("Ctrl+Wheel")))
         self.zoomWidget.setEnabled(False)
         
        # Group zoom controls into a list for easier toggling.
         beginner = (implement,editLabel,deleteShape)
         self.actions = struct(openFile=openFile,saveFile=saveFile,createShape=createShape
                                ,editLabel=editLabel,deleteShape=deleteShape
                                ,implement=implement,zoomIn=zoomIn,zoomOut=zoomOut
                                ,zoomOrg=zoomOrg,fitWidth=fitWidth,fitWindow=fitWindow
                                ,beginner=beginner)

         self.zoomWidget.valueChanged.connect(self.paintCanvas)

         self.zoomMode = self.MANUAL_ZOOM
         self.scalers = {
            self.FIT_WINDOW: self.scaleFitWindow,
            self.FIT_WIDTH: self.scaleFitWidth,
            # Set to one to scale to 100% when loading files.
            self.MANUAL_ZOOM: lambda: 1,
         }
         listLayout = QVBoxLayout()
         listLayout.setContentsMargins(0, 0, 0, 0)

        # Create a widget for using default label
         self.useDefaultLabelCheckbox = QCheckBox('useDefaultLabel')
         self.useDefaultLabelCheckbox.setChecked(False)
         self.defaultLabelTextLine = QLineEdit()
         useDefaultLabelQHBoxLayout = QHBoxLayout()
         useDefaultLabelQHBoxLayout.addWidget(self.useDefaultLabelCheckbox)
         useDefaultLabelQHBoxLayout.addWidget(self.defaultLabelTextLine)
         useDefaultLabelContainer = QWidget()
         useDefaultLabelContainer.setLayout(useDefaultLabelQHBoxLayout)

        # Create a widget for edit and diffc buttonp
         self.editButton = QToolButton()
         self.editButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
         self.editButton.setDefaultAction(editLabel)

         self.implementButton = QToolButton()
         self.implementButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
         self.implementButton.setDefaultAction(implement)

         buttonLayout = QHBoxLayout()
         buttonLayout.setContentsMargins(0, 0, 0, 0)


        # Add some of widgets to listLayout
         buttonLayout.addWidget(self.implementButton)
         buttonLayout.addWidget(self.editButton)
         listLayout.addLayout(buttonLayout)

         listLayout.addWidget(useDefaultLabelContainer)

        # Create and add a widget for showing current label items
         self.labelList = QListWidget()
         addActions(self.menus.labelList, (editLabel, deleteShape))
         self.labelList.setContextMenuPolicy(Qt.CustomContextMenu)
         self.labelList.customContextMenuRequested.connect(
            self.popLabelListMenu)
         self.labelList.itemActivated.connect(self.labelSelectionChanged)
         self.labelList.itemSelectionChanged.connect(self.labelSelectionChanged)
         self.labelList.itemDoubleClicked.connect(self.editLabel)
        # Connect to itemChanged to detect checkbox changes.
         self.labelList.itemChanged.connect(self.labelItemChanged)
         listLayout.addWidget(self.labelList)

         labelListContainer = QWidget()
         labelListContainer.setLayout(listLayout)

         self.fileLogWidget = QListWidget()
         addActions(self.menus.fileLog, [clearAll])
         self.fileLogWidget.setContextMenuPolicy(Qt.CustomContextMenu)
         self.fileLogWidget.customContextMenuRequested.connect(
            self.popfileLogMenu)
         # self.fileLogWidget.itemDoubleClicked.connect(self.fileitemDoubleClicked)
         # self.fileLogWidget.itemChanged.connect(self.fileLogRowChanged)
         fileLogLayout = QVBoxLayout()
         fileLogLayout.setContentsMargins(0, 0, 0, 0)
         fileLogLayout.addWidget(self.fileLogWidget)
         fileLogContainer = QWidget()
         fileLogContainer.setLayout(fileLogLayout)

    
         self.dock = QDockWidget('boxLabelText', self)
         self.dock.setObjectName('labels')
         self.dock.setWidget(labelListContainer)

         self.filedock = QDockWidget('fileLog', self)
         self.filedock.setObjectName('files')
         self.filedock.setWidget(fileLogContainer)

         self.parameterdock = QDockWidget('paramsVision', self)
         self.parameterdock.setObjectName('params')
         self.paramsCvWidget = paramsCv(self)
         self.parameterdock.setWidget(self.paramsCvWidget)

         self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
         self.dockFeatures = QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable
         self.dock.setFeatures(self.dock.features() ^ self.dockFeatures)

         self.addDockWidget(Qt.RightDockWidgetArea, self.filedock)
         self.filedock.setFeatures(QDockWidget.DockWidgetFloatable)

         self.addDockWidget(Qt.RightDockWidgetArea, self.parameterdock)
         self.parameterdock.setFeatures(QDockWidget.DockWidgetFloatable)

         # ==============Canvas================
         self.canvas = Canvas(self)
         # contextMenu
         addActions(self.canvas.menus[0],self.actions.beginner)
         #=================
         qImage = QImage(640,480,QImage.Format_RGBA8888)
         self.canvas.loadPixmap(QPixmap.fromImage(qImage))

        
         scroll = QScrollArea()
         scroll.setWidget(self.canvas)
         # scroll.setWidget(self.listWidget)
         scroll.setWidgetResizable(True)
         self.scrollBars = {
            Qt.Vertical: scroll.verticalScrollBar(),
            Qt.Horizontal: scroll.horizontalScrollBar()
         }
         self.scrollArea = scroll

         #signal Canvas
         self.canvas.scrollRequest.connect(self.scrollRequest)
         self.canvas.newShape.connect(self.newShape)
         self.canvas.shapeMoved.connect(self.setDirty)
         self.canvas.selectionChanged.connect(self.shapeSelectionChanged)
         self.canvas.zoomRequest.connect(self.zoomRequest)
         self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)

         self.setCentralWidget(scroll)

         self.fitState()
#
         # ==============================

         palette = self.palette()
         role = self.backgroundRole()
         palette.setColor(role, QColor(200, 232, 232, 255))
         self.setPalette(palette)

         palette = self.canvas.palette()
         role = self.canvas.backgroundRole()
         palette.setColor(role, QColor(200, 232, 232, 255))
         self.canvas.setPalette(palette)
     #======Functions==
     def getStrDateTime(self):
        return time.strftime("%y%m%d_%H%M%S")

     def saveImage(self,image=None):
        if self.saveFolder is None:
            self.saveFolder = QFileDialog.getExistingDirectory(self,"Open Directory",os.getcwd(),
                QFileDialog.ShowDirsOnly| QFileDialog.DontResolveSymlinks)
        if os.path.exists(self.saveFolder):
            if isinstance(image,np.ndarray):
                filepath = os.path.join(self.saveFolder,self.getStrDateTime()+".jpg")
                cv2.imwrite(filepath,image)

     def logFile(self,obj):
        txt = time.strftime("%H:%M:%S ")+str(obj)
        self.fileLogWidget.addItem(txt)

     def getOCR(self,cvImg,bLog=True):
        txts = ""
        data = get_text(cvImg)
        if bLog:
            for txt in data:
                if txt != "":
                    txts += "\t" + txt + "\n"
            self.logFile(txts)
        return data

     def getBarCode(self,cvImg,bLog=True):
        codes = getBarcode(cvImg)
        if bLog:
            if codes:
                for code,dtype in codes:
                    self.logFile("Code : %s , type : %s"%(code,dtype))
            else:
                self.logFile("Code : None")
        return codes

     # actions 
     def read(self,filename,default=None):
        try:
            with open(filename,"rb") as f:
                return f.read()
        except:
            return default

     def createShape(self):
        self.canvas.setEditing(False)
        self.actions.createShape.setEnabled(False)

     def remLabel(self, shape):
        if shape is None:
            # print('rm empty label')
            return
        item = self.shapesToItems[shape]
        self.labelList.takeItem(self.labelList.row(item))
        del self.shapesToItems[shape]
        del self.itemsToShapes[item]

     def delete(self):
        self.remLabel(self.canvas.deleteSelected())
     
     def implement(self):
        shape = self.canvas.selectedShape
        rect,label = self.formatShape(shape)
        roi = self.qImage.copy(rect)
        cvRoi = qImageToCvMat(roi)
        if label == "OCR":
            self.getOCR(cvRoi)
        elif label == "Barcode":
            codes = self.getBarCode(cvRoi)
        elif label == "Crop":
            self.saveImage(cvRoi)
        
     def open(self):
        filters = "All File(*.*);;JPG iamge (*.jpg)"
        self.filePath,_ = QFileDialog.getOpenFileName(self,'Select File',"", filters)
        _,extension = os.path.splitext(self.filePath)
        if self.filePath != "" and extension in __imageFile__ and os.path.exists(self.filePath):

            self.resetState()
            self.qImage = QImage(self.filePath)
            # self.qImage = self.qImage.convertToFormat(QImage.Format_ARGB32)
            self.logFile(self.qImage.format())
            # self.cvMat = cv2.imread(self.filePath)
            # if isinstance(self.cvMat,np.ndarray):
            # qImg = cVMatToQImage(self.cvMat[...,::-1])
            self.canvas.loadPixmap(QPixmap.fromImage(self.qImage))

            self.fitState()
     def save(self):
        pass

     def setDirty(self):
        self.dirty = True
        # self.actions.createShape.setEnabled(False)

     def formatShape(self,shape):
            points = shape.points
            tl = points[0].toPoint()
            br = points[2].toPoint()
            label = shape.label
            cvRect = QRect(tl,br)
            return [cvRect,label]

     # redraw rect
     # ================add and edit Label===========================
     def beginner(self):
        return self._beginner

     def advanced(self):
        return not self.beginner()

     def toggleDrawingSensitive(self, drawing=True):
        """In the middle of drawing, toggling between modes should be disabled."""
        # self.actions.editLabel.setEnabled(not drawing)
        # self.actions.implement.setEnabled(not drawing)
        if not drawing and self.beginner():
            # Cancel creation.
            print('Cancel creation.')
            self.canvas.setEditing(True)
            self.canvas.restoreCursor()
            self.actions.createShape.setEnabled(True)
     def popLabelListMenu(self, point):
        self.menus.labelList.exec_(self.labelList.mapToGlobal(point))

     def popfileLogMenu(self, point):
        self.menus.fileLog.exec_(self.fileLogWidget.mapToGlobal(point))

     def currentItem(self):
        items = self.labelList.selectedItems()
        if items:
            return items[0]
        return None

     def shapeSelectionChanged(self, selected=False):
        if self._noSelectionSlot:
            self._noSelectionSlot = False
        else:
            shape = self.canvas.selectedShape
            if shape:
                self.shapesToItems[shape].setSelected(True)
            else:
                self.labelList.clearSelection()

        self.actions.implement.setEnabled(selected)
        self.actions.editLabel.setEnabled(selected)
        self.actions.deleteShape.setEnabled(selected)
        # self.actions.shapeLineColor.setEnabled(selected)
        # self.actions.shapeFillColor.setEnabled(selected)

     def editLabel(self):
        if not self.canvas.editing():
            return
        item = self.currentItem()
        if not item:
            return
        text = self.labelDialog.popUp(item.text())
        if text is not None:
            item.setText(text)
            item.setBackground(generateColorByText(text))
            self.setDirty()

     def labelSelectionChanged(self):
        item = self.currentItem()
        if item and self.canvas.editing():
            self._noSelectionSlot = True
            self.canvas.selectShape(self.itemsToShapes[item])
            shape = self.itemsToShapes[item]
            # self.actions.editLabel.setEnabled(True)
            # self.actions.implement.setEnabled(True)

     def labelItemChanged(self, item):
        shape = self.itemsToShapes[item]
        label = item.text()
        if label != shape.label:
            shape.label = item.text()
            shape.line_color = generateColorByText(shape.label)
            self.setDirty()
        else:  # User probably changed item visibility
            self.canvas.setShapeVisible(shape, item.checkState() == Qt.Checked)

     def addLabel(self,shape):
         item = HashableQListWidgetItem(shape.label)
         item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
         item.setCheckState(Qt.Checked)
         item.setBackground(generateColorByText(shape.label))
         self.itemsToShapes[item] = shape
         self.shapesToItems[shape] = item
         self.labelList.addItem(item)
     # =================signal Canvas==========================
     def newShape(self):
        #Pop-up and give focus to the label editor. 
        if self.useDefaultLabelCheckbox.isChecked() and self.defaultLabelTextLine.text():
            label =  self.defaultLabelTextLine.text()   
        else:
            label = self.prevLabel     
        text = self.labelDialog.popUp(text = label)
        if text :
            generate_color = generateColorByText(text)
            shape = self.canvas.setLastLabel(text, generate_color, generate_color)
            self.prevLabel = text
            self.canvas.setEditing(True)
            self.actions.createShape.setEnabled(True)
            self.addLabel(shape)
        else:
               self.canvas.resetAllLines()
     
     def setZoom(self, value):
        # self.actions.fitWidth.setChecked(False)
        # self.actions.fitWindow.setChecked(False)
        self.zoomMode = self.MANUAL_ZOOM
        self.zoomWidget.setValue(value)

     def addZoom(self, increment=10):
        self.setZoom(self.zoomWidget.value() + increment)

     def zoomRequest(self,delta):
        print(delta)
        # get the current scrollbar positions
        # calculate the percentages ~ coordinates
        h_bar = self.scrollBars[Qt.Horizontal]
        v_bar = self.scrollBars[Qt.Vertical]

        # get the current maximum, to know the difference after zooming
        h_bar_max = h_bar.maximum()
        v_bar_max = v_bar.maximum()

        # get the cursor position and canvas size
        # calculate the desired movement from 0 to 1
        # where 0 = move left
        #       1 = move right
        # up and down analogous
        cursor = QCursor()
        pos = cursor.pos()
        relative_pos = QWidget.mapFromGlobal(self, pos)

        cursor_x = relative_pos.x()
        cursor_y = relative_pos.y()

        w = self.scrollArea.width()
        h = self.scrollArea.height()

        # the scaling from 0 to 1 has some padding
        # you don't have to hit the very leftmost pixel for a maximum-left movement
        margin = 0.1
        move_x = (cursor_x - margin * w) / (w - 2 * margin * w)
        move_y = (cursor_y - margin * h) / (h - 2 * margin * h)

        # clamp the values from 0 to 1
        move_x = min(max(move_x, 0), 1)
        move_y = min(max(move_y, 0), 1)

        # zoom in
        units = delta / (8 * 15)
        scale = 10
        self.addZoom(scale * units)

        # get the difference in scrollbar values
        # this is how far we can move
        d_h_bar_max = h_bar.maximum() - h_bar_max
        d_v_bar_max = v_bar.maximum() - v_bar_max

        # get the new scrollbar values
        new_h_bar_value = h_bar.value() + move_x * d_h_bar_max
        new_v_bar_value = v_bar.value() + move_y * d_v_bar_max

        h_bar.setValue(new_h_bar_value)
        v_bar.setValue(new_v_bar_value)

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

     def setFitWindow(self, value=True):
        if value:
            self.actions.fitWidth.setChecked(False)
        self.zoomMode = self.FIT_WINDOW if value else self.MANUAL_ZOOM
        self.adjustScale()

     def setFitWidth(self, value=True):
        if value:
            self.actions.fitWindow.setChecked(False)
        self.zoomMode = self.FIT_WIDTH if value else self.MANUAL_ZOOM
        self.adjustScale()

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

     def clearList(self):
        # nRow = self.fileLogWidget.count()
        # for i in range(nRow):
        #     self.fileLogWidget.takeItem(i)
        self.fileLogWidget.clear()

     def resetState(self):
        self.labelList.clear()
        self.canvas.resetState()
        self.labelCoordinates.clear()
        self.canvas.setEnabled(False)
        self.canvas.verified = False
        
     def fitState(self):
        self.canvas.setEnabled(True)
        self.adjustScale(initial=True)
        self.paintCanvas()
        self.canvas.setFocus(True)
        
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
