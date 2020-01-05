from utils import *
from bbox import *
from canvas import Canvas,Shape
from vision import *

import resources

print("System : ",os.name)

class Proc(object):
    def __init__(self,config):
        # 
        self.busy = False
        self.config = config
        #  result
        self.box  = []
        self.visualize = []
    
    def isDone(self):
        return not self.busy

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
        dockFeatures            = QDockWidget.DockWidgetClosable|QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable
        self.boxTeaching        = BoxTeaching(model_fodler
                                            ,file_function
                                            ,self)

        self.boxTeaching.boxModel.cbb_model.activated.connect(self.chooseModel)

        self.dock_teach = QDockWidget('boxTeaching', self)
        self.dock_teach.setWidget(self.boxTeaching)
        self.dock_teach.setFeatures(dockFeatures)
        
        self.boxProcess  = BoxProcessResult(self)
        self.dock_proc = QDockWidget('Result', self)
        self.dock_proc.setWidget(self.boxProcess)
        self.dock_proc.setFeatures(dockFeatures)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_proc)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_teach)
        
        toggleParaDock = self.dock_teach.toggleViewAction()
        toggleLogDock  = self.dock_proc.toggleViewAction()
        
        self.camera               = BoxCamera(0,0.005,self)
        #  connect mat from camera to image process
        self.camera.signal.connect(self.run_process)
        # self.boxProcessLog      = BoxProcessLog(self)
        self.frame              = QLabel()

        self.manual = QWidget()
        self.data   = QWidget()

        self.canvas = Canvas(self)
        self.canvas.mouseMoveSignal.connect(self.mouseMove)
        self.canvas.testActionSignal.connect(self.predict_teaching)
        self.canvas.cropActionSignal.connect(self.cropImage)

        self.stacker = QStackedWidget(self)
        addWidgets(self.stacker,[self.camera,self.manual,self.canvas,self.data])

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
        open_     = action("Open",self.openFile,"ctrl+o","open",None,False)
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
        addActions(view,[auto,manual,teach,data,toggleLogDock,toggleParaDock])
        addActions(edit,[font,editing,self.canvas.actions.test
                ,self.canvas.actions.testAll,self.canvas.actions.delete])

        # init variable , loop camera
        self.OnInit() 
        # self.box_process = []
        # self.visualize_process = []
        #

    def OnInit(self):
        self.processes = [] # control process for each shape
    #     self.resetBoxAndVisual() # reset all shape result
    #     pass 
    # def resetBoxAndVisual(self):
    #     self.box_process = []
    #     self.visualize_process = []
        

    def run_process(self,mat):
        if mat is None:
            return 
        #  reset box before run image process
        # self.resetBoxAndVisual()
        self.camera.visualize = {"boxs":None,"visualizes":None}
        config = self.currentModelConfig
        # self.bProc = []

        def shapeProc(i,proc):
            print("\n%s : Shape-%d process is starting."%(getStrTime(),i))
            proc.busy = True
            results,vis  = self.predict(proc.config,mat,pprint=True)
            proc.box = results[0].roi
            proc.visualize = (vis[-1])
            proc.busy = False
            print("\n%s : Shape-%d process is done."%(getStrTime(),i))
            # self.camera.visualize = {"boxs":self.box_process,"visualizes":self.visualize_process}
            pass
        # 
        # if config is None:
        #     return
        for i,proc in enumerate(self.processes):
            if proc.isDone():
                runThread(shapeProc,args=(i,proc))
                pass

        #         runThread(shapeProc,args=(config,))
    
                # results,vis  = self.predict(config,mat,False)
                # if results:
                #     boxs.append(results[0].roi)
                #     visualizes.append(vis[-1])
            
        pass
    def apply(self):
        if self.canvas.shapeSelected is None:
            return
        shape                               = self.canvas.shapeSelected
        index                               = self.canvas.shapes.index(shape)
        self.canvas.shapes[index].config    = self.boxTeaching.getConfig()
        self.canvas.shapeSelected.config    = self.boxTeaching.getConfig()
        pass
    def predict_teaching(self,shape):
        if shape is None:
            return
        config  = self.boxTeaching.getConfig()
        for i in range(len(self.canvas.shapes)):
            self.canvas.shapes[i].result["pixmap"]  = None
            self.canvas.shapes[i].result["text"]    = None

        resutls,visualizes  = test_process(self.canvas.mat,config,bTeaching=True)
        index                                      = self.canvas.shapes.index(shape)
        x,y,w,h                                    = str2ListInt(config["crop"]["QRect"])
        pixmap                                     = ndarray2pixmap(visualizes[-1])
        self.canvas.shapes[index].result["pixmap"] = pixmap.scaled(w,h)
        pass
    def predict(self,config=None,mat=None,pprint=True):
        if config is None or mat is None:
            return
        resutls,visualizes  = test_process(mat,config,bTeaching=False,pprint=pprint)
        return resutls,visualizes

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
                self.predict(self.canvas.shapes[iShape],mat=self.canvas.mat,teaching=bTeaching)
            
            time.sleep(timeout)
            if not state:
                break

        self.showMessage("Auto test stopped")

    def saveAll(self):
        try:
            boxTeaching     = self.boxTeaching
            model           = boxTeaching.boxModel.model()
            folder          = boxTeaching.boxModel.folder
            cfg             = ConfigParser()
            cfg_file        = "%s/%s/para.config"%(folder,model)
            # cfg.read(cfg_file)
            cfg["model"]    = {"model":model}
            for shape in self.canvas.shapes:
                lb                   = shape.label
                config               = shape.config
                cfg[lb]              = config
            with open(cfg_file,"w") as ff:
                cfg.write(ff)
            self.statusBar().showMessage("%s saved"%model,5000)
        except:
            self.statusBar().showMessage("save %s has a problem"%model,5000)

    def chooseModel(self):
        model                     = self.boxTeaching.boxModel.model()
        folder                    = self.boxTeaching.model_folder
        if model == "None" or "":
            self.currentModelConfig = None
            return
        path                      = "%s/%s/para.config"%(folder,model)
        config                    = ConfigParser()
        config.read(path)
        self.currentModelConfig   = config
        for i,section in enumerate(self.currentModelConfig.sections()):
            if "shape" in section:
                # bProc[section]      = False
                shapeConfig       = configProxy2dict(self.currentModelConfig[section])
                self.processes.append(Proc(shapeConfig))

        if self.stacker.currentWidget() != self.canvas:
            return
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
            self.stacker.setCurrentWidget(self.camera)
            # self.dock.hide()
            # self.dock_Log.show()
        elif self.sender() == self.actions.manual:
            self.stacker.setCurrentWidget(self.manual)
            # self.dock.hide()
            # self.dock_Log.hide()
        elif self.sender() == self.actions.teach:
            self.stacker.setCurrentWidget(self.canvas)
            self.actions.open_.setEnabled(True)
            # self.dock.show()
            # self.dock_Log.hide()
        elif self.sender() == self.actions.data:
            self.stacker.setCurrentWidget(self.data)
            # self.dock.hide()
            # self.dock_Log.hide()
        pass
    
    def editFont(self):
        a = self.boxFontAndColor.popUp()
        if a :
            cvFont.color        = a["cvColor"]
            cvFont.lw           = a["lw"]
            cvFont.fs           = a["fs"]/10
            self.canvas.fs      = a["fs"]
            self.canvas.color   = a["color"]
        pass
    def editing(self):
        self.canvas.edit = True
        self.statusBar().showMessage("Editing")
        pass

    def closeEvent(self,ev):
        self.camera.release()
        print("close")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.showMaximized()
    sys.exit(app.exec_())


