from ui_frame import Ui_Frame

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PIL import ImageQt
from scipy import misc

import threading,time,cv2
from pypylon import pylon,genicam

DINO = "Dino"
BASLER = "Basler"

class FrameDlg(QDialog):
    def __init__(self, parent):
        super(FrameDlg, self).__init__(parent)
        #self.setWindowFlags(Qt.Window)
        self.ui = Ui_Frame()
        self.ui.setupUi(self)
        
        # self.listDevices = self.getDevicesBasler()
        # print(self.listDevices[0].GetDeviceInfo())
        # self.listDevices[0].GetDeviceInfo().GetSerialNumber())
        self.image = None
        self.camera = None
        self.cameraName = ""
        self.bOpenCam = False
        self.bLive = False

        self.ui.but_live.clicked.connect(self.live)

    def live(self):
        if self.ui.but_live.text()=="Live":
            self.bLive = True
            self.ui.but_live.setText("Stop")
            if self.cameraName == DINO:
                self.threadLiveDinoCam()
            elif self.cameraName == BASLER:
                self.threadLiveBaslerCam()
        elif self.ui.but_live.text()=="Stop":
            self.ui.but_live.setText("Live")
            self.bLive = False
        pass

    def liveDinoCam(self):
        while self.bLive and self.bOpenCam:
            ret,image = self.camera.read()
            if ret :
                self.image = image.copy()
                self.showImage(self.ui.frame,image)
            time.sleep(0.02)
        pass
    def threadLiveDinoCam(self):
        thread = threading.Thread(target=self.liveDinoCam,args=())
        thread.start()
        pass

    def liveBaslerCam(self):
        while self.bOpenCam and self.bLive:
            try:
                grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                if grabResult.GrabSucceeded():
                    image = grabResult.Array
                    self.image = image.copy()
                    self.showImage(self.ui.frame,image)
                    time.sleep(0.02)
                else:
                    print("Error: %s,%s"%(grabResult.ErrorCode, grabResult.ErrorDescription))
            except:
                print("Error: %s,%s"%(grabResult.ErrorCode, grabResult.ErrorDescription))

    def threadLiveBaslerCam(self):
        thread = threading.Thread(target=self.liveBaslerCam,args=())
        thread.start()
        pass

    def onCamera(self,cameraName="Dino",idCam=0):
        camera = None
        bOpenCam = False
        if cameraName == DINO:
            try:
                camera = cv2.VideoCapture(idCam)
                bOpenCam = camera.isOpened()
            except:
                pass
            return camera,bOpenCam
        elif cameraName == BASLER:
            # try:
            if idCam == "First Device":
                camera = self.getFirstDevice()
            else:
                devices = pylon.TlFactory.GetInstance().EnumerateDevices()
                cameras = pylon.InstantCameraArray(2)
                for i,cam in enumerate(cameras):
                    try:
                        cam.Attach(pylon.TlFactory.GetInstance().CreateDevice(devices[i]))
                        if cam.GetDeviceInfo().GetSerialNumber() == idCam:
                            camera = cam
                    except:
                        pass
            if camera is not None:
                camera.StartGrabbing()
                bOpenCam = camera.IsGrabbing()
            # except:
            #     pass
        return camera,bOpenCam
    def getDeviceFromSerialNumber(self,listDevices=[],serialNumber=0):
        print(listDevices)
        dev = None
        for device in listDevices:
            if device[1] == serialNumber:
                dev = device[0]
        print(type(dev))
        return dev
    def getDevicesBasler(self):
        dev = []
        try:
            devices = pylon.TlFactory.GetInstance().EnumerateDevices()
            cameras = pylon.InstantCameraArray(2)
            for i,cam in enumerate(cameras):
                cam.Attach(pylon.TlFactory.GetInstance().CreateDevice(devices[i]))
                dev.append(cam)
        except:
            pass
        return dev
    def getFirstDevice(self):
        camera = None
        try:
            camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        except:
            pass
            # self.log("Not found device camera basler.")
        return  camera
        

    def showImage(self,frame,pic):
        h,w = pic.shape[0],pic.shape[1]
        hFrame,wFrame = frame.height(),frame.width()
        img = cv2.resize(pic,(wFrame,hFrame))

        if len(pic.shape) == 2:
            qPix = QPixmap.fromImage(ImageQt.ImageQt(misc.toimage(img)))
            
        else:
            ch = 3
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            qImg = QImage(img.data,wFrame,hFrame,ch*wFrame,QImage.Format_RGB888)
            qPix = QPixmap(qImg)
            
        frame.setPixmap(qPix)

    def __del__(self):
        self.ui = None
    
    bFirst = True
    baseRectElement = []
    widgets = []
    bazeSize = QSize

    def resizeEvent(self, QResizeEvent):
        if self.bFirst:
            self.bFirst = False
            self.bazeSize = self.window().size()
            self.widgets = self.window().findChildren(QWidget)
            for widget in self.widgets:
                self.baseRectElement.append(widget.geometry())
            return

        dScaleW = self.window().width() / self.bazeSize.width()
        dScaleH = self.window().height() / self.bazeSize.height()

        for i in range(0, len(self.widgets)):
            rect = self.baseRectElement[i]
            widget = self.widgets[i]
            newRect = QRect(dScaleW * rect.left(), dScaleH * rect.top(), dScaleW * rect.width(),
                            dScaleH * rect.height())
            widget.setGeometry(newRect)
            widget.updateGeometry()
        # self.showImage(self.ui.frame,self.image)
        return

    def closeEvent(self,QCloseEvent):
        try : 
            self.bLive = False
            time.sleep(0.02)
            if self.bOpenCam:
                try:
                    self.camera.release()
                except:
                    self.camera.StopGrabbing()
                else:
                    pass
        except:
            pass 


        

    