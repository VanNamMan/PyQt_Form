from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from libs.shape import *
from libs.myQCamera import *
from libs.myFile import *
from libs.canvas import *
from libs.utils import *
from libs.constants import *
from libs.stringBundle import StringBundle
from libs.shape import Shape, DEFAULT_LINE_COLOR, DEFAULT_FILL_COLOR
from libs.hashableQListWidgetItem import *
from libs.toolBar import ToolBar
from libs.labelDialog import LabelDialog
from libs.colorDialog import ColorDialog
from libs.zoomWidget import ZoomWidget

from libs.cvLib import *
from libs.parameterDlg import ParamerterDialog

import os,time,threading
from functools import partial
# multiprocessing on Gui
from multiprocessing.dummy import Pool

__appname__ = "CopyRight2019 label master."
__imageFile__ = [".jpg",".png",".bmp",".gif",".PNG"]

fileLabel = "label.txt"
listLabel = []
if os.path.exists(fileLabel):
    with open(fileLabel,"r") as inFile:
        listLabel = inFile.readline().split(",")



class WindowMixin(object):

    def menu(self, title, actions=None):
        menu = self.menuBar().addMenu(title)
        if actions:
            addActions(menu, actions)
        return menu
    def toolbar(self, title, actions=None):
        toolbar = ToolBar(title)
        toolbar.setObjectName(u'%sToolBar' % title)
        # toolbar.setOrientation(Qt.Vertical)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if actions:
            addActions(toolbar, actions)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        return toolbar
