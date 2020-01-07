from libs.utils import*
# from vision import*
# import resources

BB = QDialogButtonBox
DEFAUT_COLOR = QColor(0,255,0,255)

class BBox(QDialog):
    def __init__(self):
        super(BBox,self).__init__()
        layout = QVBoxLayout()
        bb = BB(BB.Ok|BB.Cancel)
        bb.rejected.connect(self.reject)
        bb.accepted.connect(self.accept)
        layout.addWidget(bb)
        self.setLayout(layout)
    def popUp(self):
        self.move(QCursor.pos())
        return True if self.exec_() else False

class BoxPassword(QDialog):
    def __init__(self,parent=None):
        super(BoxPassword,self).__init__(parent)
        self.setWindowTitle("Password")
        layout = QVBoxLayout()
        bb = BB(BB.Ok|BB.Cancel)
        bb.rejected.connect(self.reject)
        bb.accepted.connect(self.accept)
        self.ln_password = QLineEdit()
        self.ln_password.setFocus()
        self.ln_password.setEchoMode(QLineEdit.Password)
        addWidgets(layout,[self.ln_password,bb])
        self.setLayout(layout)
    def popUp(self):
        self.move(QCursor.pos())
        return self.ln_password.text() if self.exec_() else ""

class BoxImageResult(QDialog):
    def __init__(self,parent=None):
        super(BoxImageResult,self).__init__(parent)
        layout          = QVBoxLayout()
        self.frame      = QLabel(self)
        self.boxShapeStatus = BoxTableWidget(["Shape","Status","Inference time","Predict"],self)
        self.boxShapeStatus.setMaximumHeight(300)
        self.frame.setAlignment(Qt.AlignCenter)
        addWidgets(layout,[self.frame,self.boxShapeStatus])
        self.setLayout(layout)

