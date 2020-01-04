from utils import*
import resources

BB = QDialogButtonBox
DEFAUT_COLOR = QColor(0,255,0,255)

class BoxCamera(QDialog):
    signal  = pyqtSignal(np.ndarray)
    fpsSignal     = pyqtSignal(float)
    def __init__(self,i,timeout,parent=None):
        super(BoxCamera,self).__init__(parent)
        self.setWindowTitle("Camera Dialog")
        self.cap        = cv2.VideoCapture(i)
        self.timeout    = timeout
        self.visualize  = {"boxs":None,"visualizes":None}

        layout          = QVBoxLayout()
        self.frame      = QLabel(self)
        self.frame.setAlignment(Qt.AlignCenter)

        hlayoutTop      = QHBoxLayout()
        self.cbb_camera = newCbb(["0","1","2"])
        self.lb_fps     = QLabel("",self)
        self.lb_fps.setMaximumHeight(50)
        widgets = [
            QLabel("Camera"),
            self.cbb_camera,
            self.lb_fps
        ]
        addWidgets(hlayoutTop,widgets)
        widgetTop = QWidget()
        widgetTop.setLayout(hlayoutTop)
        widgetTop.setMaximumHeight(50)
        widgetTop.setMaximumWidth(500)

        hlayout         = QHBoxLayout()
        self.but_start = newButton("Start",self.start,"start")
        self.but_stopt = newButton("Stop",self.stop,"stop")
        self.but_reset = newButton("Reset",self.reset,"reset")
        self.but_grab = newButton("Grab",self.capture,"grab")
        widgets = [
            self.but_start,
            self.but_stopt,
            self.but_grab,
            self.but_reset
        ]
        addWidgets(hlayout,widgets)
        widgets = [
            widgetTop,
            self.frame,
            hlayout
        ]
        addWidgets(layout,widgets)
        self.setLayout(layout)
        self.bStart = False
        self.fps = 0
        self.fpsSignal.connect(self.setFPS)
    def setFPS(self,fps):
        self.lb_fps.setText("FPS : %.2f"%fps)
    def isOpened(self):
        return self.cap.isOpened()
    def capture(self):
        mkdir("grab")
        mat = self.grab()
        if mat is not None:
            filename        = "grab/%s.png"%getStrDateTime()
            if cv2.imwrite(filename,mat):
                print("image saved at %s"%filename)
    def grab(self):
        ret,mat = self.cap.read()
        if ret:
            return mat
        else:
            return None
    def start(self):
        self.bStart     = True
        runThread(self.loop,args=())
        pass
    def stop(self):
        self.bStart = False
        pass
    def reset(self):
        pass
    def release(self):
        self.bStart  = False
        time.sleep(0.01)
        self.cap.release()
    def loop(self):
        print("loop camera started")
        fps = 0
        t0 = time.time()
        while self.bStart and self.isOpened():
            mat = self.grab()
            if mat is not None:
                boxs         = self.visualize["boxs"]
                visualizes   = self.visualize["visualizes"]
                if visualizes is not None:
                    copy = mat.copy()
                    for box,vis in zip(boxs,visualizes):
                        x,y,w,h = box
                        copy[y:y+h,x:x+w] = vis
                    showImage(copy,self.frame)
                else:
                    showImage(mat,self.frame)

                # emit to run process
                self.signal.emit(self.grab())

                #  emit FPS
                fps+=1
                if(time.time() - t0) >= 1.0:
                    self.fps = fps
                    self.fpsSignal.emit(self.fps)
                    fps = 0
                    t0 = time.time()

            time.sleep(self.timeout)
        pass
    
    def __del__(self):
        self.release()
    def closeEvent(self):
        self.release()
        pass

class ColorDialog(QColorDialog):

    def __init__(self, parent=None):
        super(ColorDialog, self).__init__(parent)
        self.setOption(QColorDialog.ShowAlphaChannel)
        # The Mac native dialog does not support our restore button.
        self.setOption(QColorDialog.DontUseNativeDialog)
        # Add a restore defaults button.
        # The default is set at invocation time, so that it
        # works across dialogs for different elements.
        self.default = QColor(0,170,0,255)
        self.setCurrentColor(self.default)
        self.bb = self.layout().itemAt(1).widget()
        self.bb.addButton(BB.RestoreDefaults)
        self.bb.clicked.connect(self.checkRestore)

    def getColor(self, value=None, title=None, default=None):
        self.default = default
        if title:
            self.setWindowTitle(title)
        if value:
            self.setCurrentColor(value)
        return self.currentColor() if self.exec_() else self.default

    def checkRestore(self, button):
        if self.bb.buttonRole(button) & BB.ResetRole and self.default:
            self.setCurrentColor(self.default)