class labelMaster(QMainWindow,WindowMixin):
     FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = list(range(3))
     def __init__(self):
         QWidget.__init__(self)

         # self.setFixedSize(800, 600)
         # self.descisionDlg = ouput(self)
         self.setWindowTitle("Label Master")
         self.labelCoordinates = QLabel('')
         self.statusBar().addPermanentWidget(self.labelCoordinates)
         # intit 
         self.cvMat = None
         self.qImage = None
         self.dirty = False
         self.saveFolder = None
         self.filePath = None
         self.lastOpenDir = None
         self.mImgList = []
         self.prevLabel = "Enter object label"
         self.bLoopImplement = True
         self.bAutoImplement = False
         self.bSaveOutput = False
         self.bShowResult = True
         self.bSelectionChanged = False
         self.pool = Pool(5)
         self.output = []
         self.bEndThreads = []
         self.t0 = 0

         # self.stringBundle = StringBundle.getBundle()
         # getStr = lambda strId: self.stringBundle.getString(strId)

         self.labelDialog = LabelDialog(listItem=listLabel)
         self.colorDialog = ColorDialog(parent=self)
         self.lineColor = None
         self.textColor = None

         self.itemsToShapes = {}
         self.shapesToItems = {}
         self._noSelectionSlot = []
         self._beginner = True


         self.statusBar().showMessage('%s' % __appname__)
         # self.statusBar().show()
         #============ menu=========
         self.menus = struct(
            file=self.menu('&File'),
            edit=self.menu('&Edit'),
            view=self.menu('&View'),
            help=self.menu('&Help'),
            labelList = QMenu(),
            fileLog = QMenu())

         #================init UI ==============
         action = partial(newAction,self)

         #=======toolBar==========
         openFile = action("Open",self.open
            ,OPEN_FILE,"res/open.png","Open image file")
         openDir = action("Open Dir",self.openDirDialog
            ,OPEN_DIR,"res/openDir.png","Open image folder")
         createShape = action("Create rect box",self.createShape
            ,CREATE,"res/draw.png","Start draw rectangle")
         createPolygon = action("Create polygon",self.createPolygon
            ,CREATE,"res/polygon.png","Start draw polygon")
         copy = action('copy', self.copySelectedShape
            ,COPY,'res/copy.png','dupBoxDetail',enabled=False)
         saveFile = action("Save",self.save
            ,SAVE,"res/save.png","Save parameters")
         editLabel = action("Edit label",self.editLabel
            ,EDIT,"res/edit.png","Editting label", enabled=False)
         deleteShape = action("Delete shape",self.deleteSelectedShape
            ,DLETE,"res/delete.png","Delete shape selected", enabled=False)
         implement = action("Implement",self.implement
            ,IMPLEMENT,"res/event.png","Implement", enabled=False)
         lineColor = action("Line color",lambda:self.boxColor("line")
            ,LINE_COLOR,"res/lineColor.png","Box line color", enabled=True)
         textColor = action("Text color",lambda:self.boxColor("text")
            ,TEXT_COLOR,"res/textColor.png","Box text color", enabled=True)
         font = action("Font",self.boxFont
            ,TEXT_FONT,"res/font.png","Box font text", enabled=True)
         nextImage = action("Next Image",self.openNextImg
            ,NEXT,"res/next.png","Next image", enabled=True)
         backImage = action("Back Image",self.openPrevImg
            ,BACK,"res/back.png","Back image", enabled=True)
         zoomIn = action('zoomin', partial(self.addZoom, 10)
            ,ZOOM_IN, 'res/zoom-in.png','zoominDetail', enabled=False)
         zoomOut = action('zoomout', partial(self.addZoom, -10)
            ,ZOOM_OUT, 'res/zoom-out.png','zoomoutDetail', enabled=False)
         zoomOrg = action('originalsize', partial(self.setZoom, 100)
            ,ZOOM_ORG, 'res/zoom.png','originalsizeDetail', enabled=False)
         fitWindow = action('fitWin', self.setFitWindow
            ,FIT_WINDOW, 'res/fit-window.png','fitWinDetail',checkable=True, enabled=False)
         fitWidth = action('fitWidth', self.setFitWidth
            ,FIT_WIDTH, 'res/fit-width.png','fitWidthDetail',checkable=True, enabled=False)
         clearAll = action('clearAll', self.clearList
            ,CLEAR_ALL, 'res/clear-all.png','Clear all list items',checkable=True, enabled=True)

         showCamera = action('camera', self.showCamera
            ,SHOW_CAMERA,'res/camera2.png','Camera',checkable=True, enabled=True)

         actionMenuFile = [openFile,openDir,saveFile]
         addActions(self.menus.file,actionMenuFile)

         actionMenuEdit = [createShape,implement,editLabel,copy,lineColor,textColor,font,deleteShape]
         addActions(self.menus.edit,actionMenuEdit)

         actionToolbar = (openFile,openDir,saveFile,createShape,createPolygon,editLabel,implement,nextImage,backImage)
         self.toolbar("Tools",actions=actionToolbar)

         self.zoomWidget = ZoomWidget()
         zoom = QWidgetAction(self)
         zoom.setDefaultWidget(self.zoomWidget)
         self.zoomWidget.setWhatsThis(
            u"Zoom in or out of the image. Also accessible with"
            " %s and %s from the canvas." % (fmtShortcut("Ctrl+[-+]"),
                                             fmtShortcut("Ctrl+Wheel")))
         self.zoomWidget.setEnabled(False)
         
        # Group zoom controls into a list for easier toggling.
         beginner = (implement,editLabel,copy,deleteShape)
         self.actions = struct(openFile=openFile,openDir=openDir,saveFile=saveFile
                                ,createShape=createShape,createPolygon=createPolygon
                                ,editLabel=editLabel,deleteShape=deleteShape,copy=copy
                                ,implement=implement
                                ,lineColor=lineColor,textColor=textColor,font=font
                                ,nextImage=nextImage,backImage=backImage
                                ,zoomIn=zoomIn,zoomOut=zoomOut
                                ,zoomOrg=zoomOrg,fitWidth=fitWidth,fitWindow=fitWindow
                                ,beginner=beginner,clearAll=clearAll)

         self.zoomWidget.valueChanged.connect(self.paintCanvas)

         self.zoomMode = self.MANUAL_ZOOM
         self.scalers = {
            self.FIT_WINDOW: self.scaleFitWindow,
            self.FIT_WIDTH: self.scaleFitWidth,
            # Set to one to scale to 100% when loading files.
            self.MANUAL_ZOOM: lambda: 1,
         }
         listLayout = QVBoxLayout()
         listLayout.setContentsMargins(0, 0, 0, 0)

        # Create a widget for using default label
         self.useDefaultLabelCheckbox = QCheckBox('useDefaultLabel')
         self.useDefaultLabelCheckbox.setChecked(False)

         self.defaultLabelTextLine = QLineEdit()

         self.autoImplement = QCheckBox('autoImplement')
         self.autoImplement.setChecked(False)

         self.saveOutput = QCheckBox('saveOutput')
         self.saveOutput.setChecked(False)

         self.updateOuput = QCheckBox('showOutput')
         self.updateOuput.setChecked(True)

         self.autoImplement.stateChanged.connect(self.stateChanged)
         self.saveOutput.stateChanged.connect(self.stateChanged)
         self.updateOuput.stateChanged.connect(self.stateChanged)

         useDefaultLabelQHBoxLayout = QVBoxLayout()
         useDefaultLabelQHBoxLayout.addWidget(self.useDefaultLabelCheckbox)
         useDefaultLabelQHBoxLayout.addWidget(self.defaultLabelTextLine)
         useDefaultLabelQHBoxLayout.addWidget(self.saveOutput)
         useDefaultLabelQHBoxLayout.addWidget(self.updateOuput)
         useDefaultLabelQHBoxLayout.addWidget(self.autoImplement)

         useDefaultLabelContainer = QWidget()
         useDefaultLabelContainer.setLayout(useDefaultLabelQHBoxLayout)
         
        # Create a widget for edit and diffc buttonp
         self.editButton = QToolButton()
         self.editButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
         self.editButton.setDefaultAction(editLabel)

         self.implementButton = QToolButton()
         self.implementButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
         self.implementButton.setDefaultAction(implement)

         buttonLayout = QHBoxLayout()
         buttonLayout.setContentsMargins(0, 0, 0, 0)


        # Add some of widgets to listLayout
         buttonLayout.addWidget(self.editButton)
         buttonLayout.addWidget(self.implementButton)
         listLayout.addLayout(buttonLayout)

         listLayout.addWidget(useDefaultLabelContainer)

        # Create and add a dock widget for showing current label items
         self.labelList = QListWidget()
         addActions(self.menus.labelList, (editLabel, deleteShape))
         self.labelList.setContextMenuPolicy(Qt.CustomContextMenu)
         self.labelList.customContextMenuRequested.connect(
            self.popLabelListMenu)
         self.labelList.itemActivated.connect(self.labelSelectionChanged)
         self.labelList.itemSelectionChanged.connect(self.labelSelectionChanged)
         self.labelList.itemDoubleClicked.connect(self.editLabel)
        # Connect to itemChanged to detect checkbox changes.
         self.labelList.itemChanged.connect(self.labelItemChanged)
         listLayout.addWidget(self.labelList)

         labelListContainer = QWidget()
         labelListContainer.setLayout(listLayout)

         self.fileLogWidget = QListWidget()
         addActions(self.menus.fileLog, [clearAll])
         self.fileLogWidget.setContextMenuPolicy(Qt.CustomContextMenu)
         self.fileLogWidget.customContextMenuRequested.connect(
            self.popfileLogMenu)
         self.fileLogWidget.itemDoubleClicked.connect(self.fileitemDoubleClicked)
         # self.fileLogWidget.itemChanged.connect(self.fileLogRowChanged)
         fileLogLayout = QVBoxLayout()
         fileLogLayout.setContentsMargins(0, 0, 0, 0)
         fileLogLayout.addWidget(self.fileLogWidget)
         fileLogContainer = QWidget()
         fileLogContainer.setLayout(fileLogLayout)

    
         self.dock = QDockWidget('boxLabelText', self)
         self.dock.setObjectName('labels')
         self.dock.setWidget(labelListContainer)

         self.filedock = QDockWidget('fileLog', self)
         self.filedock.setObjectName('files')
         self.filedock.setWidget(fileLogContainer)

         self.parameterdock = QDockWidget('paramsVision', self)
         self.parameterdock.setObjectName('params')
         self.paramerterWidget = ParamerterDialog(self)
         # self.paramerterWidget.ln_kThresh.textChanged.connect(self.textChanged)
         self.parameterdock.setWidget(self.paramerterWidget)

         # self.cameradock = QDockWidget('camera', self)
         # self.cameradock.setObjectName('cameara')
         # self.cameraDlg = cameraDialog(self)
         # self.cameradock.setWidget(self.cameraDlg)

         self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
         self.dockFeatures = QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable
         # self.dock.setFeatures(self.dock.features() ^ self.dockFeatures)
         self.dock.setFeatures(self.dockFeatures)

         self.addDockWidget(Qt.RightDockWidgetArea, self.filedock)
         self.filedock.setFeatures(self.dockFeatures)

         self.addDockWidget(Qt.RightDockWidgetArea, self.parameterdock)
         self.parameterdock.setFeatures(self.dockFeatures)

         # self.addDockWidget(Qt.RightDockWidgetArea, self.cameradock)
         # self.cameradock.setFeatures(self.dockFeatures)

         toggleDock = self.dock.toggleViewAction()
         toggleDock.setText('boxLabel')
         toggleDock.setShortcut(TOGGLE_LABEL_LIST)

         toggleFileDock = self.filedock.toggleViewAction()
         toggleFileDock.setText('logFile')
         toggleFileDock.setShortcut(TOGGLE_LOG_FILE)

         toggleParaDock = self.parameterdock.toggleViewAction()
         toggleParaDock.setText('parameter')
         toggleParaDock.setShortcut(TOGGLE_PARAMETER)

         # toggleCamDock = self.cameradock.toggleViewAction()
         # toggleCamDock.setText('camera')
         # toggleCamDock.setShortcut(TOGGLE_SHOW_CAMERA)

         # self.dock.hide()
         self.filedock.hide()
         self.parameterdock.hide()
         # self.cameradock.hide()
         
         addActions(self.menus.view,[toggleDock,toggleFileDock,toggleParaDock,showCamera])

         # ==============Canvas================
         self.canvas = Canvas(self)
         # load params
         self.loadParams()
         # contextMenu
         addActions(self.canvas.menus[0],self.actions.beginner)
         #=================
         qImage = QImage(640,480,QImage.Format_RGBA8888)
         self.canvas.loadPixmap(QPixmap.fromImage(qImage))
        
         scroll = QScrollArea()
         scroll.setWidget(self.canvas)
         # scroll.setWidget(self.listWidget)
         scroll.setWidgetResizable(True)
         self.scrollBars = {
            Qt.Vertical: scroll.verticalScrollBar(),
            Qt.Horizontal: scroll.horizontalScrollBar()
         }
         self.scrollArea = scroll

         #signal Canvas
         self.canvas.scrollRequest.connect(self.scrollRequest)
         self.canvas.newShape.connect(self.newShape)
         self.canvas.shapeMoved.connect(self.setDirty)
         self.canvas.selectionChanged.connect(self.shapeSelectionChanged)
         self.canvas.zoomRequest.connect(self.zoomRequest)
         self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)

         self.setCentralWidget(scroll)

         self.fitState()