class BoxDecision(QDialog):
    def __init__(self,shapes,parent=None):
        super(BoxDecision,self).__init__(parent)
        self.plainText = QPlainTextEdit(self)

        # self.cbb_shapes = newCbb(shapes,self)
        # self.ch_text    = QCheckBox("Text")
        
        bb = BB(BB.Ok|BB.Cancel)
        bb.rejected.connect(self.reject)
        bb.accepted.connect(self.accept)

        layout = QVBoxLayout()
        addWidgets(layout,[self.plainText,bb])
        self.setLayout(layout)
    
    def _eval_(self,plainText):
        with open("decision.py","a") as ff:
            ff.write(plainText)

    def popUp(self):
        self.move(QCursor.pos()) 
        return self._eval_(self.plainText.toPlainText()) if self.exec_() else ""

    #     checkbox = partial(newCheckBox,self)
    #     self.ch_mean            = checkbox("Use",slot=self.stateChanged)
    #     self.ch_remove          = checkbox("Use",slot=self.stateChanged)
    #     self.ch_countNoneZero   = checkbox("Use",slot=self.stateChanged)
    #     self.ln_mean            = QLineEdit("100",self)
    #     self.ln_vMean           = QLineEdit("0,0,0",self)
    #     self.ln_countNoneZero   = QLineEdit("100",self)
    #     self.ln_remove          = QLineEdit("0",self)

    #     self.cbb_mean           = newCbb(["LessThan","MoreThan"],self.stateChanged)
    #     self.cbb_countNoneZero  = newCbb(["LessThan","MoreThan"],self.stateChanged)
    #     self.cbb_remove         = newCbb(["LessThan","MoreThan"],self.stateChanged)

    #     self.ln_mean.textChanged.connect(self.stateChanged)
    #     self.ln_vMean.textChanged.connect(self.stateChanged)
    #     self.ln_countNoneZero.textChanged.connect(self.stateChanged)
    #     self.ln_remove.textChanged.connect(self.stateChanged)

    #     grid = QGridLayout()
    #     grid.addWidget(self.ch_mean,0,0)
    #     grid.addWidget(QLabel("value"),0,1)
    #     grid.addWidget(self.ln_vMean,0,2)
    #     grid.addWidget(QLabel("threshold"),1,1)
    #     grid.addWidget(self.ln_mean,1,2)
    #     grid.addWidget(QLabel("compare"),2,1)
    #     grid.addWidget(self.cbb_mean,2,2)

    #     group1 = QGroupBox("Mean")
    #     group1.setLayout(grid)

    #     grid = QGridLayout()
    #     grid.addWidget(self.ch_countNoneZero,0,0)
    #     grid.addWidget(QLabel("threshold"),0,1)
    #     grid.addWidget(self.ln_countNoneZero,0,2)
    #     grid.addWidget(QLabel("compare"),1,1)
    #     grid.addWidget(self.cbb_countNoneZero,1,2)

    #     group2 = QGroupBox("CountNoneZero")
    #     group2.setLayout(grid)

    #     grid = QGridLayout()
    #     grid.addWidget(self.ch_remove,0,0)
    #     grid.addWidget(QLabel("threshold"),0,1)
    #     grid.addWidget(self.ln_remove,0,2)
    #     grid.addWidget(QLabel("compare"),1,1)
    #     grid.addWidget(self.cbb_remove,1,2)

    #     group3 = QGroupBox("Remove")
    #     group3.setLayout(grid)

    #     layout = QVBoxLayout()
    #     addWidgets(layout,[group1,group2,group3])
    #     self.setLayout(layout)
    #     self.decision = {'Mean': {'state': True, 'value': '0,0,0', 'threshold': '50', 'compare': 0}, 
    #                     'CountNoneZero': {'state': True, 'threshold': '100', 'compare': 1},
    #                     'Remove': {'state': True, 'threshold': '0', 'compare': 1}}
    # def setValue(self,decision):
    #     state            = decision["Mean"]["state"]
    #     threshold        = decision["Mean"]["threshold"]
    #     vmean            = decision["Mean"]["value"]
    #     i                = decision["Mean"]["compare"]
    #     self.ch_mean.setChecked(state)
    #     self.ln_vMean.setText(vmean)
    #     self.ln_mean.setText(threshold)
    #     self.cbb_mean.setCurrentIndex(i)
        
    #     state            = decision["CountNoneZero"]["state"]
    #     threshold        = decision["CountNoneZero"]["threshold"]
    #     i                = decision["CountNoneZero"]["compare"]
    #     self.ch_countNoneZero.setChecked(state)
    #     self.ln_countNoneZero.setText(threshold)
    #     self.cbb_countNoneZero.setCurrentIndex(i)

    #     state            = decision["Remove"]["state"]
    #     threshold        = decision["Remove"]["threshold"]
    #     i                = decision["Remove"]["compare"]
    #     self.ch_remove.setChecked(state)
    #     self.ln_remove.setText(threshold)
    #     self.cbb_remove.setCurrentIndex(i)

    #     pass
    # def stateChanged(self):
    #     isMean          = self.ch_mean.isChecked()
    #     isCountNoneZero = self.ch_countNoneZero.isChecked()
    #     isRemove        = self.ch_remove.isChecked()

    #     type_mean       = self.cbb_mean.currentIndex()
    #     type_noneZero   = self.cbb_countNoneZero.currentIndex()
    #     type_remove     = self.cbb_remove.currentIndex()

    #     thresh_mean     = self.ln_mean.text()
    #     if thresh_mean == "":
    #         thresh_mean = "0"

    #     vmean            = self.ln_vMean.text().split(",")
    #     missing          = 3 - len(vmean)
    #     if missing > 0:
    #         for i in range(missing):
    #             vmean+=["0"]
    #     elif missing < 0:
    #         vmean = vmean[:3]
    #     for i in range(len(vmean)):
    #         if vmean[i] == "":
    #             vmean[i] = "0"
        
    #     vmean           = ",".join(vmean)

    #     noneZero        = self.ln_countNoneZero.text()
    #     if noneZero == "":
    #         noneZero = "0"
    #     remove          = self.ln_remove.text()
    #     if remove == "":
    #         remove = "0"

    #     self.decision["Mean"]       = {"state":isMean,"value":vmean,"threshold":thresh_mean,"compare":type_mean}
    #     self.decision["CountNoneZero"]   = {"state":isCountNoneZero,"threshold":noneZero,"compare":type_noneZero}
    #     self.decision["Remove"]     = {"state":isRemove,"threshold":remove,"compare":type_remove}


