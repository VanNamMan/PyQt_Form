from utils import *
from bbox import *
from canvas import Canvas,Shape
from vision import *

import resources

print("System : ",os.name)

class Result(object):
    def __init__(self):
        self.n_ok = 0
        self.n_ng = 0
        self.n_total = 0
        self.res = None
    
class Proc(object):
    def __init__(self,config):
        # 
        self.busy = False
        self.config = config
        #  result
        self.time_inference = 0 # ms
        self.box  = []
        self.visualize = []
        self.res = None
    def isDone(self):
        return not self.busy

class MainWindow(QMainWindow):
    resultSignal = pyqtSignal(Result) # (ok,ng,total) , result
    shapeStatus  = pyqtSignal(int,bool,str,str,int) # idshape,status,start_time,stop_time,inference_time
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

        self.boxDecision        = BoxDecision(self)

        self.boxFontAndColor    = BoxFontColor()
        self.color              = (0,255,0)
        self.fs                 = 1
        self.lw                 = 2
        dockFeatures            = QDockWidget.DockWidgetClosable|QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable
        self.boxTeaching        = BoxTeaching(model_fodler
                                            ,file_function
                                            ,self)

        self.boxTeaching.boxModel.cbb_model.activated.connect(self.chooseModel)

        self.dock_teach = QDockWidget('BoxTeaching', self)
        self.dock_teach.setWidget(self.boxTeaching)
        self.dock_teach.setFeatures(dockFeatures)
        
        self.boxProcess  = BoxProcessResult(self)
        self.dock_proc = QDockWidget('Result', self)
        self.dock_proc.setWidget(self.boxProcess)
        self.dock_proc.setFeatures(dockFeatures)

        self.boxImageResult  = BoxImageResult(self)
        self.dock_imageResult = QDockWidget('ImageResult', self)
        self.dock_imageResult.setWidget(self.boxImageResult)
        self.dock_imageResult.setFeatures(dockFeatures)
        self.dock_imageResult.hide()

        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_proc)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_imageResult)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_teach)
        
        toggleParaDock                  = self.dock_teach.toggleViewAction()
        toggleLogImageResultDock        = self.dock_imageResult.toggleViewAction()
        toggleLogDock                   = self.dock_proc.toggleViewAction()

        toggleParaDock.setShortcut("ctrl+shift+t")
        toggleLogImageResultDock.setShortcut("ctrl+shift+i")
        toggleLogDock.setShortcut("ctrl+shift+r")
        
        timeout = float(self.config["camera"]["timeout"])
        self.camera               = BoxCamera(timeout,button=False,parent=self)

        # connect to camera
        self.boxProcess.but_start.clicked.connect(self.camera.start)
        self.boxProcess.but_stop.clicked.connect(self.camera.stop)
        self.boxProcess.but_grab.clicked.connect(self.camera.capture)
        self.boxProcess.but_reset.clicked.connect(self.camera.reset)
        # 
        # self.frame              = QLabel()

        # stacker
        self.manual = QWidget()
        self.manual.setStyleSheet("background:blue")
        self.data   = QWidget()
        self.data.setStyleSheet("background:green")
        self.canvas = Canvas(self)
        self.stacker = QStackedWidget(self)
        addWidgets(self.stacker,[self.camera,self.manual,self.canvas,self.data])
        
        self.button_widget = BoxButtons(self)

        self.scroll = QScrollArea()
        center_layout = QVBoxLayout()
        addWidgets(center_layout,[self.stacker,self.button_widget])
        widget = QWidget()
        widget.setLayout(center_layout)
        self.scroll.setWidget(widget)
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
        addActions(view,[auto,manual,teach,data
                    ,toggleLogDock
                    ,toggleParaDock
                    ,toggleLogImageResultDock])
        addActions(edit,[font,editing,self.canvas.actions.test
                ,self.canvas.actions.delete,self.canvas.actions.decision])

        #  signal
        #  connect mat from camera to image process
        self.camera.signal.connect(self.run_process)
        # shape status signal
        self.shapeStatus.connect(self.showShapeStatus)
        self.resultSignal.connect(self.showProcessResult)
        # canvas signal
        self.canvas.mouseMoveSignal.connect(self.mouseMove)
        self.canvas.testActionSignal.connect(self.predict_teaching)
        self.canvas.cropActionSignal.connect(self.cropImage)

        # init variable , loop camera
        self.OnInit() 
        # self.box_process = []
        # self.visualize_process = []
        #

    def OnInit(self):
        self.processes = [] # control process for each shape
        self.result    = Result() #
        # defautl camera 
        self.camera.openCamera()
    def showShapeStatus(self,i,status,start,stop,inference_time):
        if status:
            status = "RUNNING"
            color = Qt.red
        else:
            status = "FREE"
            color = Qt.green
        self.boxImageResult.boxShapeStatus[i] = ["shape-%d"%i,"%d ms"%inference_time,status]
        pass

    def showProcessResult(self,result): # Result
        n_ok = result.n_ok
        n_ng = result.n_ng
        n_total = result.n_total
        nums = (n_ok,n_ng,n_total)
        self.boxProcess.showResult(nums,result.res)

    def doneProcess(self,processes):
        for proc in self.processes:
            if not proc.isDone() :
                self.result.res = None
                return False

        for proc in self.processes:
            if proc.res is None:
                self.result.res = None
                return True
        
        self.result.res = True
        for proc in self.processes:
            if not proc.res:
                self.result.res = False
                break
        if self.result.res :
            self.result.n_ok += 1
            self.result.n_ok = min(self.result.n_ok,1000000)
        else:
            self.result.n_ng += 1
            self.result.n_ng = min(self.result.n_ng,1000000)

        self.result.n_total = self.result.n_ok + self.result.n_ng

        return True

    def shapeProc(self,mat,i,proc):
        # update process status 
        self.processes[i].busy = True
        # start = getStrTime()
        self.shapeStatus.emit(i,True,"","",self.processes[i].time_inference)
        t0 = time.time()
        # image process
        results,vis,pred = self.predict(self.processes[i].config,mat,pprint=True)
        # show result 
        self.processes[i].box = results[0].roi
        self.processes[i].visualize = (vis[-1])
        self.processes[i].res = pred
        
        # update camera
        self.camera.visualize["boxs"][i] = self.processes[i].box
        self.camera.visualize["visualizes"][i] = self.processes[i].visualize
        # update process status
        # stop = getStrTime()
        self.processes[i].time_inference = int((time.time()-t0)*1000)
        self.processes[i].busy = False
        self.shapeStatus.emit(i,False,"","",self.processes[i].time_inference)
        pass
    def run_process(self,mat):
        if mat is None:
            return
        # 
        if self.doneProcess(self.processes):
            self.resultSignal.emit(self.result)
            for i,proc in enumerate(self.processes):
                # if not proc.isDone():continue
                runThread(self.shapeProc,args=(mat,i,proc))
        else:
            self.resultSignal.emit(self.result)
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

        resutls,visualizes,_  = test_process(self.canvas.mat,config,bTeaching=True)
        index                                      = self.canvas.shapes.index(shape)
        x,y,w,h                                    = str2ListInt(config["crop"]["QRect"])
        pixmap                                     = ndarray2pixmap(visualizes[-1])
        self.canvas.shapes[index].result["pixmap"] = pixmap.scaled(w,h)
        pass
    def predict(self,config=None,mat=None,pprint=True):
        if config is None or mat is None:
            return
        return test_process(mat,config,bTeaching=False,pprint=pprint)

    def saveAll(self):
        dialog = BoxPassword(self)
        pass_ = self.config["password"]["pass"]
        if not dialog.popUp() == pass_:
            return
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
        self.currentModelConfig   = None
        self.processes = []
        self.camera.visualize     = {"boxs":[],"visualizes":[]}
        if model == "None" or "":
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
                # self.boxImageResult.boxShapeStatus[i] = [section,"0 ms","FREE"]
                self.camera.visualize["boxs"].append(None)
                self.camera.visualize["visualizes"].append(None)

        
        if self.stacker.currentWidget() != self.canvas:
            return
        sections                  = list(config.sections())
        lb_shapes                 = [s for s in sections if "shape" in s]
        self.canvas.items         = []
        self.canvas.shapes        = []
        self.canvas.shapeSelected = None
        self.boxTeaching.listShape.clear()

        self.canvas.items = lb_shapes
        addItems(self.boxTeaching.listShape,self.canvas.items)

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
        elif self.sender() == self.actions.manual:
            self.stacker.setCurrentWidget(self.manual)
        elif self.sender() == self.actions.teach:
            self.stacker.setCurrentWidget(self.canvas)
            self.actions.open_.setEnabled(True)
        elif self.sender() == self.actions.data:
            self.stacker.setCurrentWidget(self.data)
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


