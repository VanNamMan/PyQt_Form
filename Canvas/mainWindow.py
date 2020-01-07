from libs.header import *
from libs.utils import *
from libs.canvas import Canvas

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("Automation 2G - Vision Master")
        self.setGeometry(QRect(0,0,400,400))
        menu = QMenuBar(self)
        action = partial(newAction,self)
        # 
        file = self.menuBar().addMenu("File")
        view = self.menuBar().addMenu("View")
        edit = self.menuBar().addMenu("Edit")
        #
        draw = action("Draw rect",self.setEditing,"w","draw","draw rectangle") 
        # 
        addActions(edit,[draw])
        # 
        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)
        self.canvas.cropSignal.connect(self.crop)
        self.canvas.newShape.connect(self.newShape)
    
    def crop(self,shape):
        # format_shape = self.canvas.formatShape(shape)
        # x,y,w,h = format_shape["cvRect"]
        # pixmap = self.canvas.pixmap
        # crop   = pixmap2ndarray(pixmap)[y:y+h,x:x+w]
        # cv2.imwrite("image/crop/mat.png",crop)
        pass
    
    def newShape(self,shape):
        print(self.canvas.formatShape(shape))
    
    def setEditing(self):
        self.canvas.setEditing()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    wd = MainWindow()
    wd.show()
    sys.exit(app.exec_())   