class BoxInrange(QWidget):
    inRangeSignal = pyqtSignal(dict)
    def __init__(self,parent=None):
        super(BoxInrange,self).__init__(parent)
        slider = partial(newSlider,self)
        self.h = slider((0,255),0,1,self.valueChanged)
        self.H = slider((0,255),0,1,self.valueChanged)
        self.s = slider((0,255),0,1,self.valueChanged)
        self.S = slider((0,255),0,1,self.valueChanged)
        self.v = slider((0,255),0,1,self.valueChanged)
        self.V = slider((0,255),0,1,self.valueChanged)

        self.lb_h = QLabel("0",self)
        self.lb_H = QLabel("0",self)
        self.lb_s = QLabel("0",self)
        self.lb_S = QLabel("0",self)
        self.lb_v = QLabel("0",self)
        self.lb_V = QLabel("0",self)

        sl      = [self.h,self.H,self.s,self.S,self.v,self.V]
        value   = [self.lb_h,self.lb_H,self.lb_s,self.lb_S,self.lb_v,self.lb_V]
        lb      = ["h","H","s","S","v","V"]
        widgets = []
        for l,s,v in zip(lb,sl,value):
            layout = QHBoxLayout()
            addWidgets(layout,[QLabel(l,self),s,v])
            widgets.append(layout)

        layout = QVBoxLayout()
        addWidgets(layout,widgets)

        self.setLayout(layout)

        # 
        self.range = {"H":(0,0),"S":(0,0),"V":(0,0)}

    def setValue(self,inrange):
        h,H     = inrange["H"]
        s,S     = inrange["S"]
        v,V     = inrange["V"]
        self.h.setValue(h)
        self.H.setValue(H)
        self.s.setValue(s)
        self.S.setValue(S)
        self.v.setValue(v)
        self.V.setValue(V)
    def valueChanged(self):
        h,H     = self.h.value(),self.H.value()
        s,S     = self.s.value(),self.S.value()
        v,V     = self.v.value(),self.V.value()

        self.lb_h.setText(str(h))
        self.lb_H.setText(str(H))
        self.lb_s.setText(str(s))
        self.lb_S.setText(str(S))
        self.lb_v.setText(str(v))
        self.lb_V.setText(str(V))

        self.range["H"] = (h,H)
        self.range["S"] = (s,S)
        self.range["V"] = (v,V)

        self.inRangeSignal.emit(self.range)

class BoxButtons(QDialog):
    def __init__(self,parent=None):
        super(BoxButtons,self).__init__(parent)
        self.but_auto       = newButton("Auto",self.switchWidget,"home")
        self.but_manual     = newButton("Manual",self.switchWidget,"manual")
        self.but_teach      = newButton("Teach",self.switchWidget,"teach")
        self.but_data       = newButton("Data",self.switchWidget,"data")
        widgets=[
            self.but_auto,
            self.but_manual,
            self.but_teach,
            self.but_data
        ]
        layout = QHBoxLayout()
        addWidgets(layout,widgets)
        self.setMaximumHeight(100)
        for w in widgets:
            w.setFixedHeight(50)
        self.setLayout(layout)
    
    def switchWidget(self):
        window = self.window()
        if self.sender() == self.but_auto:
            window.stacker.setCurrentWidget(window.camera)
        elif self.sender() == self.but_manual:
            window.stacker.setCurrentWidget(window.manual)
            # self.window().camera.signal_emit = True
            # runThread(self.actived)
        elif self.sender() == self.but_teach:
            window.stacker.setCurrentWidget(window.canvas)
            window.actions.open_.setEnabled(True)
        elif self.sender() == self.but_data:
            window.stacker.setCurrentWidget(window.data)
        pass
    
    def actived(self):
        # n = 0
        # while n < 10e4:
        #     n+=1
        #     self.window().camera.signal_emit = True
        #     time.sleep(0.02)
        print("BYE BYE")

