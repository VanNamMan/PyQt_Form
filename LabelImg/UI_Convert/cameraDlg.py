from PyQt5.QtWidgets import QDialog,QFileDialog
from PyQt5.QtGui import QIcon,QPixmap
from UI_Convert.cameraDlg_ui import Ui_camraDlg

from libs.cvLib import *

import threading,time,os

class cameraDlg(QDialog):
    def __init__(self,parent):
        super(cameraDlg,self).__init__(parent)
        self.ui = Ui_camraDlg()
        self.ui.setupUi(self)

        self.ui.rad_webcam.setChecked(True)
        
        self.camera = None
        self.bLoopCamera = True
        self.bOPenCam = False
        self.dTypeCamera = None
        self.cvImg = None
        self.qImage = None
        self.saveFolder = None

        self.myThread(target=self.loopCamera)

        self.ui.but_start.clicked.connect(self.start)
        self.ui.but_start.setIcon(QIcon("res/camera2.png"))
        self.ui.but_stop.clicked.connect(self.stop)
        self.ui.but_stop.setIcon(QIcon("res/stop.png"))
        self.ui.but_capture.clicked.connect(self.capture)
        self.ui.but_capture.setIcon(QIcon("res/capture.png"))

    def start(self):
        if self.ui.rad_webcam.isChecked() :
            try:
                self.dTypeCamera = "webcam"
                txt = self.ui.ln_webcam.text()
                if txt == "":
                    idCam = 0
                else:
                    idCam = int(txt)
                if not self.camera:
                    self.camera = cv2.VideoCapture(idCam)
                self.bOPenCam = self.camera.isOpened()
                self.ui.but_start.setEnabled(False)
            except SystemError as sysErr:
                print(sysErr.args)

    def stop(self):
        self.bOPenCam = False
        self.ui.but_start.setEnabled(True)

    def getStrDateTime(self):
        return time.strftime("%y%m%d_%H%M%S")

    def capture(self):
        if self.saveFolder is None:
            self.saveFolder = QFileDialog.getExistingDirectory(self,"Open Directory",os.getcwd(),
                QFileDialog.ShowDirsOnly| QFileDialog.DontResolveSymlinks)
        if os.path.exists(self.saveFolder):
            if isinstance(self.cvImg,np.ndarray):
                filepath = os.path.join(self.saveFolder,self.getStrDateTime()+".jpg")
                print(filepath)
                cv2.imwrite(filepath,self.cvImg)

    def myThread(self,target,args=()):
        thread = threading.Thread(target=target,args=args)
        thread.start()

    def loopCamera(self):
        while self.bLoopCamera:
            if self.camera and self.bOPenCam:
                ret,self.cvImg = self.camera.read()           
                if ret:
                    self.qImage = cVMatToQImage(self.cvImg)
                    self.ui.label.setPixmap(QPixmap.fromImage(self.qImage))
            time.sleep(0.02)

    def closeEvent(self, event):
        print("Close Camera Dlg")
        self.bLoopCamera = False

    def stopAllThread(self):
        self.bLoopCamera = False
        
    def __del__(self):
        if self.dTypeCamera == "webcam":
            self.camera.release()
        print("Desconstructor Camera Dlg called")
        self.ui = None

# cap = cv2.VideoCapture(0)
# print(cap.isOpened())
