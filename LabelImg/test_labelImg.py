from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from libs.canvas import *
from libs.zoomWidget import ZoomWidget

BB = QDialogButtonBox

class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None, listItem=None):
        super(LabelDialog, self).__init__(parent)
        layout = QVBoxLayout()

        self.edit = QLineEdit()
        self.edit.setText(text)
        layout.addWidget(self.edit)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                self.listWidget.addItem(item)
            self.listWidget.itemClicked.connect(self.listItemClick)
            self.listWidget.itemDoubleClicked.connect(self.listItemDoubleClick)
            layout.addWidget(self.listWidget)

        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(QIcon('res/edit.ico'))
        bb.button(BB.Cancel).setIcon(QIcon('res/Bird.ico'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)
        
        self.setLayout(layout)

    def validate(self):
        try:
            if self.edit.text().trimmed():
                self.accept()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.edit.text().strip():
                self.accept()
    def listItemClick(self, tQListWidgetItem):
        try:
            text = tQListWidgetItem.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            text = tQListWidgetItem.text().strip()
        self.edit.setText(text)

    def listItemDoubleClick(self, tQListWidgetItem):
        self.listItemClick(tQListWidgetItem)
        self.validate()
    def popUp(self, text='', move=True):
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        if move:
            self.move(QCursor.pos())
        return self.edit.text() if self.exec_() else None

class AllGreen(QMainWindow):
     FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = list(range(3))
     def __init__(self):
         QWidget.__init__(self)
         self.setFixedSize(800, 700)

         self.dirty = False
         self.filePath = ""
         self.labelDialog = LabelDialog(listItem=["Add Rect","OCR","Barcode"])


         layout = QVBoxLayout(self)

         # ==============================
         self.canvas = Canvas(self)
         self.canvas.setFixedSize(640, 480)

         
         self.zoomWidget = ZoomWidget()
         self.scalers = {
            self.FIT_WINDOW: self.scaleFitWindow,
            self.FIT_WIDTH: self.scaleFitWidth,
            # Set to one to scale to 100% when loading files.
            self.MANUAL_ZOOM: lambda: 1,
        }

         scroll = QScrollArea()
         scroll.setWidget(self.canvas)
         scroll.setWidgetResizable(True)
         self.scrollArea = scroll
         self.canvas.scrollRequest.connect(self.scrollRequest)

         self.canvas.newShape.connect(self.newShape)
         self.canvas.shapeMoved.connect(self.setDirty)
         # self.canvas.selectionChanged.connect(self.shapeSelectionChanged)
         # self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)

         self.setCentralWidget(scroll)

         self.labelCoordinates = QLabel('')
         self.statusBar().addPermanentWidget(self.labelCoordinates)

  
         

         qImage = QImage("res/image.jpg")
         self.canvas.loadPixmap(QPixmap.fromImage(qImage))
        
         self.canvas.setEnabled(True)
         self.adjustScale(initial=True)
         self.paintCanvas()
         self.canvas.setFocus(True)

         self.setCreateMode()

         layout.addWidget(self.canvas)

         button = QPushButton('Create Rect', self)
         button.move(10,500)
         button.clicked.connect(self.createRect)
         layout.addWidget(button)

         button = QPushButton('Save', self)
         button.setToolTip('Save Setting')
         button.move(120,500)
         button.clicked.connect(self.save)

         layout.addWidget(button)
         self.setLayout(layout)
         # ==============================

         palette = self.palette()
         role = self.backgroundRole()
         palette.setColor(role, QColor('black'))
         self.setPalette(palette)

         palette = self.canvas.palette()
         role = self.canvas.backgroundRole()
         palette.setColor(role, QColor(232, 232, 232, 255))
         self.canvas.setPalette(palette)


     # def toggleDrawingSensitive(self, drawing=True):
     #    """In the middle of drawing, toggling between modes should be disabled."""
     #    # self.actions.editMode.setEnabled(not drawing)
     #    if not drawing and self.beginner():
     #        # Cancel creation.
     #        print('Cancel creation.')
     #        self.canvas.setEditing(True)
     #        self.canvas.restoreCursor()
     #        self.actions.create.setEnabled(True)
     def createRect(self):
     	self.canvas.setEditing(False)
     def save(self):
     	[print(shape.points) for shape in self.canvas.shapes]
     def setDirty(self):
        self.dirty = True
        # self.actions.save.setEnabled(True)
     def newShape(self):
        #Pop-up and give focus to the label editor.             
        text = self.labelDialog.popUp()
        if text :
        	self.canvas.setEditing(True)
        	
        else:
        	self.canvas.resetAllLines() # redraw rect
        pass
     def scrollRequest(self, delta, orientation):
        units = - delta / (8 * 15)
        bar = self.scrollBars[orientation]
        bar.setValue(bar.value() + bar.singleStep() * units)
     def setCreateMode(self):
     	 self.canvas.setEditing(False)
         # self.actions.createMode.setEnabled(edit)
         # self.actions.editMode.setEnabled(not edit)
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


def main():
     import sys
     a = QApplication(sys.argv)
     # QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))

     w = AllGreen()
     # w.canvas.setAutoFillBackground(True)
     # w.w2.setAutoFillBackground(True)
     # w.w3.setAutoFillBackground(True)
     w.show()

     a.exec_()

if __name__ == "__main__":
     main()