class BoxCamera(QDialog):
    WEBCAM      = "Webcam"
    BASLER      = "Basler"
    CONTINOUS   = "Continous"
    ACTIVE      = "Active"
    runProcSignal = pyqtSignal(np.ndarray)
    fpsSignal     = pyqtSignal(float)
    def __init__(self,timeout,emit_timeout = 0.01,top=False,button=False,parent=None):
        super(BoxCamera,self).__init__(parent)
        self.setWindowTitle("Camera Dialog")
        layout          = QVBoxLayout()
        self.frame      = QLabel(self)
        self.frame.setAlignment(Qt.AlignCenter)

        hlayoutTop          = QHBoxLayout()
        self.cbb_camera     = newCbb([self.WEBCAM,self.BASLER],self.cbbActived)
        self.cbb_emit       = newCbb([self.CONTINOUS,self.ACTIVE],self.cbbActived)
        self.ln_idCamera    = QLineEdit("0",self)
        self.but_connect    = newButton("Open",self.openCamera,"openCamera")
        self.lb_fps         = QLabel("",self)
        # self.lb_fps.setMaximumHeight(50)
        widgets = [
            QLabel("Camera"),
            self.cbb_camera,
            self.cbb_emit,
            self.ln_idCamera,
            self.but_connect,
            self.lb_fps
        ]
        addWidgets(hlayoutTop,widgets)
        widgetTop = QWidget()
        widgetTop.setLayout(hlayoutTop)
        widgetTop.setMaximumHeight(50)
        # widgetTop.setMaximumWidth(500)

        if button:
            hlayout        = QHBoxLayout()
            self.but_start = newButton("Start",self.start,"start")
            self.but_stop = newButton("Stop",self.stop,"stop")
            self.but_reset = newButton("Reset",self.reset,"reset")
            self.but_grab  = newButton("Grab",self.capture,"grab")
            widgets = [
                self.but_start,
                self.but_stop,
                self.but_grab,
                self.but_reset
            ]
            addWidgets(hlayout,widgets)
            widgets = [
                widgetTop,
                hlayout,
                self.frame
            ]
        else:
            widgets = [
                widgetTop,
                self.frame
            ]

        addWidgets(layout,widgets)
        self.setLayout(layout)

        self.cap            = None
        self.mat            = None
        self.type           = ""
        self.mat            = None
        self.timeout        = timeout
        self.emit           = self.CONTINOUS # emit iamge process continous
        self.signal_emit    = False # signal emit image process when emit type ACTIVED
        self.emit_timeout   = emit_timeout
        self.visualize  = {"boxs":None,"visualizes":None}

        self.bStart = False
        self.fps = 0
        self.t0 = 0
        self.fpsSignal.connect(self.setFPS)

    def cbbActived(self):
        self.type = self.cbb_camera.currentText()
        self.emit = self.cbb_emit.currentText()
        pass
    def openCamera(self):
        # camera = self.cbb_camera.currentText()
        id_camera = self.ln_idCamera.text()
        if self.but_connect.text() == "Open":
            if self.type == self.WEBCAM:
                # self.type = self.WEBCAM
                id_camera = int(id_camera)
                if self.cap is not None:
                    self.cap.release()
                self.cap = cv2.VideoCapture(id_camera)
                if self.isOpened():
                    self.window().boxProcess.log("Camera %d is opened"%id_camera)
                    self.but_connect.setText("Close")
                    self.cbb_camera.setEnabled(False)
                    self.ln_idCamera.setEnabled(False)
                else:
                    self.window().boxProcess.log("Camera %d failed"%id_camera)
            elif self.type == self.BASLER:
                # self.type = self.BASLER
                pass
            
        elif self.but_connect.text() == "Close":
            if self.type == self.WEBCAM:
                self.cap.release()
                if not self.isOpened():
                    id_camera = int(id_camera)
                    self.window().boxProcess.log("Camera %d is closed"%id_camera)
            elif self.type == self.BASLER:
                pass
            self.but_connect.setText("Open")
            self.cbb_camera.setEnabled(True)
            self.ln_idCamera.setEnabled(True)

        pass
    def setFPS(self,fps):
        self.lb_fps.setText("FPS : %.2f"%fps)
    def isOpened(self):
        if self.type == self.WEBCAM:
            return self.cap.isOpened()
        elif self.type == self.BASLER:
            return True

    def capture(self):
        mkdir("grab")
        mat = self.grab()
        if mat is not None:
            filename        = "grab/%s.png"%getStrDateTime()
            if cv2.imwrite(filename,mat):
                print("image saved at %s"%filename)
    def grab(self):
        ret = False
        self.mat = None
        if self.type == self.WEBCAM:
            ret,self.mat = self.cap.read()
        elif self.type == self.BASLER:
            pass
        if ret:
            return self.mat
        else:
            return None
    def start(self):
        if self.cap is None:
            return
        self.bStart     = True
        # run main process
        runThread(self.window().main_process,args=())
        # live camera
        runThread(self.loop,args=())
        # 
        self.but_connect.setEnabled(False)
        self.window().boxProcess.log("start")
        self.window().boxTeaching.setEnabled(False)
        pass
    def stop(self):
        if self.bStart :
            # stop camera
            self.bStart = False
            # stop main process 
            self.window().bRun = False
            # 
            self.but_connect.setEnabled(True)
            self.window().boxProcess.log("stop")
            self.window().boxTeaching.setEnabled(True)

        pass
    def reset(self):
        pass
    def release(self):
        self.bStart  = False
        time.sleep(0.01)
        if self.type == self.WEBCAM:
            if self.cap is not None:
                self.cap.release()
        elif self.type == self.BASLER:
            if self.cap is not None:
                pass
        
    def loop(self):
        print("loop camera started")
        fps = 0
        t0 = time.time()
        self.t0 = time.time()
        while self.bStart and self.isOpened():
            self.mat = self.grab()
            if self.mat is not None:
                #
                if self.emit == self.CONTINOUS:
                    if(time.time() - t0) >= self.emit_timeout:
                        self.runProcSignal.emit(self.mat)
                        t0 = time.time()
                elif self.signal_emit:
                    self.runProcSignal.emit(self.mat)
                    self.signal_emit = False
                    pass
                print("+++++BEGIN+++++++")
                
                # else:
                showImage(self.mat,self.frame)
                print("+++++END+++++++")

                self.fps+=1
                if(time.time() - self.t0) >= 1.0:
                    self.fpsSignal.emit(self.fps)
                    self.fps = 0
                    self.t0 = time.time()

            time.sleep(self.timeout)
        pass
    
    def __del__(self):
        self.release()
    def closeEvent(self):
        self.release()
        pass


