from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from header.treeShapeUi import Ui_TreeShape
from libs_.utils import *

class TreeShapeDlg(QWidget):
    def __init__(self,parent):
        super(TreeShapeDlg,self).__init__(parent)
        self.ui = Ui_TreeShape()
        self.ui.setupUi(self)
        self.setLayout(self.ui.verticalLayout)
        self.setMaximumWidth(300)
        self.setMinimumWidth(200)
        self.currentItem = None
        self.window = self.parent().canvas

        addItems(self.ui.listWidget,["binary",'blur','morpology'
                                ,'removeBlobs','ocr','matching'])
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(not Qt.Checked)

        # self.ui.listShape.itemClicked.connect(self.itemClicked)
        self.ui.listShape.itemSelectionChanged.connect(self.itemSelectionChanged)
        self.ui.listShape.itemClicked.connect(self.itemClicked)

        self.ui.listShape.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listShape.customContextMenuRequested.connect(self.selectMenu)
    
    def selectedShape(self,selected):
        if selected:
            shape = self.window.selectedShape
            item = self.window.shapesToItems[shape]
            self.window.drawShapes(shape=shape)
            item.setSelected(True)
            self.window.setEnableMenu(True)
        else:
            self.window.drawShapes()
            self.ui.listShape.clearSelection()
            self.currentItem = None
            self.window.setEnableMenu(False)

    def deleteShape(self):
        self.window.shapes.remove(self.window.selectedShape)
        self.ui.listShape.takeItem(self.ui.listShape.row(self.currentItem))

        del self.window.itemsToShapes[self.currentItem]
        del self.window.shapesToItems[self.window.selectedShape]
        self.currentItem = None
        self.window.selectedShape = None
        self.ui.listShape.clearSelection()

        self.window.drawShapes()
    
    def newShape(self):
        shape = self.window.shapes[-1]
        self.addShape(shape)

    # def itemClicked(self,item):
    #     self.window.selectedShape = self.window.itemsToShapes[self.currentItem]
    #     self.window.drawShapes(self.window.image.copy(),self.window.selectedShape)
    #     self.window.setEnableMenu(True)

    def itemClicked(self,item):
        self.window.selectedShape = self.window.itemsToShapes[item]
        self.currentItem = item
        self.window.drawShapes(self.window.image.copy(),self.window.selectedShape)
        self.window.setEnableMenu(True)
        pass

    def addShape(self,shape):
        x,y,w,h = shape.r
        item = HashableQListWidgetItem("%d,%d,%d,%d"%(x,y,w,h))
        self.ui.listShape.addItem(item)

        item.setSelected(True)
        self.currentItem = item
        self.window.selectedShape = shape

        self.window.itemsToShapes[item] = shape
        self.window.shapesToItems[shape] = item

        self.window.drawShapes(self.window.image.copy(),shape)
        
        
    def itemSelectionChanged(self):
        items = self.ui.listShape.selectedItems()
        if items:
            item = items[0]            

    def selectMenu(self,point):
        action = self.window.menu.exec_(self.mapToParent(QCursor.pos()))
        
        # if action == self.window.crop:
        #     pass
        # if action == self.window.mean:
        #     pass
        # if action == self.window.computeArea:
        #     self.window.computeAreaSignal.emit()
        # if action == self.window.computeDistance:
        #     self.window.computeDistanceSignal.emit()
        # if action == self.window.deleteShape:
        #     self.window.deleteShapeSignal.emit()
