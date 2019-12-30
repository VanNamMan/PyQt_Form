from utils import *
from bbox import BoxTeaching,BoxFontColor
from canvas import Canvas,Shape
from vision import *
import resources

print("System : ",os.name)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("Automation 2G - Vision Master")
        self.setGeometry(QRect(0,0,640,480))
        self.currentModelConfig    = None
        self.config                = ConfigParser()
        self.config.read("main.config")
        model_fodler        = self.config["Model"]["folder"]
        file_function       = self.config["Function"]["file"]

        self.lbPos  = QLabel("",self)
        self.lbRect = QLabel("",self)
        self.statusBar().addPermanentWidget(self.lbRect)
        self.statusBar().addPermanentWidget(self.lbPos)

        self.boxFontAndColor    = BoxFontColor()
        self.color              = (0,255,0)
        self.fs                 = 1
        self.lw                 = 2
        dockFeatures            = QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable
        self.boxTeaching        = BoxTeaching(model_fodler
                                            ,file_function
                                            ,self)

        self.boxTeaching.boxModel.cbb_model.activated.connect(self.chooseModel)

        self.dock = QDockWidget('boxTeaching', self)
        self.dock.setWidget(self.boxTeaching)
        self.dock.setFeatures(dockFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.dock.hide()
        
        self.auto   = QWidget()
        gridlayout  = QGridLayout()
        self.auto.setLayout(gridlayout)

        self.manual = QWidget()
        self.data   = QWidget()

        self.canvas = Canvas(self)
        self.canvas.mouseMoveSignal.connect(self.mouseMove)
        self.canvas.testActionSignal.connect(self.test)
        self.canvas.cropActionSignal.connect(self.cropImage)

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
        font      = action("Font-Color",self.editFont,"ctrl+f","font")

        self.actions = struct(
            open_    = open_,
            auto    = auto,
            manual  = manual,
            data    = data,
            teach   = teach,
            edit    = editing,
            font    = font
        )

        addActions(file,[open_])
        addActions(view,[auto,manual,teach,data])
        addActions(edit,[font,editing,self.canvas.actions.test
                ,self.canvas.actions.testAll,self.canvas.actions.delete])

    def apply(self):
        shape                               = self.canvas.shapeSelected
        index                               = self.canvas.shapes.index(shape)
        self.canvas.shapes[index].config    = self.boxTeaching.getConfig()
        self.canvas.shapeSelected.config    = self.boxTeaching.getConfig()
        pass
    def saveAll(self):
        boxTeaching     = self.boxTeaching
        model           = boxTeaching.boxModel.model()
        folder          = boxTeaching.boxModel.folder
        cfg             = ConfigParser()
        cfg_file        = "%s/%s/para.config"%(folder,model)
        cfg.read(cfg_file)
        cfg["model"]    = {"model":model}
        for shape in self.canvas.shapes:
            lb                   = shape.label
            config               = shape.config
            cfg[lb]         = config
        with open(cfg_file,"w") as ff:
            cfg.write(ff)
        self.statusBar().showMessage("%s saved"%model,5000)

    def chooseModel(self):
        model                     = self.boxTeaching.boxModel.cbb_model.currentText()
        folder                    = self.boxTeaching.model_folder
        path                      = "%s/%s/para.config"%(folder,model)
        config                    = ConfigParser()
        config.read(path)
        self.currentModelConfig   = config
        sections                  = list(config.sections())
        lb_shapes                 = [s for s in sections if "shape" in s]
        self.canvas.items         = []
        self.canvas.shapes        = []
        self.canvas.shapeSelected = None
        self.boxTeaching.listShape.clear()

        for i,lb in enumerate(lb_shapes):
            cfg                   = config[lb]
            x,y,w,h               = str2ListInt(eval(cfg["crop"])["QRect"])
            shape                 = Shape(QRect(x,y,w,h),lb,parent=self.canvas)
            for section in cfg.keys():
                dict_                   = eval(cfg[section])
                shape.config[section]   = dict_
            
            self.canvas.shapes.append(shape)

        self.canvas.items = lb_shapes
        addItems(self.boxTeaching.listShape,self.canvas.items)
        return 

    def cropImage(self,shape):
        x,y,w,h = shape.cvRect
        cropped = self.canvas.mat[y:y+h,x:x+w]

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename,_ = QFileDialog.getSaveFileName(self,"Save as",os.getcwd(),"Image (*.png)",options=options)
        # filename = "demo/cropped.png"
        if filename:
            cv2.imwrite(filename,cropped)
            self.statusBar().showMessage("image saved at %s"%filename,5000)
        pass
    def test(self,shape):
        config  = self.boxTeaching.getConfig()
        dst     = test_process(self.canvas.mat
                        ,config
                        ,draw_match=True
                        ,draw_box=True
                        ,fs=self.fs
                        ,lw=self.lw
                        ,color=self.color)
        if isinstance(dst,np.ndarray):
            wd = cv2.namedWindow("",cv2.WINDOW_FREERATIO)
            cv2.imshow("",dst)
            cv2.waitKey(0)
        elif isinstance(dst,OCR):
            QMessageBox.information(self,"Dst",dst.text)

    def mouseMove(self,r,p):
        self.lbPos.setText(p)
        if r:
            self.lbRect.setText("[%s]"%r)
    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename,_ = QFileDialog.getOpenFileName(self,"Select File",os.getcwd()
                ,"Image File (*.jpg *.png *.bmp)",options=options)
        if filename:
            pixmap = QPixmap(filename)
            self.canvas.loadPixmap(pixmap)
            self.statusBar().showMessage(filename)
        pass
    def switchWidget(self):
        if self.sender() == self.actions.auto:
            self.stacker.setCurrentWidget(self.auto)
            self.dock.hide()
        elif self.sender() == self.actions.manual:
            self.stacker.setCurrentWidget(self.manual)
            self.dock.hide()
        elif self.sender() == self.actions.teach:
            self.stacker.setCurrentWidget(self.canvas)
            self.actions.open_.setEnabled(True)
            self.dock.show()
        elif self.sender() == self.actions.data:
            self.stacker.setCurrentWidget(self.data)
            self.dock.hide()
        pass
    
    def editFont(self):
        a = self.boxFontAndColor.popUp()
        if a :
            self.color  = a["cvColor"]
            self.lw     = a["lw"]
            self.fs     = a["fs"]
        pass
    def editing(self):
        self.canvas.edit = True
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