class BoxManual(QWidget):
    def __init__(self,parent=None):
        super(BoxManual,self).__init__(parent)
        layout = QVBoxLayout()
        button = newButton("Run Process",self.runManual)
        layout.addWidget(button)
        self.setLayout(layout)
    
    def runManual(self):
        self.window().camera.signal_emit = True


class BoxData(QWidget):
    def __init__(self,parent=None):
        super(BoxData,self).__init__(parent)


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

class BoxComPort(QWidget):
    def __init__(self,parent):
        super(BoxComPort,self).__init__()

    pass

class Params(object):
    def __init__(self,parent):
        super(Params,self).__init__()
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
        self.orc_oem.setCurrentIndex(1)
        self.orc_psm          = newCbb(["%d"%i for i in range(14)])
        self.orc_psm.setCurrentIndex(3)
        self.orc_lang         = newCbb(["eng","vie","kor"])

        self.match_score      = spin2
        self.match_filename   = QLineEdit("",parent)
        self.match_multi      = QCheckBox("",parent)

        self.camera_type      = newCbb(["webcam","basler"])
        self.camera_id        = QLineEdit("...",parent)

        self.inrange          = BoxInrange(parent)
        # self.decision         = BoxDecision(parent)

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
            inrange         = cfg["inrange"]
            self.inrange.setValue(inrange)
            # decision        = cfg["decision"]
            # self.decision.setValue(decision)
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
class BoxTableWidget(QTableWidget):
    def __init__(self,headers,parent=None):
        super(BoxTableWidget,self).__init__(parent)
        self.verticalHeader().hide()
        self.setColumnCount(len(headers))
        for i in range(len(headers)):
            self.setHorizontalHeaderItem(i,QTableWidgetItem(headers[i]))

    def __setitem__(self,key,value):
        row = self.rowCount()
        if row > key:
            for i,text in enumerate(value):
                self.setItem(key,i,QTableWidgetItem(text))
        else:
            self.setRowCount(key+1)
            for i,text in enumerate(value):
                self.setItem(key,i,QTableWidgetItem(text))
    
    def __getitem__(self,key):
        texts = []
        n = self.rowCount()
        for i in range(self.columnCount()):
            texts.append(self.item(key,i).text())
        return texts



