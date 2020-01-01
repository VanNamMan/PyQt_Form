from utils import *
from bbox import BoxTeaching,BoxFontColor,BoxProcessLog
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
        model_fodler        = self.config["model"]["folder"]
        file_function       = self.config["function"]["file"]

        self.lbPos          = QLabel("",self)
        self.lbRect         = QLabel("",self)
        self.lbTimeInfer    = QLabel("",self)

        self.statusBar().addPermanentWidget(self.lbTimeInfer)
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
        self.boxTeaching.listShapeCliked.connect(self.listShapeCliked)

        self.dock = QDockWidget('boxTeaching', self)
        self.dock.setWidget(self.boxTeaching)
        self.dock.setFeatures(dockFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.dock.hide()
        
        self.auto               = QWidget()
        self.boxProcessLog      = BoxProcessLog(self)
        self.frame              = QLabel()
        gridlayout              = QGridLayout()
        self.auto.setLayout(gridlayout)

        self.manual = QWidget()
        self.data   = QWidget()

        self.canvas = Canvas(self)
        self.canvas.mouseMoveSignal.connect(self.mouseMove)
        self.canvas.testActionSignal.connect(self.predict)
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
    def predict(self,shape,teaching=True):
        if shape is None:
            return
        index   = self.canvas.shapes.index(shape)
        for i in range(len(self.canvas.shapes)):
            self.canvas.shapes[i].result["pixmap"]  = None
            self.canvas.shapes[i].result["text"]    = None
        if teaching:
            config  = self.boxTeaching.getConfig()
        else:
            config  = shape.config

        # t0 = time.time()
        resutls,visualizes  = test_process(self.canvas.mat
                        ,config
                        ,draw_match=True
                        ,draw_box=True
                        ,fs=self.fs
                        ,lw=self.lw
                        ,color=self.color)
        # time_infer = time.time()-t0
        # print("%s time : %d ms"%(shape.label,time_infer*1000))

        x,y,w,h                                    = str2ListInt(config["crop"]["QRect"])
        pixmap                                     = ndarray2pixmap(visualizes[-1])
        self.canvas.shapes[index].result["pixmap"] = pixmap.scaled(w,h)
        #     # QMessageBox.information(self,"Dst",dst.text)
        #     self.canvas.shapes[index].result["text"]   = dst.text

    def autoPredict(self):
        for i in range(len(self.canvas.shapes)):
            runThread(self.loopAutoPredict,args=(i,))

    def loopAutoPredict(self,iShape):
        self.showMessage("Auto test starting")
        timeout         = float(self.boxTeaching.ln_timeout.text())/1000
        n               = self.boxTeaching.cbb_shape.count()

        while True:
            index       = self.boxTeaching.cbb_shape.currentIndex()
            state       = self.boxTeaching.autotest.checkState()
            if index == -1:
                pass
            else:
                bTeaching = iShape == index
                self.predict(self.canvas.shapes[iShape],bTeaching)
            
            time.sleep(timeout)
            if not state:
                break

        self.showMessage("Auto test stopped")

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
            cfg[lb]              = config
        with open(cfg_file,"w") as ff:
            cfg.write(ff)
        self.statusBar().showMessage("%s saved"%model,5000)

    def listShapeCliked(self,row):
        for i in range(len(self.canvas.shapes)):
            self.canvas.shapes[i].selected = row == i
            self.canvas.shapeSelected      = self.canvas.shapes[row]
        pass
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
            fw,fh                 = eval(cfg["frame"])["Width"],eval(cfg["frame"])["Height"]
            width,height          = self.canvas.width_,self.canvas.height_
            sw,sh                 = width/fw,height/fh
            x_,y_,w_,h_           = int(x*sw),int(y*sh),int(w*sw),int(h*sh)                        
            shape                 = Shape(QRect(x_,y_,w_,h_),lb,parent=self.canvas)
            for section in cfg.keys():
                dict_                   = eval(cfg[section])
                dict_["QRect"]  = "%d,%d,%d,%d"%(x_,y_,w_,h_)  
                shape.config[section]   = dict_
            
            shape.scaled_()
            
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
    
    def showMessage(self,stt):
        self.statusBar().showMessage(stt)

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
            self.color          = a["cvColor"]
            self.lw             = a["lw"]
            self.fs             = a["fs"]/10
            self.canvas.fs      = a["fs"]
            self.canvas.color   = a["color"]
        pass
    def editing(self):
        self.canvas.edit = True
        self.statusBar().showMessage("Editing")
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.showMaximized()
    sys.exit(app.exec_())