class BoxFontColor(QDialog):
    def __init__(self,parent=None):
        super(BoxFontColor,self).__init__(parent)
        self.colorDialog     = ColorDialog(self)
        self.color           = DEFAUT_COLOR
        self.but_color       = newButton("Color",self.getColor)
        self.spin_lw         = QSpinBox(self)
        self.spin_fs         = QSpinBox(self)
        self.spin_lw.setRange(1,10)
        self.spin_fs.setRange(1,1000)

        lb_color             = QLabel("Color")
        lb_lw                = QLabel("LineWidth")
        lb_fs                = QLabel("FontScale")

        bb = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        bb.rejected.connect(self.reject)
        bb.accepted.connect(self.accept)

        layout = QGridLayout()
        layout.addWidget(lb_color,0,0)
        layout.addWidget(lb_lw,1,0)
        layout.addWidget(lb_fs,2,0)

        layout.addWidget(self.but_color,0,1)
        layout.addWidget(self.spin_lw,1,1)
        layout.addWidget(self.spin_fs,2,1)
        layout.addWidget(bb,3,1)

        self.setLayout(layout)
    def popUp(self):
        self.move(QCursor.pos())
        return self.getFontAndColor() if self.exec_() else None
    
    def getColor(self):
        self.color = self.colorDialog.getColor(title='Choose color',default=DEFAUT_COLOR)
    def getFontAndColor(self):
        return {"color"     : self.color,
                "cvColor"   : self.color.getRgb()[:3][::-1],
                "lw"        : self.spin_lw.value(),
                "fs"        : self.spin_fs.value()}

class Items(object):
    def __init__(self,parent):
        super(Items,self).__init__()
        self.parent           = parent
        spin                  = QSpinBox(parent)
        spin2                 = QSpinBox(parent)
        self.crop             = QLineEdit("0,0,0,0",parent)
        self.qrect            = QLineEdit("0,0,0,0",parent)
        self.convert          = newCbb(["bgr2gray","gray2bgr","hsv"])
        self.binary_threshold = spin
        self.binary_type      = newCbb(["normal","inv"])
        self.binary_method    = newCbb(["normal","otsu","adaptive"])
        self.binary_blocksize = QLineEdit("11",parent)
        self.blur_size        = QLineEdit("3",parent)
        self.blur_method      = newCbb(["blur","median","gauss"])
        self.morph_size       = QLineEdit("3",parent)
        self.morph_iter       = QLineEdit("1",parent)
        self.morph_method     = newCbb(["dilate","erode","close","open"
                                        ,"gradient","top hat","black hat"])
        self.cnts_mode      = newCbb(["external","list"])
        self.cnts_method        = newCbb(["none","simple"])

        self.remove_width     = QLineEdit("-1,-1",parent)
        self.remove_height    = QLineEdit("-1,-1",parent)
        self.remove_area      = QLineEdit("-1,-1",parent)
        self.orc_oem          = newCbb(["%d"%i for i in range(4)])
        self.orc_psm          = newCbb(["%d"%i for i in range(14)])
        self.orc_lang         = newCbb(["eng","vie","kor"])
        self.match_score      = spin2
        self.match_filename   = QLineEdit("",parent)
        self.match_multi      = QCheckBox("",parent)
        # self.match_filename   = QCommandLinkButton("...",parent)
        # self.match_filename.clicked.connect(self.brower)
        self.camera_type      = newCbb(["webcam","basler"])
        self.camera_id        = QLineEdit("...",parent)

        spin.setRange(0,255)
        spin.setValue(100)
        spin2.setRange(0,100)
        spin2.setValue(90)
    
    def setConfig(self,config):
        try:
            cfg             = config
            # camera          = eval(cfg["camera"])
            camera          = cfg["camera"]
            self.camera_type.setCurrentText(camera["Type"])
            self.camera_id.setText(camera["SN"])
            crop            = cfg["crop"]
            self.crop.setText(crop["Box"])
            self.qrect.setText(crop["QRect"])
            cvt             = cfg["convert"]
            self.convert.setCurrentText(cvt["Type"])
            binary          = cfg["binary"]
            self.binary_threshold.setValue(int(binary["Threshold"]))
            self.binary_method.setCurrentText(binary["Method"])
            self.binary_type.setCurrentText(binary["Type"])
            self.binary_blocksize.setText(binary["BlockSize"])
            blur            = cfg["blur"]
            self.blur_size.setText(blur["Size"])
            self.blur_method.setCurrentText(blur["Method"])
            morph           = cfg["morph"]
            self.morph_size.setText(morph["Size"])
            self.morph_iter.setText(morph["Iter"])
            self.morph_method.setCurrentText(morph["Method"])
            cnt             = cfg["contours"]
            self.cnts_mode.setCurrentText(cnt["Mode"])
            self.cnts_method.setCurrentText(cnt["Method"])
            remove          = cfg["remove"]
            self.remove_width.setText(remove["Width"])
            self.remove_height.setText(remove["Height"])
            self.remove_area.setText(remove["Area"])
            ocr             = cfg["ocr"]
            self.orc_lang.setCurrentText(ocr["Lang"])
            self.orc_oem.setCurrentText(ocr["Oem"])
            self.orc_psm.setCurrentText(ocr["Psm"])
            match           = cfg["matching"]
            self.match_score.setValue(int(match["Score"]))
            self.match_filename.setText(match["File"])
            self.match_multi.setChecked(eval(match["Multiple"]))
        except:
            print("has a problem when set items config")
            pass
    def brower(self):
        filename,_ = QFileDialog.getOpenFileName(self.parent,"Select File",os.getcwd()
                ,"Image File (*jpg *png)")
        if filename:
            self.match_filename.setText(filename)