#
         # ==============================

         palette = self.palette()
         role = self.backgroundRole()
         palette.setColor(role, QColor(200, 232, 232, 255))
         self.setPalette(palette)

         palette = self.canvas.palette()
         role = self.canvas.backgroundRole()
         palette.setColor(role, QColor(200, 232, 232, 255))
         self.canvas.setPalette(palette)

         #==start thead implement
         self.myThread(target=self.loopImplement,args=())
         #==start thead OpenCam
     #======Functions==
     def getStrDateTime(self):
        return time.strftime("%y%m%d_%H%M%S")

     def saveImage(self,image=None):
        if self.saveFolder is None:
            self.saveFolder = QFileDialog.getExistingDirectory(self,"Open Directory",os.getcwd(),
                QFileDialog.ShowDirsOnly| QFileDialog.DontResolveSymlinks)
        if os.path.exists(self.saveFolder):
            if isinstance(image,np.ndarray):
                filepath = os.path.join(self.saveFolder,self.getStrDateTime()+".jpg")
                print(filepath)
                cv2.imwrite(filepath,image)

     def logFile(self,obj):
        txt = time.strftime("%H:%M:%S ")+str(obj)
        self.fileLogWidget.addItem(txt)

     def shapeProcess(self,shape):
        #
        print("prosess : ",shape)
        # index = self.canvas.shapes.index(shape)
        index,labels,rect = self.formatShape(shape)
        self.bEndThreads[index] = False
        # result
        shape.result["in"]["id"] = index
        shape.result["in"]["label"] = labels
        shape.result["in"]["rect"] = rect

        try:
            roi = self.qImage.copy(rect)
            cvRoi = qImageToCvMat(roi)
        except:
            cvRoi = None
            return

        lbs = labels.split(",")[:-1]

        for label in lbs:
            if label == OCR:
                text = self.getOCR(shape,label,cvRoi)
            elif label == BARCODE:
                codes = self.getBarCode(shape,label,cvRoi)
            # elif label == CROP:
                # self.saveImage(cvRoi)
        
        # update text , barcode on canvas
        if self.bShowResult and shape.result:
            w,h = rect.width(),rect.height()
            txt = ""
            for key in lbs:
                txt += str(shape.result["out"][key])+"\n"

            self.canvas.text[index] = txt
            rect.setHeight(len(lbs)*rect.height())
            self.canvas.locText[index] = rect.translated(QPoint(0,-h)) 
            self.canvas.update()

        self.bEndThreads[index] = True
        # if self.bEndThreads == len(self.canvas.shapes)*[True]:
        #     self.logFile("dt : %.3f"%(time.time() - self.t0))
        if shape.result :
            print(shape.result)
            return shape.result
        else:
            return None

     def getOCR(self,shape,key,img=None):

        lang = self.paramerterWidget.cbb_language.currentText()
        oem = self.paramerterWidget.cbb_oem.currentIndex()
        psm = self.paramerterWidget.cbb_psm.currentIndex()
        config = '--oem %d --psm %d'%(oem,psm)

        # print(config)

        txt = get_text(img,lang,config=config)

        if shape:
            shape.result["out"][key] = txt

        return txt

     def getBarCode(self,shape,key,img=None):

        if img is None:
            return

        codes = getBarcode(img)
        
        if shape:
            shape.result["out"][key] = codes
    
        return codes

     # actions 
     def read(self,filename,default=None):
        try:
            with open(filename,"rb") as f:
                return f.read()
        except:
            return default

     def createPolygon(self):
        self.canvas.setDrawPolygon()
        self.actions.createShape.setEnabled(True)
     def createShape(self):
        self.canvas.setEditing(False)

        self.actions.createShape.setEnabled(False)

     def remLabel(self, shape):
        if shape is None:
            # print('rm empty label')
            return
        item = self.shapesToItems[shape]
        # index = self.canvas.shapes.index(shape)
        
        self.labelList.takeItem(self.labelList.row(item))
        self.canvas.text = []
        self.canvas.locText = []
        if self.labelList.count() == 0:
            self.actions.implement.setEnabled(False)
            self.actions.editLabel.setEnabled(False)
            self.actions.copy.setEnabled(False)
            self.actions.deleteShape.setEnabled(False)

        del self.shapesToItems[shape]
        del self.itemsToShapes[item]

        # del self.bEndThreads[index]
        
     def boxFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.canvas.fontText = font

     def boxColor(self,obj):
        color = self.colorDialog.getColor(self.lineColor, u'Choose %s color'%obj,
                                          default=DEFAULT_LINE_COLOR)
        # print(color,type(color))
        if color :
            if obj == LINE:
                self.lineColor = color
                Shape.line_color = color
                self.canvas.setDrawingColor(color)
            elif obj == TEXT:
                # pass
                self.canvas.drawingTextColor = color

            self.canvas.update()
            self.setDirty()

     def deleteSelectedShape(self):
        self.remLabel(self.canvas.deleteSelected())

     def implement(self):
        if self.qImage is None:
            return
        shapes = self.canvas.shapes

        self.canvas.text = len(shapes)*[None]
        self.canvas.locText = len(shapes)*[None]
        # self.canvas.drawingTextColor = len(shapes)*[None]
        # print(shape.points)
        self.t0 = time.time()
        self.pool.map(self.shapeProcess,shapes)
        self.logFile("dt : %.3f"%(time.time()-self.t0))
        # multi thread
        # targets = len(shapes)*[self.shapeProcess]
        # args = [(shape,) for shape in shapes]
        # self.myMultiThread(targets = targets, args=args)
        #========
        # dt = time.time() - t0
        # self.logFile("tactime : %s"%dt)

        if self.bSaveOutput:
            pass
    
     def open(self):
        filters = "All File(*.*);;JPG iamge (*.jpg)"
        self.filePath,_ = QFileDialog.getOpenFileName(self,'Select File',"", filters)
        if self.filePath:
            self.mImgList = []
            self.loadFile(self.filePath)
        

     def loadFile(self,filePath):
        self.filePath = filePath
        _,extension = os.path.splitext(filePath)
        if filePath != "" and extension in __imageFile__ and os.path.exists(filePath):
            self.setWindowTitle("Label Master "+filePath)
            self.resetState()
            self.qImage = QImage(filePath)
            # self.qImage = self.qImage.convertToFormat(QImage.Format_ARGB32)
            self.logFile(getFormatQImage(self.qImage))
            # self.cvMat = cv2.imread(self.filePath)
            # if isinstance(self.cvMat,np.ndarray):
            # qImg = cVMatToQImage(self.cvMat[...,::-1])
            self.canvas.loadPixmap(QPixmap.fromImage(self.qImage))

            self.fitState()
        pass

     def openDirDialog(self, _value=False, dirpath=None):
        # if not self.mayContinue():
        #     return

        defaultOpenDirPath = dirpath if dirpath else '.'
        if self.lastOpenDir and os.path.exists(self.lastOpenDir):
            defaultOpenDirPath = self.lastOpenDir
        else:
            defaultOpenDirPath = os.path.dirname(self.filePath) if self.filePath else '.'

        targetDirPath = ustr(QFileDialog.getExistingDirectory(self,
                                                     '%s - Open Directory' % __appname__, defaultOpenDirPath,
                                                     QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks))
        self.importDirImages(targetDirPath)

     def importDirImages(self, dirpath):
        if not dirpath:
            return

        self.lastOpenDir = dirpath
        self.dirname = dirpath
        self.filePath = None
        self.fileLogWidget.clear()
        self.mImgList = self.scanAllImages(dirpath)
        self.openNextImg()
        for imgPath in self.mImgList:
            item = QListWidgetItem(imgPath)
            self.fileLogWidget.addItem(item)

     def scanAllImages(self, folderPath):
        extensions = ['.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        images = []

        for root, dirs, files in os.walk(folderPath):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    relativePath = os.path.join(root, file)
                    path = ustr(os.path.abspath(relativePath))
                    images.append(path)
        natural_sort(images, key=lambda x: x.lower())
        return images

     def openNextImg(self, _value=False):
        # Proceding prev image without dialog if having any label
        # if self.autoSaving.isChecked():
        # if self.defaultSaveDir is not None:
        #     if self.dirty is True:
        #         self.saveFile()
        # else:
        #     self.changeSavedirDialog()
        #     return

        # if not self.mayContinue():
        #     return

        if len(self.mImgList) <= 0:
            return

        filename = None
        if self.filePath is None:
            filename = self.mImgList[0]
        else:
            currIndex = self.mImgList.index(self.filePath)
            if currIndex + 1 < len(self.mImgList):
                filename = self.mImgList[currIndex + 1]

        if filename:
            self.loadFile(filename)

     def openPrevImg(self, _value=False):
        # Proceding prev image without dialog if having any label
        # if self.autoSaving.isChecked():
        #     if self.defaultSaveDir is not None:
        #         if self.dirty is True:
        #             self.saveFile()
        #     else:
        #         self.changeSavedirDialog()
        #         return

        # if not self.mayContinue():
        #     return

        if len(self.mImgList) <= 0:
            return

        if self.filePath is None:
            return

        currIndex = self.mImgList.index(self.filePath)
        if currIndex - 1 >= 0:
            filename = self.mImgList[currIndex - 1]
            if filename:
                self.loadFile(filename)

     def loadParams(self):
        try:
            params = load_from_json("params/param.json")
            shapes = params["shapes"]
            for sh in shapes:
                index,label,r = sh["id"],sh["label"],sh["rect"]
                generate_color = generateColorByText(label)
                shape = Shape(label = label,line_color = generate_color,paintLabel=True)
                # shape.fill = True
                shape.fill_color = generate_color
                shape.points = 4*[QPoint()]
                shape.points[0] = QPointF(r[0],r[1])
                shape.points[1] = QPointF(r[0]+r[2],r[1])
                shape.points[2] = QPointF(r[0]+r[2],r[1]+r[3])
                shape.points[3] = QPointF(r[0],r[1]+r[3])
                shape.close()
                self.canvas.shapes.append(shape)
                self.addLabel(shape)
        except:
            pass



     def save(self):
        a = [self.formatShape(shape) for shape in self.canvas.shapes]
        b = [{"id":i,"label":lb,"rect":[r.x(),r.y(),r.width(),r.height()]} for i,lb,r in a]


        raw_data = {
            "k-thresh" : self.paramerterWidget.ln_threshold.text()
            ,"block size" : self.paramerterWidget.ln_blockSize.text()
            ,"shapes" : b
        }
        save_to_json("params/param.json",raw_data)
        pass

     def setDirty(self):
        self.dirty = True
        # self.actions.createShape.setEnabled(False)
        shape = self.canvas.selectedShape
        # self.implement()

     def formatShape(self,shape):
        if shape is None:
            return None
        points = shape.points
        tl = points[0].toPoint()
        br = points[2].toPoint()
        idx = self.canvas.shapes.index(shape)
        label = shape.label
        cvRect = QRect(tl,br)
        return idx,label,cvRect

     def myThread(self,target,args=()):
        thread = threading.Thread(target=target,args=args)
        thread.start()

     def myMultiThread(self,targets,args):
        for tar,arg in zip(targets,args):
            thread = threading.Thread(target=tar,args=arg)
            thread.start()

     # run thread auto implement
     def loopImplement(self):
        while self.bLoopImplement:
            if self.bAutoImplement and self.bEndThreads==len(self.canvas.shapes)*[True]:
                self.implement()
            time.sleep(0.2)

     # redraw rect
     # ======signal slot================
     def copySelectedShape(self):
        self.addLabel(self.canvas.copySelectedShape())
        # fix copy and delete
        self.shapeSelectionChanged(True)

     def textChanged(self,text):
        # self.canvas.text = text
        self.canvas.update()
     # ================add and edit Label===========================
     def stateChanged(self,iState):
            self.bAutoImplement = self.autoImplement.isChecked()
            if self.bAutoImplement :
                self.bEndThreads = len(self.canvas.shapes)*[True]
            self.bSaveOutput = self.saveOutput.isChecked()
            self.bShowResult = self.updateOuput.isChecked()

            self.canvas.update()

     def fileitemDoubleClicked(self, item=None):
        currIndex = self.mImgList.index(ustr(item.text()))
        if currIndex < len(self.mImgList):
            filename = self.mImgList[currIndex]
            if filename:
                self.loadFile(filename)

     def beginner(self):
        return self._beginner

     def advanced(self):
        return not self.beginner()

     def toggleDrawingSensitive(self, drawing=True):
        """In the middle of drawing, toggling between modes should be disabled."""
        # self.actions.editLabel.setEnabled(not drawing)
        # self.actions.implement.setEnabled(not drawing)
        if not drawing and self.beginner():
            # Cancel creation.
            print('Cancel creation.')
            self.canvas.setEditing(True)
            self.canvas.restoreCursor()
            self.actions.createShape.setEnabled(True)
     def popLabelListMenu(self, point):
        self.menus.labelList.exec_(self.labelList.mapToGlobal(point))

     def popfileLogMenu(self, point):
        self.menus.fileLog.exec_(self.fileLogWidget.mapToGlobal(point))

     def currentItem(self):
        items = self.labelList.selectedItems()
        if items:
            return items[0]
        return None

     def shapeSelectionChanged(self, selected=False):
        if self._noSelectionSlot:
            self._noSelectionSlot = False
        else:
            shape = self.canvas.selectedShape
            if shape:
                self.shapesToItems[shape].setSelected(True)
            else:
                self.labelList.clearSelection()
        self.bSelectionChanged = selected
        self.actions.implement.setEnabled(selected)
        self.actions.editLabel.setEnabled(selected)
        self.actions.copy.setEnabled(selected)
        self.actions.deleteShape.setEnabled(selected)
        # self.actions.shapeLineColor.setEnabled(selected)
        # self.actions.shapeFillColor.setEnabled(selected)

     def editLabel(self):
        if not self.canvas.editing():
            return
        item = self.currentItem()
        if not item:
            return
        # self.descisionDlg.show()
        text = self.labelDialog.popUp(item.text())
        if text is not None:
            shape = self.itemsToShapes[item]
            index,label,rect = self.formatShape(shape)
            item.setText(text)
            item.setBackground(generateColorByText(text))
            self.setDirty()

     def labelSelectionChanged(self):
        item = self.currentItem()
        if item and self.canvas.editing():
            self._noSelectionSlot = True
            self.canvas.selectShape(self.itemsToShapes[item])
            shape = self.itemsToShapes[item]
            # self.actions.editLabel.setEnabled(True)
            # self.actions.implement.setEnabled(True)

     def labelItemChanged(self, item):
        shape = self.itemsToShapes[item]
        label = item.text()
        if label != shape.label:
            shape.label = item.text()
            shape.line_color = generateColorByText(shape.label)
            self.setDirty()
        else:  # User probably changed item visibility
            self.canvas.setShapeVisible(shape, item.checkState() == Qt.Checked)

     def addLabel(self,shape):
         shape.paintLabel = True
         index,label,rect = self.formatShape(shape)
         item = HashableQListWidgetItem(label)
         item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
         item.setCheckState(Qt.Checked)
         item.setBackground(generateColorByText(shape.label))
         self.itemsToShapes[item] = shape
         self.shapesToItems[shape] = item
         self.labelList.addItem(item)

         self.bEndThreads.append(False)
     # =================signal Canvas==========================
     def newShape(self):
        #Pop-up and give focus to the label editor. 
        if self.useDefaultLabelCheckbox.isChecked() and self.defaultLabelTextLine.text():
            label =  self.defaultLabelTextLine.text()   
        else:
            label = self.prevLabel     
        text = self.labelDialog.popUp(text = label)
        if text :
            generate_color = generateColorByText(text)
            shape = self.canvas.setLastLabel(text, generate_color, generate_color)

            self.prevLabel = text
            self.canvas.setEditing(True)
            self.actions.createShape.setEnabled(True)
            self.addLabel(shape)
        else:
               self.canvas.resetAllLines()
     
     def setZoom(self, value):
        # self.actions.fitWidth.setChecked(False)
        # self.actions.fitWindow.setChecked(False)
        self.zoomMode = self.MANUAL_ZOOM
        self.zoomWidget.setValue(value)

     def addZoom(self, increment=10):
        self.setZoom(self.zoomWidget.value() + increment)

     def zoomRequest(self,delta):
        # print(delta)
        # get the current scrollbar positions
        # calculate the percentages ~ coordinates
        h_bar = self.scrollBars[Qt.Horizontal]
        v_bar = self.scrollBars[Qt.Vertical]

        # get the current maximum, to know the difference after zooming
        h_bar_max = h_bar.maximum()
        v_bar_max = v_bar.maximum()

        # get the cursor position and canvas size
        # calculate the desired movement from 0 to 1
        # where 0 = move left
        #       1 = move right
        # up and down analogous
        cursor = QCursor()
        pos = cursor.pos()
        relative_pos = QWidget.mapFromGlobal(self, pos)

        cursor_x = relative_pos.x()
        cursor_y = relative_pos.y()

        w = self.scrollArea.width()
        h = self.scrollArea.height()

        # the scaling from 0 to 1 has some padding
        # you don't have to hit the very leftmost pixel for a maximum-left movement
        margin = 0.1
        move_x = (cursor_x - margin * w) / (w - 2 * margin * w)
        move_y = (cursor_y - margin * h) / (h - 2 * margin * h)

        # clamp the values from 0 to 1
        move_x = min(max(move_x, 0), 1)
        move_y = min(max(move_y, 0), 1)

        # zoom in
        units = delta / (8 * 15)
        scale = 10
        self.addZoom(scale * units)

        # get the difference in scrollbar values
        # this is how far we can move
        d_h_bar_max = h_bar.maximum() - h_bar_max
        d_v_bar_max = v_bar.maximum() - v_bar_max

        # get the new scrollbar values
        new_h_bar_value = h_bar.value() + move_x * d_h_bar_max
        new_v_bar_value = v_bar.value() + move_y * d_v_bar_max

        h_bar.setValue(new_h_bar_value)
        v_bar.setValue(new_v_bar_value)

     def scrollRequest(self, delta, orientation):
        units = - delta / (8 * 15)
        bar = self.scrollBars[orientation]
        bar.setValue(bar.value() + bar.singleStep() * units)

     def setCreateMode(self):
         self.canvas.setEditing(False)

     def paintCanvas(self):
         # assert not self.image.isNull(), "cannot paint null image"
         self.canvas.scale = 0.01 * self.zoomWidget.value()
         self.canvas.adjustSize()
         self.canvas.update()

     def adjustScale(self, initial=False):
        value = self.scalers[self.FIT_WINDOW if initial else self.zoomMode]()
        self.zoomWidget.setValue(int(100 * value))

     def setFitWindow(self, value=True):
        if value:
            self.actions.fitWidth.setChecked(False)
        self.zoomMode = self.FIT_WINDOW if value else self.MANUAL_ZOOM
        self.adjustScale()

     def setFitWidth(self, value=True):
        if value:
            self.actions.fitWindow.setChecked(False)
        self.zoomMode = self.FIT_WIDTH if value else self.MANUAL_ZOOM
        self.adjustScale()

     def scaleFitWindow(self):
        """Figure out the size of the pixmap in order to fit the main widget."""
        e = 2.0  # So that no scrollbars are generated.
        w1 = self.centralWidget().width() - e
        h1 = self.centralWidget().height() - e
        a1 = w1 / h1
        # Calculate a new scale value based on the pixmap's aspect ratio.
        w2 = self.canvas.pixmap.width() - 0.0
        h2 = self.canvas.pixmap.height() - 0.0 
        # a2 = w2/h2
        if h2 == 0 :
            h2 = 1 
        a2 = w2 / h2
        return w1 / w2 if a2 >= a1 else h1 / h2

     def scaleFitWidth(self):
        # The epsilon does not seem to work too well here.
        w = self.centralWidget().width() - 2.0
        return w / self.canvas.pixmap.width()

     def clearList(self):
        # nRow = self.fileLogWidget.count()
        # for i in range(nRow):
        #     self.fileLogWidget.takeItem(i)
        self.fileLogWidget.clear()

     def showCamera(self):
        self.cameraDlg = cameraDialog(self)
        self.cameraDlg.show()

     def resetState(self):
        # self.canvas.deleteSelected()
        # self.labelList.clear()
        # self.itemsToShapes.clear()
        # self.shapesToItems.clear()
        self.canvas.locText = len(self.canvas.shapes)*[None]
        self.canvas.text = len(self.canvas.shapes)*[None]
        # self.canvas.drawingTextColor = len(self.canvas.shapes)*[None]

        self.canvas.resetState()
        self.labelCoordinates.clear()
        self.canvas.setEnabled(False)
        self.canvas.verified = False
        
     def fitState(self):
        self.canvas.setEnabled(True)
        self.adjustScale(initial=True)
        self.paintCanvas()
        self.canvas.setFocus(True)
        
     def resizeEvent(self, event):
        if self.canvas and self.zoomMode != self.MANUAL_ZOOM:
            self.adjustScale()
        super(labelMaster, self).resizeEvent(event)
     def closeEvent(self, event):
        print("Close main")
        self.bLoopImplement = False
        # self.cameraDlg.stopAllThread()

def main():
     import sys
     a = QApplication(sys.argv)
     w = labelMaster()
     w.showMaximized()
     a.exec_()

if __name__ == "__main__":
     main()
