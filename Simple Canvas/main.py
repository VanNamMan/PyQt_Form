from utils import *
import resources

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("Automation 2G - Vision Master")
        self.setGeometry(QRect(0,0,640,480))

        self.lbCoor = QLabel("",self)
        self.statusBar().addPermanentWidget(self.lbCoor)
        
        self.auto   = QWidget()
        gridlayout  = QGridLayout()
        self.auto.setLayout(gridlayout)

        self.manual = QWidget()
        self.data   = QWidget()

        self.canvas = Canvas(self)
        self.canvas.mouseMoveSignal.connect(self.mouseMove)

        self.stacker = QStackedWidget(self)
        addWidgets(self.stacker,[self.auto,self.manual,self.canvas,self.data])

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.stacker)
        self.scroll.setWidgetResizable(True)

        self.setCentralWidget(self.scroll)

        # menu
        file = self.menuBar().addMenu("File")
        view = self.menuBar().addMenu("View")
        edit = self.menuBar().addMenu("Edit")

        self.menus = struct(
            file = file,
            view = view,
            edit = edit
        )

        action    = partial(newAction,self)
        open_     = action("Open",self.openFile,"ctrl+o","open",False)
        auto      = action("Home",self.switchWidget,"ctrl+a","home")
        teach     = action("Teaching",self.switchWidget,"ctrl+t","teach")
        data      = action("Data",self.switchWidget,"ctrl+d","data")
        manual    = action("Manual",self.switchWidget,"ctrl+m","manual")
        editing   = action("Edit",self.editing,"w","edit")

        self.actions = struct(
            open_    = open_,
            auto    = auto,
            manual  = manual,
            data    = data,
            teach   = teach,
            edit    = editing
        )

        addActions(file,[open_])
        addActions(view,[auto,manual,teach,data])
        addActions(edit,[editing,self.canvas.actions.test
                ,self.canvas.actions.testAll,self.canvas.actions.delete])

    def mouseMove(self,text):
        self.lbCoor.setText(text)
    def openFile(self):
        filename,_ = QFileDialog.getOpenFileName(self,"Select File",os.getcwd()
                ,"Image File (*jpg *png)")
        if filename:
            pixmap = QPixmap(filename)
            self.canvas.loadPixmap(pixmap)
            self.statusBar().showMessage(filename)
        pass
    def switchWidget(self):
        if self.sender() == self.actions.auto:
            self.stacker.setCurrentWidget(self.auto)
        elif self.sender() == self.actions.manual:
            self.stacker.setCurrentWidget(self.manual)
        elif self.sender() == self.actions.teach:
            self.stacker.setCurrentWidget(self.canvas)
            self.actions.open_.setEnabled(True)
        elif self.sender() == self.actions.data:
            self.stacker.setCurrentWidget(self.data)
        
        pass
    def editing(self):
        self.canvas.edit = True
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


