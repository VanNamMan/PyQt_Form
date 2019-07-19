from tkinter import *
from tkinter import ttk,filedialog,messagebox

from libs.myCanvas import myCanvas
from libs.myDefine import *
# import libs.myCamera as myCam
from pypylon import pylon,genicam

from PIL import Image,ImageTk
import threading,time,os,cv2

# BASLER = "Basler"
# DINO = "Dino"

class balserCamera:
    def __init__(self,dev,bGrabbing,strSerinumber):
        self.dev = dev
        self.bGrabbing = bGrabbing
        self.sn = strSerinumber
class usbCamera:
    def __init__(self,dev,bOpened,deviceName):
        self.dev = dev
        self.bOpened = bOpened
        self.deviceName = deviceName
class cameraDlg(Toplevel):
    def __init__(self,title,cameraName,devices):
        super(cameraDlg,self).__init__(width=500,height=400)
        self.title(title)
        self.cameraName = cameraName
        self.bLive = False
        self.curDevice = None
        self.devices = devices
        self.image = None
        self.initGui()
        self.protocol("WM_DELETE_WINDOW",self.on_closing)
    def initGui(self):
        # self.canvas = myCanvas(self,bg=YELLOW1,w=640,h=480)
        self.canvas = Label(self,text="My Camera",bg=BLUE5,width=65,height=25)
        self.canvas.pack(fill="both")
        font = ("Arial 10 bold")
        self.butLive = Button(self,text="Live",width=10,height=2,font=font
                    ,command=self.live)
        self.butLive.pack(side=LEFT)

        self.butStop = Button(self,text="Stop",width=10,height=2,font=font
                    ,command=self.stop)
        self.butStop.pack(side=LEFT)

        self.butGetImage = Button(self,text="Get Image",width=10,height=2,font=font
                    ,command=self.getImage)
        self.butGetImage.pack(side=LEFT)

        self.cbbDevies = ttk.Combobox(self,width=20)
        self.cbbDevies.pack(side=RIGHT,anchor=NE)
        # get all devices basler and start grabbing
        try :
            self.cbbDevies["values"] = [dev[2] for dev in self.devices]
        except :
            pass
        # ====
        Label(self,text="Devies",width=10).pack(side=RIGHT,anchor=NE)
    # command
    def live(self):
        cbbCurrentText = self.cbbDevies.get()
        if cbbCurrentText == "":
            return
        else:
            if self.cameraName == BASLER:
                self.threadBalserCam(cbbCurrentText)
            if self.cameraName == DINO:
                self.threadUsbCam(cbbCurrentText)
            self.butLive.configure(state = DISABLED)
    def stop(self):
        self.bLive = False
        self.butLive.configure(state = NORMAL)
        pass
    def getImage(self):
        if self.image is None :
            return
        if self.cameraName == BASLER:
            folder = "data/%s/"%self.curDevice.sn
            if not os.path.exists(folder):
                os.mkdir(folder)
            fname = time.strftime("%d%m%y_%H%M%S.jpg")
            cv2.imwrite(os.path.join(folder,fname),self.image)
        else:
            folder = "data/%s/"%self.curDevice.deviceName
            if not os.path.exists(folder):
                os.mkdir(folder)
            fname = time.strftime("%d%m%y_%H%M%S.jpg")
            cv2.imwrite(os.path.join(folder,fname),self.image)
        pass  
    # ====funtion ======
    def show(self,canvas,img):
        w,h = 480,360
        canvas.configure(width=w,height=h)
        if len(img.shape) == 2:
            res = cv2.resize(img,(w,h))
        else:
            res = cv2.resize(img[...,::-1],(w,h))
        pilImg = Image.fromarray(res)
        photoImg = ImageTk.PhotoImage(pilImg)
        canvas["image"] = photoImg
        canvas.image = photoImg
    # thread
    def threadBalserCam(self,strIdCam):
        if self.bLive :
            return
        camera = None
        for device in self.devices:
            dev,bGrabbing,sn = device
            if sn == strIdCam:
                self.curDevice = balserCamera(dev,bGrabbing,sn)
                break
        if self.curDevice.bGrabbing:
            self.bLive = True
            thread = threading.Thread(target=self.loopBaslerCam,args=(self.curDevice,))
            thread.start()
    def loopBaslerCam(self,camera):
        try:
            while camera.bGrabbing and self.bLive:
                grabResult = camera.dev.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                if grabResult.GrabSucceeded():
                    self.image = grabResult.Array
                    self.show(self.canvas,self.image)
                    time.sleep(0.02)
        except:
            # camera.dev.StopGrabbing()
            pass


    def threadUsbCam(self,deviceName):
        if self.bLive :
            return
        camera = None
        for device in self.devices:
            dev,bOpened,name = device
            if name == deviceName:
                self.curDevice = usbCamera(dev,bOpened,name)
                break
        if self.curDevice.bOpened:
            self.bLive = True
            thread = threading.Thread(target=self.loopUsbCam,args=(self.curDevice,))
            thread.start()
        pass
    def loopUsbCam(self,camera):
        try:
            while camera.bOpened and self.bLive:
                ret,image = camera.dev.read()
                if ret:
                    self.image = image
                    self.show(self.canvas,self.image)
                    time.sleep(0.02)
        except:
            pass
        pass
    # =========Closing============
    def __del__(self):
        print ('Camera Dlg destructor called')
    def on_closing(self):
        self.bLive = False
        self.master.destroy()
        print ('Camera Dlg closing called')

# def main():
#     root = Tk()
#     dlg = cameraDlg("Camera")
#     root.mainloop()

# if __name__ == "__main__":
#     main()