class BoxProcessResult(QDialog):
    def __init__(self,parent=None):
        super(BoxProcessResult,self).__init__(parent)
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

        self.but_clear      = newButton("Clear",self.clear,"clear")

        hlayout        = QHBoxLayout()
        self.but_start = newButton("Start",None,"start")
        self.but_stop = newButton("Stop",None,"stop")
        self.but_reset = newButton("Reset",None,"reset")
        self.but_grab  = newButton("Grab",None,"grab")
        widgets = [
            self.but_start,
            self.but_stop,
            self.but_grab,
            self.but_reset
        ]
        addWidgets(hlayout,widgets)
        
        widget = [
            grid,
            self.lb_result,
            self.list,
            self.but_clear,
            hlayout
        ]
        layout = QVBoxLayout()
        addWidgets(layout,widget)

        self.setLayout(layout)

    def clear(self):
        self.list.clear()
    def log(self,text):
        self.list.addItem("%s : %s"%(getStrTime(),text))
    
    def showResult(self,nums,res=-1):
        style = "color:black;font:bold 36px;border-width:3px;background:%s \
        ;border-color:black;border-style: outset"
        ok , ng ,total = nums
        self.numOK.setText("%d"%ok)
        self.numNG.setText("%d"%ng)
        self.numTotal.setText("%d"%total)
        if res == -1:
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
        lbs = "Camera Crop Convert Binary Blur Morph Contours Remove OCR Matching InRange".split()
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
            "Range"
        ]
        self.lb_item  = lbs
        self.lb_child = child
        for i,lb,ch in zip(range(len(lbs)),lbs,child):
            item   = QTreeWidgetItem([lb])
            chs    = ch.split()
            self.addTopLevelItem(item)
            for x in chs:
                self.topLevelItem(i).addChild(QTreeWidgetItem([x]))
            
        self.items = Params(self)
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

        addWidget(10,0,self.items.inrange)
        # addWidget(11,0,self.items.decision)

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
        models = os.listdir(folder)+["None"]
        addItems(self.cbb_model,models)
        self.cbb_model.setCurrentIndex(len(models)-1)