# class Frame(QLabel):
#     def __init__(self,parent=None):
#         super(Frame,self).__init__(parent)
#         self.setAlignment(Qt.AlignCenter)

#     def show(self,mat):
#         pixmap  = ndarray2pixmap(mat)
#         self.setPixmap(pixmap)
#         pass
class BoxProcessLog(QDialog):
    def __init__(self,parent=None):
        super(BoxProcessLog,self).__init__(parent)
        self.list           = QListWidget(self)

        grid                = QGridLayout()
        self.lb_numOK       = QLabel("OK",self)
        self.lb_numNG       = QLabel("NG",self)
        self.lb_numTotal    = QLabel("Total",self)
        self.numOK          = QLabel("0",self)
        self.numNG          = QLabel("0",self)
        self.numTotal       = QLabel("0",self)
        grid.addWidget(self.lb_numOK,0,0)
        grid.addWidget(self.numOK,0,1)
        grid.addWidget(self.lb_numNG,1,0)
        grid.addWidget(self.numNG,1,1)
        grid.addWidget(self.lb_numTotal,2,0)
        grid.addWidget(self.numTotal,2,1)

        style = "color:green;font:bold 24px"
        self.lb_numOK.setStyleSheet(style)
        self.numOK.setStyleSheet(style)
        style = "color:red;font:bold 24px"
        self.lb_numNG.setStyleSheet(style)
        self.numNG.setStyleSheet(style)
        style = "color:black;font:bold 24px"
        self.lb_numTotal.setStyleSheet(style)
        self.numTotal.setStyleSheet(style)


        self.lb_result      = QLabel("Wait",self)
        self.lb_result.setAlignment(Qt.AlignCenter)
        self.lb_result.setMinimumHeight(300)
        style = "color:black;font:bold 72px;border-width:3px;border-color:black;border-style: outset"
        self.lb_result.setStyleSheet(style)

        self.but_clear      = newButton("Clear",self.clear,"clear")
        
        widget = [
            grid,
            self.lb_result,
            self.list,
            self.but_clear
        ]
        layout = QVBoxLayout()
        addWidgets(layout,widget)

        self.setLayout(layout)
        self.showResult([8,9,17],None)
    
    def clear(self):
        self.list.clear()
    def log(self,text):
        self.list.addItem("%s : %s"%(getStrTime,text))
    
    def showResult(self,nums,res=None):
        style = "color:black;font:bold 72px;border-width:3px;background:%s \
        ;border-color:black;border-style: outset"
        ok , ng ,total = nums
        self.numOK.setText("%d"%ok)
        self.numNG.setText("%d"%ng)
        self.numTotal.setText("%d"%total)
        if res is None:
            self.lb_result.setText("Wait")
            self.lb_result.setStyleSheet(style%"yellow")
        else:
            if res :
                self.lb_result.setText("OK")
                self.lb_result.setStyleSheet(style%"green")
            else:
                self.lb_result.setText("NG")
                self.lb_result.setStyleSheet(style%"red")

