from header import *

def ocr_(mat,cfg):
    txt = pytesseract.image_to_string(mat,config=cfg)
    return txt

def ocr_cmd(filename):
    base,_ = os.path.splitext(filename)
    cmd = "tesseract %s %s -l eng"%(filename,base)
    subprocess.call(cmd,shell=True)

class HashableQListWidgetItem(QListWidgetItem):

    def __init__(self, *args):
        super(HashableQListWidgetItem, self).__init__(*args)

    def __hash__(self):
        return hash(id(self))

class Port(serial.Serial):
    def __init__(self,port="COM1",baud=9600,prefix="@",suffix="\r\n",_timeout=0.01):
        super(Port,self).__init__(port,baud)
        self.prefix = prefix
        self.suffix = suffix
        self.data = ""
        self._timeout = 0.01
    
    def isMessage(self,data):
        return re.findall(self.prefix,data) and re.findall(self.suffix,data)
    
    def splitData(self,data):
        start = re.search(self.prefix,data).end()
        end = re.search(self.suffix,data).start()
        return data[start:end]

class struct(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def readline(filename):
    txts = []    
    f = open(filename, "r")
    for x in f:
        x = x.strip().strip("\n")
        txts.append(x)
    return txts

def getStrDateTime():
    return time.strftime("%d%m%y_%H%M%S")

def getStrTime():
    return time.strftime("%H:%M:%S")
def inSide(x,tup):
    m,M = tup
    if M == -1:
        if m == -1:
            return True
        else:
            return m < x
    elif m == -1:
        return x < M

def distance(v1,v2):
    assert len(v1)==len(v2),print("v1,v2 need same length")
    v = np.array([v2[i] - v1[i] for i in range(len(v1))])
    return np.sqrt(np.sum(np.square(v)))

def str2ListInt(string):
    lst = string.split(",")
    return [int(l) for l in lst]

def addItems(cbb,items):
    [cbb.addItem(it) for it in items if it]

def newCbb(items,parent):
    cbb = QComboBox(parent)
    addItems(cbb,items)
    return cbb

def newDialogButton(texts,slots,icons,orient=Qt.Vertical):
    bb = QDialogButtonBox(orient)
    for txt,slot,icon in zip(texts,slots,icons):
        but = bb.addButton(txt,QDialogButtonBox.ApplyRole)
        if slot is not None:
            but.clicked.connect(slot)
        if icon is not None:
            but.setIcon(newIcon(icon))
    return bb

def newSlider(parent,_range,value,step,slot=None):
    sl = QSlider(Qt.Horizontal,parent)
    a,b = _range
    sl.setRange(a,b)
    sl.setValue(value)
    sl.setSingleStep(step)
    if slot is not None:
        sl.valueChanged.connect(slot)
    return sl

def newCheckBox(parent,text,state=False,slot=None):
    ch = QCheckBox(text,parent)
    ch.setCheckState(state)
    if slot is not None:
        ch.stateChanged.connect(slot)
    return ch
    
def newIcon(icon):
    return QIcon(':/' + icon)

def addActions(menu,actions):
    for act in actions:
        if isinstance(act,QAction):
            menu.addAction(act)
        else:
            menu.setMenuBar(act)

def newCbb(items,slot=None):
    cbb = QComboBox()
    [cbb.addItem(item) for item in items]
    if slot is not None:
        cbb.activated.connect(slot)
    return cbb
def newButton(text,slot=None,icon=None):
    b = QPushButton(text)
    if slot is not None:
        b.clicked.connect(slot)
    if icon is not None:
        b.setIcon(newIcon(icon))
    
    return b

def addWidgets(layout,wds):
    for w in wds:
        if isinstance(w,QWidget):
            layout.addWidget(w)
        else:
            layout.addLayout(w)

def addTriggered(action,trigger):
    action.triggered.connect(trigger)

def newAction(parent,text,slot=None,shortcut=None,icon=None,tooltip=None,enabled=True):
    a = QAction(text,parent)
    if icon is not None:
        a.setIcon(newIcon(icon))
    if shortcut is not None:
        a.setShortcut(shortcut)
    if slot is not None:
        a.triggered.connect(slot)
    if tooltip is not None:
        a.setToolTip(tooltip)
    a.setEnabled(enabled)
    return a

def mkdir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def runThread(target,args):
    thread = threading.Thread(target=target,args=args)
    thread.start()

def ndarray2pixmap(arr):
    h,w = arr[:2]
    if len(arr.shape) == 2:
        # qpix = QPixmap.fromImage(ImageQt.ImageQt(misc.toimage(arr)))
        pixmap = QPixmap.fromImage(gray2qimage(arr))
    else:
        # channel = arr.shape[-1]
        rgb = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
        # qim = QImage(rgb.data,w,h,channel*w, QImage.Format_RGB888)
        # qpix = QPixmap(qim)
        pixmap = QPixmap.fromImage(array2qimage(rgb))
    return pixmap

def configProxy2dict(config):
    dict_ = {}
    for key in config.keys():
        dict_[key] = eval(config[key])
    return dict_

class Timer(object):
    __checkin__ = float
    def __init__(self):
        super(Timer,self).__init__()
        self.t0 = time.time()
    
    def start(self):
        self.t0 = time.time()
    
    def dt(self):
        return time.time() - self.t0
    
    def MoreThan(self,dt):
        return True if self.dt() > dt else False
    def LessThan(self,dt):
        return True if self.dt() < dt else False

def showImage(image,label):
    width , height = label.width(),label.height()

    h,w = image.shape[:2]

    s = min(width/w,height/h)

    new_w = int(w*s)
    new_h = int(h*s)

    # t0 = time.time()
    new_img = cv2.resize(image,(new_w,new_h))
    # print(time.time()-t0)
    qpix    = ndarray2pixmap(new_img)
    # if len(image.shape) == 2:
    #     new_img = cv2.cvtColor(new_img, cv2.COLOR_GRAY2RGB)
    #     qpix = QPixmap.fromImage(ImageQt.ImageQt(misc.toimage(new_img)))
    # else:
    #     channel = image.shape[-1]
    #     new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
    #     qim = QImage(new_img.data,new_w,new_h,channel*new_w, QImage.Format_RGB888)
    #     qpix = QPixmap(qim)

    label.setPixmap(qpix)

    return s

if __name__ == "__main__":

    # txts = readline("default_function.txt")
    # print(txts)
    # config = ConfigParser()
    # config.read("demo/para.config")
    # camera = eval(config["Config"]["Camera"])
    mat = cv2.imread("demo/logitech.jpg")
    # from PIL import Image
    text = ocr_(mat,cfg="-l eng")
    print(text)


    
    