class BoxFunction(QListWidget,QDialog):
    def __init__(self,items,parent=None):
        super(BoxFunction,self).__init__(parent)
        if items:
            addItems(self,items)
            for i in range(len(items)):
                item = self.item(i)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(not Qt.Checked)

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
        deleteAll          = action("Delete All",self.deleteAll,"","delete_all","delete all functions")
        deleteFunc         = action("Delete",self.deleteFunc,"","delete","delete function")
        prevFunc           = action("Up",self.prevFunc,"","up","prev function")
        nextFunc           = action("Down",self.nextFunc,"","down","next function")
        cancel             = action("Cancel",None,"","cancel","cancel")

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
    def __init__(self,model_folder,defautl_function,parent=None):
        super(BoxTeaching,self).__init__(parent)
        layout = QVBoxLayout()
        funcs  = readline(defautl_function)
        self.parent                 = parent
        self.model_folder           = model_folder
        self.boxModel               = BoxModel(model_folder)
        self.listShape              = QListWidget(self)
        self.boxFunction            = BoxFunction(funcs)
        self.boxSelectedFunction    = BoxSelectedFunction()
        self.boxParameter           = BoxParameter()
        self.autotest               = QCheckBox("Auto Test")
        self.cbb_shape              = QComboBox(self)
        self.but_save               = newButton("Save",self.save,"save")
        self.but_apply              = newButton("Apply",self.apply,"apply")

        self.boxFunction.itemClicked.connect(self.funcClicked)
        self.listShape.itemClicked.connect(self.itemClicked)
        self.autotest.stateChanged.connect(self.stateChanged)

        self.boxParameter.items.inrange.inRangeSignal.connect(self.inRange)

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
        self.parent.apply()
    def inRange(self,range_):
        window = self.parent
        h,H = range_["H"]
        s,S = range_["S"]
        v,V = range_["V"]
        if self.autotest.isChecked():
            idx = window.canvas.shapes.index(window.canvas.shapeSelected)
            window.canvas.testActionSignal.emit(window.canvas.shapes[idx])

    def stateChanged(self,state):
        shapes = self.parent.canvas.shapes
        labels = [shape.label for shape in shapes] + ["None"]
        self.cbb_shape.clear()
        addItems(self.cbb_shape,labels)
        self.cbb_shape.setCurrentIndex(-1)
        # self.window().autoPredict()
        pass
    def save(self):
        self.parent.saveAll()
        pass
    def itemClicked(self,item):
        row = self.listShape.currentRow()
        for i in range(len(self.parent.canvas.shapes)):
            self.parent.canvas.shapes[i].selected = row == i
            self.parent.canvas.shapeSelected      = self.parent.canvas.shapes[row]
        self.parent.canvas.selectedShapeSignal.emit(True)

        pass
    def funcClicked(self,item):
        if item.checkState() == Qt.Checked:
            self.boxSelectedFunction.list.addItem(item.text())
        
        row = self.boxFunction.currentIndex()
        fun = eval(item.text())
        tooltip = DEF_FUNCTIONS[fun].__doc__
        self.setToolTip(tooltip)
    
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
            "Width"    : self.parent.canvas.width_,
            "Height"   : self.parent.canvas.height_
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
        config["inrange"] = {
            "H"    : item.inrange.range["H"],
            "S"    : item.inrange.range["S"],
            "V"    : item.inrange.range["V"],
        }
        # config["decision"] = {
        #     "Mean"              : item.decision.decision["Mean"],
        #     "CountNoneZero"     : item.decision.decision["CountNoneZero"],
        #     "Remove"            : item.decision.decision["Remove"],
        # }
        return config


if __name__ == "__main__":
    QColor().red
    import sys
    app = QApplication(sys.argv)
    wd = QMainWindow()
    # box = BoxSelectedFunction(["A","B","C"])
    box  = BoxSettingCamera(wd)
    box.show()
    # wd.setCentralWidget(box)
    # wd.setCentralWidget(canvas)
    sys.exit(app.exec_())