class BoxParameter(QTreeWidget):
    def __init__(self,parent=None):
        super(BoxParameter,self).__init__(parent)
        _translate = QCoreApplication.translate
        self.headerItem().setText(0, _translate("", "Parameter"))
        self.headerItem().setText(1, _translate("", "Value"))
        lbs = "Camera Crop Convert Binary Blur Morph Contours Remove OCR Matching".split()
        child = [
            "Type SN",
            "Box Qrect",
            "Type",
            "Threshold Method Type BlockSize",
            "Method Size",
            "Method Size Iter",
            "Mode Method",
            "Width Height Area",
            "Lang Oem Psm",
            "Score File Multiple",
        ]
        self.lb_item  = lbs
        self.lb_child = child
        for i,lb,ch in zip(range(len(lbs)),lbs,child):
            item   = QTreeWidgetItem([lb])
            chs    = ch.split()
            self.addTopLevelItem(item)
            for x in chs:
                self.topLevelItem(i).addChild(QTreeWidgetItem([x]))
            
        self.items = Items(self)
        addWidget = self.addWidget

        addWidget(0,0,self.items.camera_type)
        addWidget(0,1,self.items.camera_id)

        addWidget(1,0,self.items.crop)
        addWidget(1,1,self.items.qrect)

        addWidget(2,0,self.items.convert)

        addWidget(3,0,self.items.binary_threshold)
        addWidget(3,1,self.items.binary_method)
        addWidget(3,2,self.items.binary_type)
        addWidget(3,3,self.items.binary_blocksize)

        addWidget(4,0,self.items.blur_method)
        addWidget(4,1,self.items.blur_size)

        addWidget(5,0,self.items.morph_method)
        addWidget(5,1,self.items.morph_size)
        addWidget(5,2,self.items.morph_iter)

        addWidget(6,0,self.items.cnts_mode)
        addWidget(6,1,self.items.cnts_method)

        addWidget(7,0,self.items.remove_width)
        addWidget(7,1,self.items.remove_height)
        addWidget(7,2,self.items.remove_area)

        addWidget(8,0,self.items.orc_lang)
        addWidget(8,1,self.items.orc_oem)
        addWidget(8,2,self.items.orc_psm)

        addWidget(9,0,self.items.match_score)
        addWidget(9,1,self.items.match_filename)
        addWidget(9,2,self.items.match_multi)

    def addWidget(self,idIt,idChild,widget):
        if idChild is not None:
            it = self.topLevelItem(idIt).child(idChild)
            self.setItemWidget(it, 1, widget)
        else:
            it = self.topLevelItem(idIt)
            self.setItemWidget(it, 1, widget)
    

class BoxModel(QDialog):
    def __init__(self,folder):
        super(BoxModel,self).__init__()
        self.folder = folder
        mkdir(folder)
        layout              = QGridLayout()
        lb1                 = QLabel("Model",self)
        but_new             = newButton("",self.addNew,"add")
        self.cbb_model      = newCbb([])
        self.ln_model       = QLineEdit("",self)
        layout.addWidget(lb1,0,0)
        layout.addWidget(self.cbb_model,0,1)
        layout.addWidget(but_new,1,0)
        layout.addWidget(self.ln_model,1,1)
        self.setLayout(layout)
        self.load(folder)

    def addNew(self):
        allItems    = [self.cbb_model.itemText(i) for i in range(self.cbb_model.count())]
        new         = self.ln_model.text()
        if new :
            msg = QMessageBox.question(self,"Add Model","Do you want to add new model?")
            if msg == QMessageBox.Yes:
                allItems.append(new)
                self.cbb_model.clear()
                self.ln_model.clear()
                addItems(self.cbb_model,allItems)
                self.cbb_model.setCurrentIndex(len(allItems)-1)
                mkdir('%s/%s'%(self.folder,new))
                cfg             = ConfigParser()
                cfg["model"]    = {"model" : new}
                with open("Model/%s/para.config"%new,"w") as ff:
                    cfg.write(ff)
    def model(self):
        return self.cbb_model.currentText()
    
    def load(self,folder):
        models = os.listdir(folder)
        addItems(self.cbb_model,models)
        self.cbb_model.setCurrentIndex(-1)

class BoxFunction(QListWidget,QDialog):
    itemClickedSignal   = pyqtSignal(QListWidgetItem)
    def __init__(self,items,parent=None):
        super(BoxFunction,self).__init__(parent)
        if items:
            addItems(self,items)
            for i in range(len(items)):
                item = self.item(i)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(not Qt.Checked)

        self.itemClicked.connect(self.itemClicked_)
    
    def itemClicked_(self,item):
        self.itemClickedSignal.emit(item)

class BoxSelectedFunction(QDialog):
    itemRightClickedSignal   = pyqtSignal(QListWidgetItem)
    def __init__(self,items=[],parent=None):
        super(BoxSelectedFunction,self).__init__(parent)
        self.list = QListWidget(self)
        addItems(self.list,items)
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.popUpMenuFunc)
        hlayout         = QHBoxLayout()
        bb              = newDialogButton(["","","",""],
                                          [self.prevFunc,self.nextFunc,self.deleteFunc,self.deleteAll],
                                          ["up","down","delete","delete_all"])
        bb.setMaximumWidth(50)
        addWidgets(hlayout,[bb,self.list])
        self.setLayout(hlayout)
        # 
        action             = partial(newAction,self)
        deleteAll          = action("Delete All",self.deleteAll,"","delete_all")
        deleteFunc         = action("Delete",self.deleteFunc,"","delete",True)
        prevFunc           = action("Up",self.prevFunc,"","up",True)
        nextFunc           = action("Down",self.nextFunc,"","down",True)
        cancel             = action("Cancel",None,"","cancel",True)

        self.actions       = struct(
            deleteAll   = deleteAll,
            deleteFunc  = deleteFunc,
            prevFunc    = prevFunc,
            nextFunc    = nextFunc
        )
        self.funcMenu   = QMenu()
        addActions(self.funcMenu,[cancel,prevFunc,nextFunc,deleteFunc,deleteAll])

    def popUpMenuFunc(self):
        if self.list.count() > 0:
            self.funcMenu.exec_(QCursor.pos())
        pass
    
    def prevFunc(self):
        _list = self.list
        n = _list.count()
        items = _list.selectedItems()
        if items :
            row     = _list.row(items[0])
            if row > 0:
                txt1    = _list.item(row).text()
                txt2    = _list.item(row-1).text()
                _list.item(row).setText(txt2)
                _list.item(row-1).setText(txt1)
                _list.item(row).setSelected(False)
                _list.item(row-1).setSelected(True)
        pass
    def nextFunc(self):
        _list = self.list
        n = _list.count()
        items = _list.selectedItems()
        if items :
            row     = _list.row(items[0])
            if row < n-1:
                txt1    = _list.item(row).text()
                txt2    = _list.item(row+1).text()
                _list.item(row).setText(txt2)
                _list.item(row+1).setText(txt1)
                _list.item(row).setSelected(False)
                _list.item(row+1).setSelected(True)
        pass
    def deleteAll(self):
        self.list.clear()
    def deleteFunc(self):
        items = self.list.selectedItems()
        if items :
            msg = QMessageBox.question(self,"Delete Item","Do you want to delete item?")
            if msg == QMessageBox.Yes:
                row = self.list.row(items[0])
                self.list.takeItem(row)
class BoxTeaching(QDialog):
    listShapeCliked     = pyqtSignal(int)
    def __init__(self,model_folder,defautl_function,parent=None):
        super(BoxTeaching,self).__init__(parent)
        layout = QVBoxLayout()
        funcs  = readline(defautl_function)
        self.model_folder           = model_folder
        self.boxModel               = BoxModel(model_folder)
        self.listShape              = QListWidget(self)
        self.boxFunction            = BoxFunction(funcs)
        self.boxSelectedFunction    = BoxSelectedFunction()
        self.boxParameter           = BoxParameter()
        self.autotest               = QCheckBox("Auto Test")
        self.ln_timeout             = QSpinBox(self)
        self.cbb_shape              = QComboBox(self)
        self.but_save               = newButton("Save",self.save,"save")
        self.but_apply              = newButton("Apply",self.apply,"apply")

        self.boxFunction.itemClickedSignal.connect(self.funcClicked)
        self.listShape.clicked.connect(self.itemClicked)
        self.autotest.stateChanged.connect(self.stateChanged)

        self.ln_timeout.setRange(1,1000)
        self.ln_timeout.setSingleStep(10)
        self.ln_timeout.setValue(100)

        tab1                        = QWidget()
        layout1                     = QVBoxLayout()
        widgets1 = [
            self.boxModel,
            self.listShape,
            QLabel("select functions"),
            self.boxFunction,
            QLabel("processing"),
            self.boxSelectedFunction,
        ]
        addWidgets(layout1,widgets1)
        tab1.setLayout(layout1)

        tab2                        = QWidget()
        layout2                     = QVBoxLayout()
        widgets2 = [
            self.boxParameter
        ]
        addWidgets(layout2,widgets2)
        tab2.setLayout(layout2)

        tabWidget                   = QTabWidget(self)
        tabWidget.addTab(tab1,"Shape")
        tabWidget.addTab(tab2,"Params")

        autotest                     = QHBoxLayout()
        widgets1 = [
            self.autotest,
            QLabel("Timeout"),
            self.ln_timeout,
            QLabel("Shape"),
            self.cbb_shape
        ]
        addWidgets(autotest,widgets1)

        widgets = [
            self.but_apply,
            self.but_save
        ]
        buttons                     = QHBoxLayout()
        addWidgets(buttons,widgets)

        widgets = [
            tabWidget,
            autotest,
            buttons
        ]
        addWidgets(layout,widgets)

        self.setLayout(layout)
    
    def apply(self):
        self.window().apply()
    def stateChanged(self,state):
        shapes = self.window().canvas.shapes
        labels = [shape.label for shape in shapes] + ["None"]
        self.cbb_shape.clear()
        addItems(self.cbb_shape,labels)
        self.cbb_shape.setCurrentIndex(-1)
        # self.window().autoPredict()
        pass
    def save(self):
        self.window().saveAll()
        pass
    def itemClicked(self,item):
        row = self.listShape.currentRow()
        self.listShapeCliked.emit(row)
        pass
    def funcClicked(self,item):
        if item.checkState() == Qt.Checked:
            self.boxSelectedFunction.list.addItem(item.text())
    
    def chooseModel(self):
        pass
    
    def setConfig(self,config):
        self.boxParameter.items.setConfig(config)
        functions       = config["function"]["Functions"].split(",")
        
        self.boxSelectedFunction.list.clear()
        addItems(self.boxSelectedFunction.list,functions)
        pass
    def getConfig(self):
        config = {}
        item               = self.boxParameter.items
        boxFunc            = self.boxSelectedFunction
        functions          = [boxFunc.list.item(i).text() for i in range(boxFunc.list.count())]
        functions          = ",".join(functions)

        config["camera"]   = {
            "Type"     : item.camera_type.currentText(),
            "SN"       : item.camera_id.text()
        }
        config["frame"]   = {
            "Width"    : self.window().canvas.width_,
            "Height"   : self.window().canvas.height_
        }
        config["function"] = {
            "Functions"     : functions
        }
        config["crop"]     = {
            "Box"      : item.crop.text(),
            "QRect"    : item.qrect.text()
        }
        config["convert"]  = {
            "Type"     : item.convert.currentText()
        }
        config["binary"]   = {
            "Threshold": item.binary_threshold.text(),
            "Method"   : item.binary_method.currentText(),
            "Type"     : item.binary_type.currentText(),
            "BlockSize": item.binary_blocksize.text(),
        }
        config["blur"]     = {
            "Method"   : item.blur_method.currentText(),
            "Size"     : item.blur_size.text()
        }
        config["morph"]    = {
            "Method"   : item.morph_method.currentText(),
            "Size"     : item.morph_size.text(),
            "Iter"     : item.morph_iter.text()
        }
        config["contours"]    = {
            "Mode"   : item.cnts_mode.currentText(),
            "Method"     : item.cnts_method.currentText()
        }
        config["remove"]   = {
            "Width"    : item.remove_width.text(),
            "Height"   : item.remove_height.text(),
            "Area"     : item.remove_area.text()
        }
        config["ocr"]      = {
            "Lang"     : item.orc_lang.currentText(),
            "Oem"      : item.orc_oem.currentText(),
            "Psm"      : item.orc_psm.currentText()
        }
        config["matching"] = {
            "Score"    : item.match_score.text(),
            "File"     : item.match_filename.text(),
            "Multiple" : str(item.match_multi.isChecked())
        }
        return config

class BBox(QDialog):
    def __init__(self):
        super(BBox,self).__init__()
        layout = QVBoxLayout()
        bb = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        bb.rejected.connect(self.reject)
        bb.accepted.connect(self.accept)
        layout.addWidget(bb)
        self.setLayout(layout)
    def popUp(self):
        self.move(QCursor.pos())
        return True if self.exec_() else False


if __name__ == "__main__":
    QColor().red
    import sys
    app = QApplication(sys.argv)
    # wd = QMainWindow()
    canvas = BoxSelectedFunction()
    # wd.setCentralWidget(canvas)
    canvas.showNormal()
    sys.exit(app.exec_())